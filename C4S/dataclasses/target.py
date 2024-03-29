# imports
from typing import Union

# relative imports
from .columntype import ColumnType

MISSING_FLUX = -99
MISSING_UNCERTAINTY = 1E10
MISSING_WAVELENGTH = -99

class Target:
    def __init__(self, id: int, ra: float, dec: float, z: float) -> None:
        self.id = id
        self.ra = ra
        self.dec = dec
        self.z = z
        self.observations: "dict[str,dict[str,Union[float,None]]]" = {}

    def __repr__(self):
        return f'{self.id:9}>  RA:{self.ra:.5f}  DEC:{self.dec:.5f}  z:{self.z:3f} | observations: {len(self.observations)}'

    def __eq__(self, __o: "Target") -> bool:
        return self.id == __o.id

    def add_observation(self,name:str, f: float, Δf:float, λ: Union[float, None]) -> None:
        self.observations[name] = {'flux': f, 'flux_uncertainty': Δf, 'wavelength': λ}

    def does_observation_exist(self, name:str ) -> bool:
        return name in self.observations

    def get_flux_and_uncertainty(self, name: str) -> "tuple[float,float]":
        if not self.does_observation_exist(name):
            return (MISSING_FLUX,MISSING_UNCERTAINTY)
        else:
            flux = self.observations[name]['flux']
            uncertainty = self.observations[name]['flux_uncertainty']
            return (flux, uncertainty)

    def get_wavelength(self,name: str):
        if not self.does_observation_exist(name):
            return MISSING_WAVELENGTH
        elif not self.observations[name]['wavelength']: # if wavelength is None
            raise ValueError(f'Observation "{name}" is not of type {ColumnType.EXTRA}')
        else:
            return self.observations[name]['wavelength']

    def get_info(self,info: str):
        if info.lower() == 'id':
            return self.id
        elif info.lower() in ['ra','right ascension']:
            return self.ra
        elif info.lower() in ['dec','declination']:
            return self.dec
        elif info.lower() in ['z','redshift']:
            return self.z
        else:
            raise NotImplementedError(f'This was not supposed to happen. Requested info: {info} from target {self.id}')
