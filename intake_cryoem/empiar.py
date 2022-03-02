import os
import xarray
import matplotlib.pyplot as plt
import xmltodict
import urllib
import requests

from skimage import io
from bs4 import BeautifulSoup

from .mrcsource import MrcSource
from .starsource import StarSource


"""Creating reader for files loaded from EMPIAR: it checks the number
of files in the directory, and goes through them
"""

class empiarDict(dict):
    """Retrieving the EMPIAR directory as a dictionary
    """

    def __init__(self, empiarnumber: int):
        """ To retrieve the dictionary, only the EMPIAR number is necessary """
        self.number = empiarnumber
        self.urlpath = "http://ftp.ebi.ac.uk/empiar/world_availability/" + str(self.number)
        self.xmlpath = self.urlpath + "/" + str(self.number) + ".xml"
        print(type(self.xmlpath))
        self._set_directory()
        self._set_image_data()

    def _set_directory(self):
        """ Gets all the data in the directory """
        print(self.xmlpath)
        file = urllib.request.urlopen(self.xmlpath)
        print("yo")
        data = file.read()
        file.close()

        data = xmltodict.parse(data)
        self.fulldata = data

    def _set_image_data(self):
        """ Gets image groups data """
        self.imagedata = self.fulldata['entry']['imageSet']
        self.number_sets = len(self.imagedata)
        print(self.number_sets)

    def image_directory(self, imagesetnumber: int, directory=None):
        """ Retrieves directory for the images """
        if directory is None:
            return self.urlpath + self.imagedata[imagesetnumber]['directory']
        else:
            return self.urlpath + "/" + self.imagedata[imagesetnumber][directory]

    def all_image_url(self, url):
        """ Retrieves all URLs from image directory """
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        results = []
        for a in soup.find_all('a'):
            if ".." in a:
                continue
            else:
                results.append(url + "/" + a['href'])
        return results


def check_extension(path):
    """Returns the extension of the file
    """
    filename, fileextension = os.path.splitext(path)
    return fileextension


class EmpiarReader:
    def __init__(self, id_number: int, image_set=0, directory=None):
        self.id = id_number
        self.fulldirectory = empiardirectory.empiarDict(self.id)
        self._set_imagesdir(directory, image_set)
        print('done init')

    def iterate_through_files(self):
        """ Goes through the files in the list and retrieves them"""
        print("starting to iterate")
        for i in range(0, len(self.all_image_links)):
            print(self.all_image_links[i])
            if ".." in self.all_image_links[i]:
                continue
            else:
                full_file = self.read_file(self.all_image_links[i])
                print("has opened file")
                full_file.plot()
                # for img in full_file:
                #     plt.imshow(img, cmap='gray')
                #     plt.show()
                #     break

    def read_file(self, path):
        """ Reads the file according to the extension """
        extension = check_extension(path)
        print(extension)
        if "mrc" in extension:
            print(extension)
            f = mrcsource.MrcSource(path.replace("http", "ftp"))
            dataset = f.read()
        elif "star" in extension:
            f = starsource.StarSource(path.replace("http", "ftp"))
            dataset = f.read()
        else:
            f = xarray.DataArray(io.imread(path))
            dataset = xarray.Dataset(f)
        return dataset

    def _set_imagesdir(self, new_directory, image_set=0):
        """ Change the images directory """
        self.imagesdir = self.fulldirectory.image_directory(image_set, new_directory)
        self.all_image_links = self.fulldirectory.all_image_url(self.imagesdir)

    def run(self):
        print("started run")
        self.iterate_through_files()
