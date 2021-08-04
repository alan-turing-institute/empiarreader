import xmltodict
import urllib
import requests
from bs4 import BeautifulSoup


class empiarDict(dict):
    """ Retrieving the EMPIAR directory as a dictionary """

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

