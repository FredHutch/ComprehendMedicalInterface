import os.path
from pkg_resources import Requirement, resource_filename
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call


def make_awscli_call():
    '''
    helper function to install beta models via awscli call.
    more information can be found here:
    https://setuptools.readthedocs.io/en/latest/pkg_resources.html

    :return:
    '''
    filename = resource_filename(Requirement.parse("AmazonServiceInterface"), "models/deepinsighthera-2017-01-01.normal.json")

    amazon_file_pull_string = "".join(["file://", filename])

    print("adding {} to aws client".format(filename))

    check_call("aws configure add-model "
               "--service-model {}"
               " --service-name {} ".format(amazon_file_pull_string,
                                            "deepinsighthera"
                                            ).split())


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        make_awscli_call()
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        make_awscli_call()
        install.run(self)

setup(
    name='AmazonServiceInterface',
    version='0.1',
    packages=['amazonserviceinterface', 'clinicalnotesprocessor', 'utils'],
    include_package_data=True,
    url='https://github.com/FredHutch/HDCMedLPInterface',
    license='',
    author='whiteau',
    author_email='whiteau@fredhutch.org',
    description='a package for Amazon Service Interfaces for internal Hutch use',
    install_requires=['awscli', 'boto3'],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    zip_safe=False
)

