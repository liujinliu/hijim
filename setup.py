# -*- coding: utf-8 -*-
import os
import setuptools
from setuptools import find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def _setup():
    setuptools.setup(
        name='hijim',
        version='0.0.1',
        description='',
        long_description='',
        author='liujinliu',
        url='https://github.com/liujinliu',
        license='Apache',
        install_requires=[
            'sqlalchemy[asyncio]==1.4.41',
            'tornado==6.2',
            'python-dateutil==2.8.2'
        ],
        packages=find_packages('src'),
        package_dir={'': 'src'},
        entry_points={
            'console_scripts': []
            },
        classifiers=[
            'Environment :: Console',
        ],
    )


def main():
    _setup()


if __name__ == '__main__':
    main()
