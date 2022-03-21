
from C4S import CataloguerForStardust

def main():
    # create catalogue "test-name" at the path "./test/"
    c4s = CataloguerForStardust('test-name','test')
    # add target with unique ID=1 at RA=1, DEC=1, z=1
    c4s.create_target(1,1,1,1)
    # add target with unique ID=2 at RA=2, DEC=2, z=2
    c4s.create_target(2,2,2,2)
    # add observation of target ID=1 for instrument (+ filter) A with a flux of 1 ± 0.1 μJy, and assign Stardust filter 1 to it.
    c4s.add_observation(1,'A',1,0.1,'uJy',code=1)
    # add observation of target ID=2 for instrument (+ filter) A with a flux of 2 ± 0.5 μJy, and assign Stardust filter 1 to it.
    c4s.add_observation(2,'A',2,0.5,'uJy',code=1)
    # add observation of target ID=1 for instrument (+ filter) B with a flux of 3 ± 0.4 μJy, and assign a square filter around 250 μm.
    c4s.add_observation(1,'B',3,0.4,'uJy',λ=250)
    # Get a print out of the catalogue. Nice for Notebooks.
    print(c4s)
    # save catalogue --> Fits file, config file, param file, bands file and potentially the extra bands file.
    c4s.save()
    

if __name__ == '__main__':
    main()