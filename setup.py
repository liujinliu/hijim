# -*- coding: utf-8 -*-
import os
import setuptools
from setuptools import find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def _find_requires():
    with open(os.path.join(HERE, 'requirments.txt')) as f:
        lines = f.readlines()
        requires = []
        for line in lines:
            if line.strip():
                requires.append(line.strip())
        return requires


def _setup():
    setuptools.setup(
        name='hijim',
        version='0.0.1',
        description='',
        long_description='',
        author='liujinliu',
        url='https://gitee.com/liujinliu/hijim',
        license='Apache',
        install_requires=_find_requires(),
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
