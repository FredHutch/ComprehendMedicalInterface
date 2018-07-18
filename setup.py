import os.path
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
from shutil import copyfile

setup_path = os.path.dirname(os.path.realpath(__file__))

def make_awscli_call():
    full_path = os.path.sep.join([setup_path,
                                  "amazonserviceinterface\models\deepinsighthera-2017-01-01.normal.json"])

    amazon_file_pull_string = "".join(["file://", full_path])

    print("adding {} to aws client".format(full_path))

    check_call("aws configure add-model "
               "--service-model {}"
               " --service-name {} ".format(amazon_file_pull_string,
                                            "deepinsighthera"
                                            ).split())

def place_aws_model_in_home_dir():
    home = os.path.expanduser("~")
    aws_model_dir = os.path.sep.join([home, ".aws", "models", "deepinsighthera", "2017-01-01"])

    if not os.path.exists(os.path.sep.join([aws_model_dir, "deepinsighthera-2017-01-01.normal.json"])):
        if not os.path.isdir(aws_model_dir):
            os.mkdir(aws_model_dir)
        src_path = os.path.sep.join([setup_path,
                                      "amazonserviceinterface\models\deepinsighthera-2017-01-01.normal.json"])
        print("copying {} to {}".format(src_path, aws_model_dir))
        copyfile(src_path, aws_model_dir)

    return None

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        print(setup_path)
        make_awscli_call()
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        print(setup_path)
        print("abs path of package dir: {}".format(os.path.dirname(os.path.realpath(__file__))))
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        #place_aws_model_in_home_dir()
        make_awscli_call()
        install.run(self)

setup(
    name='AmazonServiceInterface',
    version='0.1',
    packages=['amazonserviceinterface', 'clinicalnotesprocessor', 'utils'],
    url='https://github.com/FredHutch/HDCMedLPInterface',
    license='',
    author='whiteau',
    author_email='whiteau@fredhutch.org',
    description='a package for Amazon Service Interfaces for internal Hutch use',
    install_requires=['boto3', 'awscli'],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    zip_safe=False
)

