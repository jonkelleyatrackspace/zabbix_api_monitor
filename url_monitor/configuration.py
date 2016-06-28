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
            configurations to convienent and common namespace. """
        return {'checks':             self._loadChecks(),
                'config':             self._loadConfig(),
                'identity_providers': self._loadConfigIdentityProviders()}

    def _loadChecks(self,withIdentityProvider=None):
        """ Loads the checks for work to be run.
            Default loads all checks, withIdentityProvider option will limit checks
            returned by identity provider (useful for smart async request grouping)  """
        loaded_checks      = []

        if withIdentityProvider:
            # Useful if doing grouping async requests with a shared identityprovider
            #  and then spawning async call
            for checkdata in self._loadTestSetList():
                if checkdata['data']['identity_provider'].lower() == withIdentityProvider.lower():
                    #loaded_checks.append({'data': checkdata['data']})
                    loaded_checks.append(checkdata)

        else:
            loaded_checks = self._loadTestSetList()

        return loaded_checks

    def _loadConfig(self):
        """ Return base config key """
        return self.config['config']

    def _loadConfigIdentityProviders(self):
        """ This fetches out a list of identity providers kwarg configs from main config """
        providers = {}
        for provider_config_alias, v in self._loadConfig()['identity_providers'].iteritems():
            # Add each provider and config to dictionary from yaml file.
            providers[provider_config_alias] = v
        # Return a list of the config 
        return providers

        """ Loads a list of the checks """

    def _uniq(self,seq):
        """ Returns a unique list when a list of
         non unique items are put in """
        set = {}
        map(set.__setitem__, seq, [])
        return set.keys()

    def getDatatypesList(self):
        """ Used by the discover command to identify a list of valid datatypes """
        possible_datatypes = []
        for testSet in self._loadChecks():
            checkname = testSet['key']
            try:
                uri = testSet['data']['uri']
            except KeyError, err:
                error = "\n\nError: Missing " + str(err) + " under testSet item "+ str(testSet['key']) +", discover cannot run.\n1"
                raise Exception("KeyError: " + str(err) + str(error))

            try:
                testSet['data']['testElements']
            except KeyError, err:
                error = "\n\nError: Missing " + str(err) + " under testSet item "+ str(testSet['key']) +", discover cannot run.\n1"
                raise Exception("KeyError: " + str(err) + str(error))

            for element in testSet['data']['testElements']:  # For every test element
                try:
                    datatypes = element['datatype'].split(',')
                except KeyError, err:
                    error = "\n\nError: Missing " + str(err) + " under testElements in "+ str(testSet['key']) +", discover cannot run.\n1"
                    raise Exception("KeyError: " + str(err) + str(error))
                for datatype in datatypes:
                    possible_datatypes.append(datatype)

        return str(self._uniq(possible_datatypes))
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
        """ Trys loading all the config objects for zabbix conf. This can be expanded to do
            all syntax checking in this config class, instead of in the program logic as it is
            mostly right now. """
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

    def _loadTestSetList(self):
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
    x.load_yaml_file(config=None)
    a = x._loadChecks()
    print(a)
    print(x.getDatatypeList())