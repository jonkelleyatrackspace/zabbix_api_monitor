# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
from setuptools import setup

import sys
sys.path.insert(0, '.')

from url_monitor.packaging import version, authors, emails, license, install_requires
from url_monitor.packaging import long_description, description, package, url, software_classified

if __name__ == "__main__":
    setup(
        name=package,
        version=version,
        author=authors,
        author_email=emails,
        url=url,
        license=license,
        packages=[package],
        package_dir={package: package},
        description=description,
        long_description=long_description,
        classifiers=software_classified,
        entry_points={
            'console_scripts': ['url_monitor = url_monitor.main:main'],
        },
        data_files=[('/etc', ['url_monitor.yaml'])],
        install_requires=install_requires
    )
