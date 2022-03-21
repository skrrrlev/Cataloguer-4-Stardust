# Walk-through of the _test.py_.

All output files can be found in the folder _test/_. Take a look to get familiar with them.

#### 1. Create catalogue
```python
# create catalogue "test-name" at the path "./docs/test"
c4s = Cataloguer('test-name','docs/test',unit=astropy.units.mJy)
```
Notice that the catalogue has been defined to be outputted in mJy.

The internal catalogue comes pre-defined with four columns; id, ra, dec & z. Thus, currently the catalogue only consists of those four columns. No rows has been added yet.

#### 2. Add targets
```python
# add target with unique ID=1 at RA=1, DEC=1, z=1
c4s.create_target(1,1,1,1)
# add target with unique ID=2 at RA=2, DEC=2, z=2
c4s.create_target(2,2,2,2)
```

Everytime you add a target, you basically add a row to the fits-file. After running these two lines of code, the internal catalogue now looks like:

| id | ra | dec | z |
|----|----|-----|---|
| 1  | 1  | 1   | 1 |
| 2  | 2  | 2   | 2 |

#### 3. Add observations
```python
# add observation of target ID=1 for instrument (+ filter) A with a flux of 1000 ± 100 μJy, and assign Stardust filter 1 to it.
c4s.add_observation(1,'A',1,0.1,'uJy',code=1)
# add observation of target ID=2 for instrument (+ filter) A with a flux of 2000 ± 500 μJy, and assign Stardust filter 1 to it.
c4s.add_observation(2,'A',2,0.5,'uJy',code=1)
# add observation of target ID=1 for instrument (+ filter) B with a flux of 3000 ± 400 μJy, and assign a square filter around 250 μm.
c4s.add_observation(1,'B',3,0.4,'uJy',λ=250)
```

Running these three lines of codes adds observations to the targets. The table comes out in the following way:

| id | ra | dec | z | f_A | fe_A | f_B | fe_B | wl_B |
|----|----|-----|---|-----|------|-----|------|------|
| 1  | 1  | 1   | 1 | 1   | 0.1  | 3   | 0.4  | 250  |
| 2  | 2  | 2   | 2 | 2   | 0.5  |     |      |      |

Columns prefixed with _f_ contains the flux. Columns prefixed with _fe_ contains the uncertainty of the flux. Columns prefixed with _wl_ contains the central wavelength of the square filter in μm. 

Notice that the _Cataloguer_ has converted the flux and uncertainty to _mJy_.


#### 4. Saving the catalogue
```python
# save catalogue --> Fits file, config file, param file, bands file and potentially the extra bands file.
c4s.save()
```
Saving the catalogue will first and foremost save the fits file. It will look like:

| id | ra | dec | z | f_A | fe_A | f_B | fe_B | wl_B |
|----|----|-----|---|-----|------|-----|------|------|
| 1  | 1  | 1   | 1 | 1   | 0.1  | 3   | 0.4  | 250  |
| 2  | 2  | 2   | 2 | 2   | 0.5  | -99 | -99  | -99  |

Notice that values that do not exist, but are required in the table structure, has been added as _-99_. This is the standard _missing value_ format for _Stardust_. 

A _.bands_ file is created that links the _A_-column to the _Stardust_ filter code 1. It contains the following line:
```console
1 f_A fe_A
```

A *.bands_extra* file is created that links the _B_-column to the central wavelength. It contains the following line:
```console
wl_B f_B fe_B
```

A *.params* file is created that links the id and redshift to their correct columns. It contains the lines:
```console
id id
z z
Mstar None
```
Currently, there's no way to add stellar masses. 

Lastly, a _.config_ file is created, that can easily be customized to how you want to apply _Stardust_. However, it comes pre-fitted with the correct paths to the various input files. Also, you can run it directly with _Stardust_, and the output will be saved in _output/_ folder located in the same directory as the configuration files.


