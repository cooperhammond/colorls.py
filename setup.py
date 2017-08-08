from setuptools import setup

setup(
    name =                 'colorls',
    version =              '0.0.1',
    description =          'A music downloader that just gets metadata.',
    url =                  'https://github.com/kepoorhampond/colorls.py',
    author =               'Kepoor Hampond',
    author_email =         'kepoorh@gmail.com',
    license =              'MIT',
    packages =             ['colorls'],
    package_data =         {'colorls': 'colorls/yaml/*'},
    include_package_data = True,
    install_requires = [
        'pyyaml',
    ],
    entry_points = {
        'console_scripts': ['colorls_ = colorls.cli:main'],
    },
)
