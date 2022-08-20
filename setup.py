from setuptools import setup, find_packages
from distutils.util import convert_path

module_globals = {}
with open(convert_path('psd_generator_builder/version.py')) as f:
    exec(f.read(), module_globals)

setup(
    name="psd_generator_builder",
    version=module_globals['__version__'],
    description="Convert a PSD file to PNG files.",
    author="34j",
    url="https://github.com/34j/psd_generator_builder",
    packages=find_packages('psd_generator_builder'),
    install_requires=['git+https://github.com/34j/psd2pngs.git'],
    license='MIT',
    entry_points={
        "console_scripts": [
            "psd_generator_builder = psd_generator_builder.__main__:psd_generator_builder",
        ],
    }
)