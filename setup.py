from setuptools import find_packages, setup
setup(
    name='gscholar_search',
    packages=find_packages(),
    version='0.1.0',
    description='Program to search and parse google scholar results',
    author='Onur Kara',
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.1.1'],
    test_suite='tests',
)
