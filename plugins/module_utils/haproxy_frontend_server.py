# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Chris Morton, cosmo@cosmo.2y.net
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
import re
import socket
from ansible_collections.pfsensible.core.plugins.module_utils.module_base import PFSenseModuleBase

# Standard pfSense address choices for external addresses
EXTADDR_STANDARD_CHOICES = [
    'any_ipv4',
    'localhost_ipv4',
    'wan_ipv4',
    'lan_ipv4',
    'any_ipv6',
    'localhost_ipv6',
    'wan_ipv6',
    'lan_ipv6',
]

# Pattern for interface-specific options: opt<digits>_ipv4 or opt<digits>_ipv6
EXTADDR_INTERFACE_PATTERN = re.compile(r'^opt\d+_ipv[46]$')

HAPROXY_FRONTEND_SERVER_ARGUMENT_SPEC = dict(
    state=dict(default='present', choices=['present', 'absent']),
    frontend=dict(required=True, type='str'),
    extaddr=dict(required=False, type='str'),
    extaddr_port=dict(required=False, type='int'),
    extaddr_ssl=dict(required=False, type='str'),
)


class PFSenseHaproxyFrontendServerModule(PFSenseModuleBase):
    """ module managing pfsense haproxy frontends """

    @staticmethod
    def get_argument_spec():
        """ return argument spec """
        return HAPROXY_FRONTEND_SERVER_ARGUMENT_SPEC

    ##############################
    # init
    #
    def __init__(self, module, pfsense=None):
        super(PFSenseHaproxyFrontendServerModule, self).__init__(module, pfsense)
        self.name = "pfsense_haproxy_frontend_server"
        self.root_elt = None
        self.obj = dict()

        pkgs_elt = self.pfsense.get_element('installedpackages')
        self.haproxy = pkgs_elt.find('haproxy') if pkgs_elt is not None else None
        self.frontends = self.haproxy.find('ha_backends') if self.haproxy is not None else None
        if self.frontends is None:
            self.module.fail_json(msg='Unable to find frontends (ha_backends) XML configuration entry. Are you sure haproxy is installed ?')

        self.frontend = None

    ##############################
    # params processing
    #
    def _params_to_obj(self):
        """ return a frontend dict from module params """
        obj = dict()
        self._get_ansible_param(obj, 'extaddr')
        self._get_ansible_param(obj, 'extaddr_port')
        self._get_ansible_param(obj, 'extaddr_ssl')
        obj['name'] = "'{0}_{1}'".format(self.params['extaddr'], self.params['extaddr_port'])

        return obj

    def _validate_extaddr(self, extaddr):
        """Validate the extaddr parameter value."""
        if extaddr is None:
            return  # Not provided, skip validation

        # Check standard choices
        if extaddr in EXTADDR_STANDARD_CHOICES:
            return

        # Check interface pattern (opt<N>_ipv4 or opt<N>_ipv6)
        if EXTADDR_INTERFACE_PATTERN.match(extaddr):
            return

        # Check if valid IPv4 address
        try:
            socket.inet_pton(socket.AF_INET, extaddr)
            return
        except socket.error:
            pass

        # Check if valid IPv6 address
        try:
            socket.inet_pton(socket.AF_INET6, extaddr)
            return
        except socket.error:
            pass

        # Invalid value
        self.module.fail_json(
            msg="Invalid extaddr value '{0}'. Must be one of: {1}, "
                "an interface option (opt<N>_ipv4 or opt<N>_ipv6), "
                "or a valid IPv4/IPv6 address.".format(
                    extaddr, ', '.join(EXTADDR_STANDARD_CHOICES)))

    def _validate_params(self):
        """ do some extra checks on input parameters """

        # validate extaddr value
        self._validate_extaddr(self.params.get('extaddr'))

        # get the frontend
        self.frontend = self._find_frontend(self.params['frontend'])
        if self.frontend is None:
            self.module.fail_json(msg="The frontend named '{0}' does not exist".format(self.params['frontend']))

        # setup the a_extaddr if we don't have it
        self.root_elt = self.frontend.find('a_extaddr')
        if self.root_elt is None:
            self.root_elt = self.pfsense.new_element('a_extaddr')
            self.frontend.append(self.root_elt)

    ##############################
    # XML processing
    #
    def _create_target(self):
        """ create the XML target_elt """
        server_elt = self.pfsense.new_element('item')
        return server_elt

    def _find_frontend(self, name):
        """ return the target frontend_elt if found """
        for item_elt in self.frontends:
            if item_elt.tag != 'item':
                continue
            name_elt = item_elt.find('name')
            if name_elt is not None and name_elt.text == name:
                return item_elt
        return None

    def _find_target(self):
        """ find the XML target_elt """
        for item_elt in self.root_elt:
            if item_elt.tag != 'item':
                continue
            name_elt = item_elt.find('name')
            if name_elt is not None and name_elt.text == self.obj['name']:
                return item_elt
        return None

    def _get_next_id(self):
        """ get next free haproxy id  """
        max_id = 99
        id_elts = self.haproxy.findall('.//id')
        for id_elt in id_elts:
            if id_elt.text is None:
                continue
            ha_id = int(id_elt.text)
            if ha_id > max_id:
                max_id = ha_id
        return str(max_id + 1)

    ##############################
    # run
    #
    def _update(self):
        """ make the target pfsense reload haproxy """
        return self.pfsense.phpshell('''require_once("haproxy/haproxy.inc");
$result = haproxy_check_and_run($savemsg, true); if ($result) unlink_if_exists($d_haproxyconfdirty_path);''')

    ##############################
    # Logging
    #
    def _log_fields(self, before=None):
        """ generate pseudo-CLI command fields parameters to create an obj """
        values = ''
        if before is None:
            values += self.format_cli_field(self.params, 'extaddr')
            values += self.format_cli_field(self.params, 'extaddr_port')
            values += self.format_cli_field(self.params, 'extaddr_ssl')
        else:
            values += self.format_updated_cli_field(self.obj, before, 'extaddr', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'extaddr_port', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'extaddr_ssl', add_comma=(values))
        return values

    def _get_obj_name(self):
        """ return obj's name """
        return "'{0}_{1}'".format(self.obj['extaddr'], self.obj['extaddr_port'])
