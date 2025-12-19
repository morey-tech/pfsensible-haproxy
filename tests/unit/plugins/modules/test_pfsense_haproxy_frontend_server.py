# Copyright: (c) 2025, Chris Morton <cosmo@cosmo.2y.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import pytest
import sys

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("pfSense Ansible modules require Python >= 2.7")

from xml.etree.ElementTree import fromstring, ElementTree
from ansible_collections.pfsensible.haproxy.plugins.modules import pfsense_haproxy_frontend_server
from ansible_collections.pfsensible.haproxy.plugins.module_utils.haproxy_frontend_server import (
    PFSenseHaproxyFrontendServerModule,
)
from ansible_collections.pfsensible.core.tests.unit.plugins.modules.pfsense_module import TestPFSenseModule

# Local fixture path for haproxy tests
HAPROXY_FIXTURE_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestPFSenseHaproxyFrontendServerModule(TestPFSenseModule):

    module = pfsense_haproxy_frontend_server

    def __init__(self, *args, **kwargs):
        super(TestPFSenseHaproxyFrontendServerModule, self).__init__(*args, **kwargs)
        self.config_file = 'pfsense_haproxy_frontend_server_config.xml'
        self.pfmodule = PFSenseHaproxyFrontendServerModule

    def load_fixtures(self):
        """ loading data from local haproxy fixtures """
        fixture_file = os.path.join(HAPROXY_FIXTURE_PATH, self.config_file)
        with open(fixture_file) as f:
            data = f.read()
        self.parse.return_value = ElementTree(fromstring(data))

    ##############
    # tests utils
    #
    def get_target_elt(self, obj, absent=False, module_result=None):
        """ get the generated frontend server xml definition """
        pkgs_elt = self.assert_find_xml_elt(self.xml_result, 'installedpackages')
        hap_elt = self.assert_find_xml_elt(pkgs_elt, 'haproxy')
        frontends_elt = self.assert_find_xml_elt(hap_elt, 'ha_backends')

        # Find the frontend
        for frontend_item in frontends_elt:
            name_elt = frontend_item.find('name')
            if name_elt is not None and name_elt.text == obj['frontend']:
                # Find the a_extaddr section
                a_extaddr = frontend_item.find('a_extaddr')
                if a_extaddr is None:
                    if not absent:
                        self.fail('a_extaddr not found in frontend ' + obj['frontend'])
                    return None

                # Find the server binding
                expected_name = "'{0}_{1}'".format(obj['extaddr'], obj['extaddr_port'])
                for item in a_extaddr:
                    item_name_elt = item.find('name')
                    if item_name_elt is not None and item_name_elt.text == expected_name:
                        return item

                if not absent:
                    self.fail('haproxy_frontend_server ' + expected_name + ' not found.')
                return None

        if not absent:
            self.fail('frontend ' + obj['frontend'] + ' not found.')
        return None

    def check_target_elt(self, obj, target_elt):
        """ test the xml definition of frontend server """
        if obj.get('extaddr'):
            self.assert_xml_elt_equal(target_elt, 'extaddr', obj['extaddr'])
        if obj.get('extaddr_port'):
            self.assert_xml_elt_equal(target_elt, 'extaddr_port', str(obj['extaddr_port']))
        if obj.get('extaddr_ssl'):
            self.assert_xml_elt_equal(target_elt, 'extaddr_ssl', obj['extaddr_ssl'])

    ##############
    # extaddr validation tests
    #
    def test_extaddr_standard_any_ipv4(self):
        """ test standard choice any_ipv4 is accepted """
        server = dict(frontend='test-frontend', extaddr='any_ipv4', extaddr_port=80)
        command = "create haproxy_frontend_server 'any_ipv4_80', extaddr='any_ipv4', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_standard_localhost_ipv4(self):
        """ test standard choice localhost_ipv4 is accepted """
        server = dict(frontend='test-frontend', extaddr='localhost_ipv4', extaddr_port=8080)
        command = "create haproxy_frontend_server 'localhost_ipv4_8080', extaddr='localhost_ipv4', extaddr_port=8080"
        self.do_module_test(server, command=command)

    def test_extaddr_standard_wan_ipv4(self):
        """ test standard choice wan_ipv4 is accepted """
        server = dict(frontend='test-frontend', extaddr='wan_ipv4', extaddr_port=80)
        command = "create haproxy_frontend_server 'wan_ipv4_80', extaddr='wan_ipv4', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_standard_lan_ipv4(self):
        """ test standard choice lan_ipv4 is accepted """
        server = dict(frontend='test-frontend', extaddr='lan_ipv4', extaddr_port=80)
        command = "create haproxy_frontend_server 'lan_ipv4_80', extaddr='lan_ipv4', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_standard_any_ipv6(self):
        """ test standard choice any_ipv6 is accepted """
        server = dict(frontend='test-frontend', extaddr='any_ipv6', extaddr_port=80)
        command = "create haproxy_frontend_server 'any_ipv6_80', extaddr='any_ipv6', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_standard_localhost_ipv6(self):
        """ test standard choice localhost_ipv6 is accepted """
        server = dict(frontend='test-frontend', extaddr='localhost_ipv6', extaddr_port=80)
        command = "create haproxy_frontend_server 'localhost_ipv6_80', extaddr='localhost_ipv6', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_interface_opt1_ipv4(self):
        """ test interface option opt1_ipv4 is accepted """
        server = dict(frontend='test-frontend', extaddr='opt1_ipv4', extaddr_port=80)
        command = "create haproxy_frontend_server 'opt1_ipv4_80', extaddr='opt1_ipv4', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_interface_opt2_ipv6(self):
        """ test interface option opt2_ipv6 is accepted """
        server = dict(frontend='test-frontend', extaddr='opt2_ipv6', extaddr_port=80)
        command = "create haproxy_frontend_server 'opt2_ipv6_80', extaddr='opt2_ipv6', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_interface_opt10_ipv4(self):
        """ test interface option with multi-digit number is accepted """
        server = dict(frontend='test-frontend', extaddr='opt10_ipv4', extaddr_port=80)
        command = "create haproxy_frontend_server 'opt10_ipv4_80', extaddr='opt10_ipv4', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_custom_ipv4(self):
        """ test custom IPv4 address is accepted """
        server = dict(frontend='test-frontend', extaddr='192.168.1.100', extaddr_port=80)
        command = "create haproxy_frontend_server '192.168.1.100_80', extaddr='192.168.1.100', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_custom_ipv4_any(self):
        """ test custom IPv4 address 0.0.0.0 is accepted """
        server = dict(frontend='test-frontend', extaddr='0.0.0.0', extaddr_port=80)
        command = "create haproxy_frontend_server '0.0.0.0_80', extaddr='0.0.0.0', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_custom_ipv6(self):
        """ test custom IPv6 address is accepted """
        server = dict(frontend='test-frontend', extaddr='2001:db8::1', extaddr_port=80)
        command = "create haproxy_frontend_server '2001:db8::1_80', extaddr='2001:db8::1', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_custom_ipv6_loopback(self):
        """ test custom IPv6 loopback address is accepted """
        server = dict(frontend='test-frontend', extaddr='::1', extaddr_port=80)
        command = "create haproxy_frontend_server '::1_80', extaddr='::1', extaddr_port=80"
        self.do_module_test(server, command=command)

    def test_extaddr_invalid_string(self):
        """ test invalid extaddr value is rejected """
        server = dict(frontend='test-frontend', extaddr='invalid_value', extaddr_port=80)
        msg = ("Invalid extaddr value 'invalid_value'. Must be one of: "
               "any_ipv4, localhost_ipv4, wan_ipv4, lan_ipv4, any_ipv6, localhost_ipv6, wan_ipv6, lan_ipv6, "
               "an interface option (opt<N>_ipv4 or opt<N>_ipv6), or a valid IPv4/IPv6 address.")
        self.do_module_test(server, msg=msg, failed=True)

    def test_extaddr_invalid_ip(self):
        """ test invalid IP address format is rejected """
        server = dict(frontend='test-frontend', extaddr='192.168.1.999', extaddr_port=80)
        msg = ("Invalid extaddr value '192.168.1.999'. Must be one of: "
               "any_ipv4, localhost_ipv4, wan_ipv4, lan_ipv4, any_ipv6, localhost_ipv6, wan_ipv6, lan_ipv6, "
               "an interface option (opt<N>_ipv4 or opt<N>_ipv6), or a valid IPv4/IPv6 address.")
        self.do_module_test(server, msg=msg, failed=True)

    def test_extaddr_invalid_interface_pattern(self):
        """ test invalid interface pattern is rejected """
        server = dict(frontend='test-frontend', extaddr='optX_ipv4', extaddr_port=80)
        msg = ("Invalid extaddr value 'optX_ipv4'. Must be one of: "
               "any_ipv4, localhost_ipv4, wan_ipv4, lan_ipv4, any_ipv6, localhost_ipv6, wan_ipv6, lan_ipv6, "
               "an interface option (opt<N>_ipv4 or opt<N>_ipv6), or a valid IPv4/IPv6 address.")
        self.do_module_test(server, msg=msg, failed=True)

    def test_frontend_server_delete(self):
        """ test deletion of a frontend server binding """
        server = dict(frontend='test-frontend', extaddr='wan_ipv4', extaddr_port=443)
        command = "delete haproxy_frontend_server 'wan_ipv4_443'"
        self.do_module_test(server, delete=True, command=command)
