__author__ = 'merne'

import yaml
import unittest

from migrationTemplateGenerator import migrationTemplateGenerator

class TestMigrationTemplateGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = migrationTemplateGenerator('./tests/files/test_v1.yaml', './tests/files/test_v2.yaml')


    def test_generate(self):


        with open("./tests/files/test_v2.yaml") as stream:
            expected = yaml.load(stream)

        generated = self.generator.generateAll()[3]
        self.assertEqual(generated, expected, 'generated file does not match expected value')

    def test_get_category(self):

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

        none = ["foobar"]

        for resourceType in versioned:
            self.assertEqual(self.generator.get_category(resourceType, "v1_foobar"), "Version")
            self.assertEqual(self.generator.get_category(resourceType, "v2_foobar"), "Version")
            self.assertEqual(self.generator.get_category(resourceType, "v9999999999_foobar"), "Version")
            self.assertEqual(self.generator.get_category(resourceType, "V1_foobar"), "Version")
            self.assertEqual(self.generator.get_category(resourceType, "V9999999999_foobar"), "Version")
            self.assertEqual(self.generator.get_category(resourceType, "v1_"), "None")
            self.assertEqual(self.generator.get_category(resourceType, "foobar"), "None")

        for resourceType in shared:
            self.assertEqual(self.generator.get_category(resourceType, "shared_foobar"), "Shared")
            self.assertEqual(self.generator.get_category(resourceType, "v1_"), "None")
            self.assertEqual(self.generator.get_category(resourceType, "V1_"), "None")
            self.assertEqual(self.generator.get_category(resourceType, "shared_"), "None")

        for resourceType in routing:
            self.assertEqual(self.generator.get_category(resourceType, "foobar"), "Routing")
            self.assertEqual(self.generator.get_category(resourceType, "v1_foobar"), "None")
            self.assertEqual(self.generator.get_category(resourceType, "V1_foobar"), "None")
            self.assertEqual(self.generator.get_category(resourceType, "shared_foobar"), "None")

        for resourceType in none:
            self.assertEqual(self.generator.get_category(resourceType, "foobar"), "None")
            self.assertEqual(self.generator.get_category(resourceType, "v1_foobar"), "None")
            self.assertEqual(self.generator.get_category(resourceType, "V1_foobar"), "None")
            self.assertEqual(self.generator.get_category(resourceType, "shared_"), "None")

    def test_generate_first(self):
        with open("./tests/files/test_v1_v2.yaml") as stream:
            expected = yaml.load(stream)

        generated = self.generator.generateFirst()
        self.assertEqual(generated, expected)

    def test_generate_first_for_failure(self):
        self.generator.newVersion['resources']['shared_private_subnet']['foo'] = 'bar'
        generated = self.generator.generateFirst()
        self.assertEqual(generated, 'Shared resource %s differs!' % 'shared_private_subnet')
        del self.generator.newVersion['resources']['shared_private_subnet']['foo']
        self.generator.newVersion['resources']['shared_private_subnet']['type'] = "OS::Foo::Bar"
        generated = self.generator.generateFirst()
        self.assertEqual(generated, 'Unsupported type/name combination found! type: %s name: %s' % ("OS::Foo::Bar", 'shared_private_subnet'))


    def test_generate_second(self):
        with open("./tests/files/test_v2_v1.yaml") as stream:
            expected = yaml.load(stream)

        generated = self.generator.generateSecond()
        self.assertEqual(generated, expected)


    def test_generate_second_for_failure(self):
        self.generator.newVersion['resources']['shared_private_subnet']['foo'] = 'bar'
        generated = self.generator.generateSecond()
        self.assertEqual(generated, 'Shared resource %s differs!' % 'shared_private_subnet')
        del self.generator.newVersion['resources']['shared_private_subnet']['foo']
        self.generator.newVersion['resources']['shared_private_subnet']['type'] = "OS::Foo::Bar"
        generated = self.generator.generateSecond()
        self.assertEqual(generated, 'Unsupported type/name combination found! type: %s name: %s' % ("OS::Foo::Bar", 'shared_private_subnet'))


