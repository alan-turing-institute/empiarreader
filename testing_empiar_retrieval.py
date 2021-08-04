from components import empreader

# dict_10340 = empiardirectory.empiarDict(10340)
# dict_10003 = empiardirectory.empiarDict(10003)

# file = urllib.request.urlopen("http://ftp.ebi.ac.uk/empiar/world_availability/10340/10340.xml")
# data = file.read()
# file.close()
data = empreader.EmpiarReader(10340, directory='micrographsFilePattern')
data.run()
# Getting the urls for each image
# imagesdict = dict_10340.image_directory(0, directory='micrographsFilePattern')
# all_image_links = dict_10340.all_image_url(imagesdict)
#
# for i in all_image_links:
#     if ".." in i:
#         continue
#     else:
#         filename, fileextension = os.path.splitext(i)
#         f = mrcsource.MrcSource(i.replace("http", "ftp"))
#         all_images = f.read()
#         # f.read() function changed from Alan's version as this one retrieves a dataset of dataarrays
#         if f.npartitions == 1:
#             # plt.figure(figsize=(16, 16))
#             plt.imshow(all_images[0], cmap='gray')
#             plt.show()
#         else:
#             for img in all_images:
#                 plt.figure(figsize=(16, 16))
#                 plt.imshow(img[2000:4000, 2000:4000], cmap='gray')
#                 plt.show()
#         break


