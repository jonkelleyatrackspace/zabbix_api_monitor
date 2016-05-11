#!/usr/bin/python

import yaml
import logging

class ConfigObject(object):
    """ This class makes YAML configuration
    available as python datastructure. """

    def __init__(self):
        self.config = None
        self.checks = None

    def load_yaml_file(self, config):
        if config == None:
            config ="/etc/url_monitor.yaml"

        with open(config, 'r') as stream:
            try:
                self.config = (yaml.load(stream))
                return self.config
            except yaml.YAMLError as exc:
                print(exc)

    def load(self):
        """ This is the main config load function to pull in
            configuration in the main program """
        return {'checks': self._load_check_list(), 'config': self.config['config'], 'identity_providers': self._load_identity_providers()}

    def _load_identity_providers(self):
        """ This fetches out a list of identity providers based on the key of the config alias. """
        providers = {}
        for provider_config_alias, v in self.config['config']['identity_providers'].iteritems():
            # Add each provider and config to dictionary from yaml file.
            providers[provider_config_alias] = v
        # Return a list of the config 
        # or as well as a covnient provider_list  [x for x in providers]
        return providers

    def get_log_level(self,debug_level=None):
        """ Allow user-configurable log-leveling """
        try:
            if debug_level == None:
                debug_level = self.config['config']['loglevel']
        except KeyError, err:
            print("Error: Missing " + str(err) + " in config under config: loglevel.\nTry config: loglevel: Exceptions")
            print("1")
            exit(1)
        if (debug_level.lower().startswith('err') or debug_level.lower().startswith('exc')):
            return logging.ERROR
        elif debug_level.lower().startswith('crit'):
            return logging.CRITICAL
        elif debug_level.lower().startswith('warn'):
            return logging.WARNING
        elif debug_level.lower().startswith('info'):
            return logging.INFO
        elif debug_level.lower().startswith('debu'):
            return logging.DEBUG
        else:
            return logging.ERROR

    def load_zabbix(self):
        """ Trys loading all the config objects for zabbix conf. """
        try:
            self.config['config']
            self.config['config']['zabbix']['host']
            self.config['config']['zabbix']['port']
        except KeyError, err:
            print("Error: Missing zabbix: " + str(err) + " structure in config under config.")
            print("You need that to configure your zabbix destination host for metrics")
            print("1")
            exit(1)
        try:
            self.config['config']['zabbix']['item_key_format']
        except KeyError, err:
            print("Error: Missing zabbix: " + str(err) + " structure in config under config.")
            print("This is a string template that maps to the item name you see in Zabbix")
            print("It takes {macros} you can reference from testElements, as well as builtins")
            print(" called {datatype}, {uri}")
            print(str(err) + ": url_monitor[{datatype}, {metricname}, {uri}] is a good start")
            print("1")
            exit(1)

    def _load_check_list(self):
        """ Used to prepare format of data for the checker functions
        out of the configuration file.
        Here is a sample of return output.
        [{
            "elements": [
                {
                    "jsonvalue": "./jobSuccess",
                    "key": "StatusJob.success"
                },
                {
                    "jsonvalue": "./jobFailure",
                    "key": "StatusJob.failure"
                }
            ],
            "response_type": "json",
            "url": "https://x.net/v3/jobs/statusjob/stats/totals"
        },
        {
            "elements": [
                {
                    "jsonvalue": "./report[1]/status",
                    "key": "./report[1]/name"
                },
            ],
            "response_type": "json",
            "url": "https://x.net/dependencies"
        }]"""

        self.checks = []
        for testSet in self.config['testSet']:
            for key, v in testSet.iteritems():
                self.checks.append({'key': key, 'data': testSet[key]})

        return self.checks

if __name__ == "__main__":
    x = ConfigObject()
    a = x.load_check_list()
    print(a)
