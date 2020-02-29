from setuptools import setup



setup(
    name='compmed',
    version='0.1',
    packages=['compmed', 'compmed_utils'],
    include_package_data=True,
    url='https://github.com/FredHutch/ComprehendMedicalInterface',
    license='',
    author='whiteau',
    author_email='whiteau@fredhutch.org',
    description='a package for Amazon Service Interfaces for internal Hutch use',
    install_requires=['awscli', 'boto3'],
    zip_safe=False
)

