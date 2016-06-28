#!/usr/bin/python
# -*- coding: utf-8 -*-
__doc__ = """url_monitor

Extensible URL monitor that iterates through supplied json/yaml
files to pull remote data from fields in http, xml, or json
documents and sends data to remote sources.  To support zabbix,
Rackspace Cloud Monitoring, collectd, etc...
"""

# The package name, which is also the "UNIX name" for the project.
package = 'url_monitor'
project = "URL Monitor Module"
project_no_spaces = project.replace(' ', '')
version = '0.8.9'
description = 'A zabbix plugin to perform URL endpoint monitoring for JSON and XML REST APIs, supporting multiple http auth mechinisms'
authors = ['Jon Kelley', 'Nick Bales']
authors_string = ', '.join(authors)
emails = ['jon.kelley@rackspace.com',
          'nick.bales@rackspace.com']
license = 'ASLv2'
company = "Rackspace, Inc."
copyright = '2016 ' + company
url = 'https://github.com/jonkelleyatrackspace/zabbix_url_monitor'
