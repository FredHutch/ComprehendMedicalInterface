from setuptools import setup

setup(
    name='AmazonServiceInterface',
    version='0.1',
    packages=['amazonserviceinterface', 'clinicalnotesprocessor', 'utils'],
    url='https://github.com/FredHutch/HDCMedLPInterface',
    license='',
    author='whiteau',
    author_email='whiteau@fredhutch.org',
    description='a package for Amazon Service Interfaces for internal Hutch use',
    install_requires=['boto3'],
    zip_safe=False
)
