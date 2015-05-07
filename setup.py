import os

from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='pipedrive-py',
    version='0.3.25',
    description='Python lib for the pipedrive.com api',
    long_description=(read('README.md') + '\n\n' +
                      read('HISTORY.md') + '\n\n' +
                      read('AUTHORS.md')),
    url='http://github.com/loggi/pipedrive-py/',
    license='BSD License',
    author='Arthur Debert',
    author_email='arthur@loggi.com',
    install_requires=['schematics', 'requests'],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
