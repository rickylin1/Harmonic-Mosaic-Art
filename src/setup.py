#this helps setup app.py second iteration

from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'html5lib',
    'pandas',
    'pathlib',
]

setup(
    name = 'spotify tool',
    version = '1.0',
    description = 'an app for me to retreieving user spotify data and analyzing it',
    author = 'Ricky Lin',
    packages = find_packages(),
    include_package_data =  True,
    install_requires = requires


)

