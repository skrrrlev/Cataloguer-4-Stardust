# imports
from astropy import units as U
from astropy.io import fits
from os import makedirs, remove
from os.path import isdir, isfile
import numpy as np

# relative imports
from .dataclasses import Target, ColumnType

class Cataloguer:
    '''This cataloguer can create the input files that the Stardust SED fitting algorithm uses.

        It is initialised by defining a name for the catalogue,
        a path to where it should be stored and a flux-unit (μJy ,mJy, ...)
        
        It has two main features:

        Add target:

            Add a new target to the catalogue.

                Each unique target is identified by an ID <int>.

            Must also pass the RA, DEC and redshift of the target, however, they are not being actively used by Stardust.
        
        Add observation:
            Add an observation of a target to the catalogue.

            Specify the ID of the target that the observation belongs to.

            Each observations is characterized by a name describing the unique column that it will become a part of.

                Each column essentially corresponds to an instrument (+ filter)

            Must either specify a code, corresponding to the transmission curve in the Stardust filter-list,
            or the central wavelength (in μm), causing Stardust to create a 10μm-wide square transmission filter. 

    '''

    def __init__(self, name: str, path: str, flux_unit=U.mJy) -> None:

        self.name = name
        '''Name of catalogue instance'''

        self.path = path
        '''Path to files created by Cataloguer.'''

        self._clean_directory()

        self.flux_unit = flux_unit
        '''Unit of flux and flux uncertainties'''

        self.columns = {
            'id': {'format': 'K', 'unit': None, 'type': ColumnType.INFO},
            'ra': {'format': 'E', 'unit': None, 'type': ColumnType.INFO},
            'dec': {'format': 'E', 'unit': None, 'type': ColumnType.INFO},
            'z': {'format': 'E', 'unit': None, 'type': ColumnType.INFO}
        }
        '''Columns of the resulting fits file.'''

        self.targets: "dict[int,Target]" = {}
        '''Dictionary using target ids as keys, containing target objects.'''

        self.extra_bands: bool = False
        '''Boolean check for whether any extra bands has been added.'''

    def __repr__(self) -> str:
        string = f'----< Catalogue-4-Stardust >----\n'
        string += f'name:    {self.name}\n'
        string += f'path:    {self.path}\n'
        string += f'targets: {len(self.targets)}\n'
        for target in self.targets:
            string += f'{self.targets[target]}\n'
        string += '-------------------------------'
        return string
    
    def _clean_directory(self) -> None:
        '''Prepare specified directory for Cataloguer.'''
        
        self.path = self.path.replace('\\', '/')
        if not self.path.endswith('/'):
            self.path += '/'

        if not isdir(self.path):
            makedirs(self.path)
            return
        
        if isfile(self.path + self.name + '.fits'):
            remove(self.path + self.name + '.fits')
        if isfile(self.path + self.name + '.bands'):
            remove(self.path + self.name + '.bands')
        if isfile(self.path + self.name + '.bands_extra'):
            remove(self.path + self.name + '.bands_extra')
        if isfile(self.path + self.name + '.config'):
            remove(self.path + self.name + '.config')
            
    
    def does_target_exist(self, id) -> bool:
        '''Returns boolean describing whether a target with the given id exists in the Cataloguer.'''
        return id in self.targets

    def create_target(self, id: int, ra: float, dec: float, z: float) -> None:
        '''Add a new target to the Cataloguer.'''
        if not self.does_target_exist(id):
            self.targets[id] = Target(id = id, ra = ra, dec = dec, z = z)
        else:
            raise ValueError(f'Target {id} already exists.')

    def does_column_exist(self, name: str) -> bool:
        '''Returns boolean describing whether a column with the given unique "name" exists in the Cataloguer.'''
        return name in self.columns

    def add_observation(self, id: int, name: str, f: float, Δf:float, unit: str, code: int = None, λ: float = None):
        '''Add an observation to a target in the Cataloguer.
            The Cataloguer will automatically keep track of the types of observations added.'''

        if not unit == str(self.flux_unit):
            f = ((f*U.Unit(unit)).to(self.flux_unit)).value
            Δf = ((Δf*U.Unit(unit)).to(self.flux_unit)).value
        
        tp = None
        if code and λ: 
            raise ValueError('Observation cannot be regular filter and an extra band.')
        elif code:
            tp = ColumnType.FILTER
        elif λ:
            tp = ColumnType.EXTRA
        else:
            raise ValueError('Please specify either a stardust code or a extra-band wavelength.')

        if not self.does_column_exist(name):
            self.columns[name] = {'format': 'E', 'unit': str(self.flux_unit), 'type': tp}
            if tp == ColumnType.FILTER:
                self._add_to_bands_file(name, code)
            elif tp == ColumnType.EXTRA:
                self._add_to_extra_bands_file(name)

        self.targets[id].add_observation(name, f, Δf, λ)


    def _add_to_bands_file(self, name: str, code: int) -> None:
        '''
        Add new line to the .bands file, connecting the stardust code with the name of the flux and flux-uncertainty column.
        Automatically runs everytime a new "filter"-type column is defined.
        '''
        file = self.path + self.name + '.bands'
        if isfile(file):
            open_code = 'a'
        else:
            open_code = 'w'

        with open(file, open_code) as f:
            f.write(f'{code} f_{name} fe_{name}\n')

    def _add_to_extra_bands_file(self, name: str) -> None:
        '''
        Add new line to the .extra_bands file, connecting the central wavelength column to the flux and flux-uncertainty column.
        Automatically runs everytime a new column "extra bands"-type column is defined.
        '''
        file = self.path + self.name + '.bands_extra'
        if isfile(file):
            open_code = 'a'
        else:
            open_code = 'w'

        with open(file, open_code) as f:
            f.write(f'wl_{name} f_{name} fe_{name}\n')

        if not self.extra_bands:
            self.extra_bands = True



    def _write_config_file(self):
        '''Create the config file. Is used by the save() method.'''
        content = f'''#===============================================================================
#INPUT PARAMETERS
#===============================================================================
CATALOGUE   {self.path}{self.name}.fits
BANDS_FILE  {self.path}{self.name}.bands
EXTRA_BANDS_FILE {self.path+self.name+'.bands_extra' if self.extra_bands else 'None'}
PARAM_FILE  {self.path}{self.name}.param
#===============================================================================
#OUTPUT PARAMETERS
#===============================================================================
PATH    {self.path}outputs/test/
OUTPUT_NAME test
FIGLOC  {self.path}outputs/test/figures/
sedloc  {self.path}outputs/test/seds/
#covarloc test/output/covar
SAVE_FIGURE 1
SAVE_TABLE 1
SAVE_SED 1
SAVE_COVAR 0
#===============================================================================
#GENERAL SETTINGS
#===============================================================================
VERBOSE 1 
FLUX_UNIT   {str(self.flux_unit)}
EXTRA_BANDS {1 if self.extra_bands else 0}
USE_COLD_DL 1
RADIO_METHOD    delv20
#===============================================================================
#ADVANCED SETTINGS
#===============================================================================
UNCERT_SCALE 0.05
QSO 0
IGM_SWITCH 0
USE_OWN_STELLAR_MASS False
ABZP    23.9
#===============================================================================
#TEMPLATE PARAMETERS
#===============================================================================
FIT_DUST 1
FIT_AGN 0
FIT_STELLAR 1
#===============================================================================
'''
        with open(self.path+self.name+'.config', 'w') as f:
            f.write(content)
        print(f"Created config file: {self.path+self.name+'.config'}")


    def _write_param_file(self):
        '''Create the .param file. Used by the save() method.'''
        with open(self.path+self.name+'.param', 'w') as f:
            f.write('id id\n')
            f.write('z z\n')
            f.write('Mstar None')
        print(f"Created param file: {self.path+self.name+'.param'}")

    def _write_fits_file(self):
        '''Create the fits file. Used by the save() method.'''

        # Define variable to hold fits columns.
        fits_columns: "dict[str, fits.Column]" = {}
        
        # Create empty fits columns
        for name in self.columns:
            _type = self.columns[name]['type']
            _format = self.columns[name]['format']
            _unit = self.columns[name]['unit']

            if _type == ColumnType.INFO:
                fits_columns[name] = fits.Column(name=name, array=np.array([]), format=_format)
            elif _type == ColumnType.FILTER:
                f_name = f'f_{name}'
                fe_name = f'fe_{name}'
                fits_columns[f_name] = fits.Column(name=f_name,array=np.array([]),format=_format, unit=_unit)
                fits_columns[fe_name] = fits.Column(name=fe_name,array=np.array([]),format=_format, unit=_unit)
            elif _type == ColumnType.EXTRA:
                f_name = f'f_{name}'
                fe_name = f'fe_{name}'
                λ_name = f'wl_{name}'
                fits_columns[f_name] = fits.Column(name=f_name,array=np.array([]),format=_format, unit=_unit)
                fits_columns[fe_name] = fits.Column(name=fe_name,array=np.array([]),format=_format, unit=_unit)
                fits_columns[λ_name] = fits.Column(name=λ_name,array=np.array([]),format=_format, unit=_unit)
            else:
                raise NotImplementedError(f'This was not supposed to happen:\ntype={_type}, name={name}')

        # fill in fits columns.
        for id in self.targets:
            target = self.targets[id]
            for name in self.columns:
                _type = self.columns[name]['type']
                if _type == ColumnType.INFO:
                    fits_columns[name].array = np.append(fits_columns[name].array, target.get_info(name))
                elif _type == ColumnType.FILTER:
                    f_name = f'f_{name}'
                    fe_name = f'fe_{name}'
                    f, fe = target.get_flux_and_uncertainty(name)
                    fits_columns[f_name].array = np.append(fits_columns[f_name].array, f)
                    fits_columns[fe_name].array = np.append(fits_columns[fe_name].array, fe)
                elif _type == ColumnType.EXTRA:
                    f_name = f'f_{name}'
                    fe_name = f'fe_{name}'
                    wl_name = f'wl_{name}'
                    f, fe = target.get_flux_and_uncertainty(name)
                    wl = target.get_wavelength(name)
                    fits_columns[f_name].array = np.append(fits_columns[f_name].array, f)
                    fits_columns[fe_name].array = np.append(fits_columns[fe_name].array, fe)
                    fits_columns[wl_name].array = np.append(fits_columns[wl_name].array, wl)

        # save file
        columns = [fits_columns[key] for key in fits_columns]
        hdu = fits.BinTableHDU.from_columns(columns)
        hdu.writeto(self.path+self.name+'.fits',overwrite=True)
        print(f"Created fits file: {self.path+self.name+'.fits'}")

    def save(self):
        print('Saving catalogue.')
        self.print_targets()
        self._write_config_file()
        self._write_param_file()
        self._write_fits_file()

    def print_targets(self):
        for target in self.targets:
            print(self.targets[target])



