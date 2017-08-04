#!/usr/bin/env python
from setuptools import setup, find_packages

install_reqs = [
    'Django>=1.11',
    'Pillow>=4.1.1',
]

setup(
    name='django-image-compressor',
    version='0.0.4',
    description='Compress static images from Django with Pillow',
    author='James Christopher',
    author_email='jcahall@washington.edu',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    url='https://github.com/jameschristopher/django-image-compressor',
    install_requires=install_reqs,
)