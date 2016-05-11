# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
from setuptools import setup

import sys
sys.path.insert(0, '.')

from url_monitor.metadata import version, authors, emails, license, url

NAME = "url_monitor"
SHORT_DESC = "A tool used to monitor api endpoint data in zabbix"


if __name__ == "__main__":
    setup(
        name=NAME,
        version=version,
        author=authors,
        author_email=emails,
        url=url,
        license=license,
        packages=[NAME],
        package_dir={NAME: NAME},
        description=SHORT_DESC,
        classifiers=[
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: System :: Monitoring',
            'Topic :: System :: Networking :: Monitoring',
            'Topic :: System :: Systems Administration ',
        ],
        entry_points={
            'console_scripts': ['url_monitor = url_monitor.main:main'],
        },
        data_files=[('/etc', ['url_monitor.yaml'])],
        install_requires=['python-daemon',
                          'requests',
                          'requests-oauthlib',
                          'oauthlib',
                          'argparse',
                          'PyYAML',
                          'importlib']
    )
