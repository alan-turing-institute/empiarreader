from intake.config import conf

from intake_cryoem.empiar import EmpiarCatalog, EmpiarSource

import os

# stolen from test_empiar_retrieval.test_empiar 
# and adapting to test caching and renamed cache
def test_empiar_cache():
    conf['cache_download_progress'] = True
    conf['cache_dir'] = os.path.join(os.getcwd(), 'test_cache_dir')
    for attr in dir(conf):
        print('conf attr {} is {}'.format(attr, getattr(conf,attr)))
    print('\n\n')

    # now get all conf dict entries
    for k,v in conf.items():
        print('Key: {} is: {}'.format(k,v))
    print('\n\n')

    cat = EmpiarCatalog(10340)
    print(cat)
    print(list(cat))
    print('\n\n')

    # I think cat(alogue) is a list of imagesets
    # So EmpiarCatalogue() starts by grabbing the name of the imagesets by reading them
    # from the online path (EmpiarCatalogue.fetch_entrydata()). 
    # This list ??? should be accessible via EmpiarCatalogue.imagesets
    
    # Now checking after initialisation of EmpiarCatalogue what actually is 
    # present in it:
    print('Dir of EmpiarCatalogue.entry_data: {}'.format(dir(cat)))
    for thing in dir(cat):
        print('Cat thing {} is {}'.format(thing, getattr(cat,thing)))
    print('\n\n')

    # print the args
    for i, entry in enumerate(cat._entries):
        print('Entry {} has {} and is {}'.format(i, entry, type(entry)))
        #for j, arg in enumerate(entry.args):
        #    print('Entry {} has arg {} of {}'.format(i, j, arg))
    
    print('\n\n')

    # I don't think you re actually using the cache yet as you seem to only have grabbed metadata
    # Try grabbing an actual data file and see what happens... do you use cache?
    ds = cat["Unaligned movies for Case 1"]
    ds.read_partition(0)
    



    """
    for i,key in enumerate(cat.keys):
        print('{}: {}'.format(i, key))
    """
    return

    assert "Unaligned movies for Case 1" in cat.keys()

    ds = cat["Unaligned movies for Case 1"]

    assert isinstance(ds, EmpiarSource)

    assert ds.directory == "data/Movies/Case1"

    # Note: ds.read() is expensive

if __name__ == '__main__':
    test_empiar_cache()