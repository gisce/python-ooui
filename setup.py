from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("requirements-dev.txt", "r") as f:
    requirements_dev = f.read().splitlines()

setup(
    name='ooui',
    description='Open Object User Interface',
    author='GISCE',
    author_email='devel@gisce.net',
    url='https://github.com/gisce/python-ooui',
    version='0.12.2',
    license='MIT',
    long_description='''Open Object User Interface for GISCE-ERP''',
    provides=['ooui'],
    install_requires=requirements,
    tests_require=requirements_dev,
    packages=find_packages()
)
