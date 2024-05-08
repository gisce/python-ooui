from setuptools import setup, find_packages

setup(
    name='ooui',
    description='Open Object User Interface',
    author='GISCE',
    author_email='devel@gisce.net',
    url='https://github.com/gisce/python-ooui',
    version='0.1.0',
    license='MIT',
    long_description='''Open Object User Interface for GISCE-ERP''',
    provides=['ooui'],
    install_requires=[
        'lxml',
        'python-dateutil',
        'six',
    ],
    tests_require=[
        'mamba',
        'expects',
    ],
    packages=find_packages()
)
