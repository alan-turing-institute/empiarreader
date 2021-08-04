import os
from intake_cryoEM.components import empiardirectory
from intake_cryoEM.components import mrcsource
from intake_cryoEM.components import starsource
import xarray
from skimage import io
import matplotlib.pyplot as plt

""" Creating reader for files loaded from EMPIAR: it checks the number of files in the directory, and goes through them """


def check_extension(path):
    """ Returns the extension of the file """
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
