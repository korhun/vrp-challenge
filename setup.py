# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_ = f.read()

setup(
    name='vrp-challenge',
    version='0.0.0',
    description='',
    long_description=readme,
    author='Koray Orhun',
    author_email='korhun@gmail.com',
    url='https://github.com/korhun/vrp-challenge',
    license=license_,
    packages=find_packages(exclude='tests')
)
