from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    '''
    This function will return the list of required modules
    '''

    HYPHEN_E_DOT = "-e ."

    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements

setup(
    name='SMS_Spam_filter',
    version='0.1',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
            'your_script_name=your_package.module:main',
        ],
    },
    author='Sandipan Dutta',
    author_email='sandipanarnab@hotmail.com',
    description='Multilabel Eye Disease Classification',
    url='https://github.com/sandipanarnab/Spam-filter-based-on-personal-SMS-data.git',
)
