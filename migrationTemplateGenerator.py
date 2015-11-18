__author__ = 'merne'

import yaml
import re

versionRe = re.compile(r'^[vV]\d+_.+')
sharedRe = re.compile(r'^shared_.+')

class migrationTemplateGenerator:

    def __init__(self, oldVersionFile, newVersionFile):
        self.oldVersionFile = oldVersionFile
        self.newVersionFile = newVersionFile

        with open(oldVersionFile, 'r') as stream:
            self.oldVersion = yaml.load(stream)
        with open(newVersionFile, 'r') as stream:
            self.newVersion = yaml.load(stream)

    def generateAll(self):

        return {1: self.generateFirst(),
                2: self.generateSecond(),
                3: self.newVersion}

    def generateFirst(self):
        generated = {}
        generated['description'] = self.oldVersion['description']
        generated['heat_template_version'] = self.oldVersion['heat_template_version']

        # this needs to be enhanced at some point
        generated['parameters'] = self.oldVersion['parameters']
        generated['outputs'] = self.oldVersion['outputs']

        generated['resources'] = self.oldVersion['resources'].copy()

        for name, resource in self.newVersion['resources'].iteritems():
            type = resource['type']
            category = self.get_category(type, name)

            if category == 'Version':
                generated['resources'][name] = resource

            if category == 'Shared':
                if self.oldVersion['resources'][name] != self.newVersion['resources'][name]:
                    return 'Shared resource %s differs!' % name

            if category == 'Routing':
                pass

            if category == 'None':
                return 'Unsupported type/name combination found! type: %s name: %s' % (type, name)

        return generated


    def generateSecond(self):
        generated = {}
        generated['description'] = self.oldVersion['description']
        generated['heat_template_version'] = self.oldVersion['heat_template_version']

        # this needs to be enhanced at some point
        generated['parameters'] = self.oldVersion['parameters']
        generated['outputs'] = self.oldVersion['outputs']

        generated['resources'] = self.oldVersion['resources'].copy()

        for name, resource in self.newVersion['resources'].iteritems():
            type = resource['type']
            category = self.get_category(type, name)

            if category == 'Version':
                generated['resources'][name] = resource

            if category == 'Shared':
                if self.oldVersion['resources'][name] != self.newVersion['resources'][name]:
                    return 'Shared resource %s differs!' % name

            if category == 'Routing':
                generated['resources'][name] = resource

            if category == 'None':
                return 'Unsupported type/name combination found! type: %s name: %s' % (type, name)

        return generated


    def get_category(self, type, name):

        versioned = [
            "OS::Nova::Server",
            "OS::Neutron::Port"
        ]
        shared = [
            "OS::Heat::RandomString",
            "OS::Neutron::Net",
            "OS::Neutron::Subnet",
            "OS::Neutron::SecurityGroup",
            "OS::Neutron::Router",
            "OS::Neutron::RouterInterface",
            "OS::Neutron::Port",
            "OS::Nova::Server"
        ]
        routing = ["OS::Neutron::FloatingIP"]

        if type in versioned:
            if bool(versionRe.search(name)):
                return "Version"
        if type in shared:
            if bool(sharedRe.search(name)):
                return "Shared"
        if type in routing:
            if not bool(versionRe.search(name)) and not bool(sharedRe.search(name)):
                return "Routing"
        return "None"
