# Cataloguer For Stardust (``C4S``)
A tool for easily creating the necessary input files for the [Stardust SED fitting code](https://github.com/VasilyKokorev/stardust.git) using your own data.

## Setup

This package can be installed using _pip_. It is made using Python version 3.9.6, but also works for version 3.6.15, which is needed to run _Stardust_. 

```console
python -m pip install C4S@git+https://github.com/skrrrlev/Cataloguer-4-Stardust.git
```

## Initialisation
The cataloguer can now be imported and used.
```python
from C4S import Cataloguer
from astropy import units as U
test_catalogue = Cataloguer(name='test',path='.',unit=U.mJy)
```

A more comprehensive walk-through can be found in the _docs_ section of this git-page. 