from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    # "Thiss funcition is going to return the list"
    requirements = []
    with open(file_path) as file_obj:

        requirements = file_obj.readlines()
        requirements = [req.replace("/n","") for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
            
    return requirements

setup(
    name='Ames_housing',
    packages=find_packages(),
    nstall_requires=get_requirements('requirements.txt'),
    version='0.1.0',
    description='this is real state project where this program predict the value of the property',
    author='Nilansh Garg',
    author_email = 'nilnashgarg13@gmail.com',
    license='MIT',
    
)
