from setuptools import setup


setup(
    name = "C4S",
    author = "Ditlev Frickmann @skrrrlev",
    author_email = "reimer.frickmann@gmail.com",
    description = "A tool for easily creating the necessary input files for the Stardust SED fitting code using your own data.",
    version = "0.0.1",
    license = "MIT",
    url = "https://github.com/skrrrlev/Cataloguer-4-Stardust.git",  
    packages=[
        'C4S',
        'C4S.dataclasses',
    ],
    install_requires = [
        'numpy',
        'astropy',
    ],
)