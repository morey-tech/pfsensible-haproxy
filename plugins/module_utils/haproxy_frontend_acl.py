# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nicholas Morey, nicholas@morey.tech
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.pfsensible.core.plugins.module_utils.module_base import PFSenseModuleBase

HAPROXY_FRONTEND_ACL_ARGUMENT_SPEC = dict(
    state=dict(default='present', choices=['present', 'absent']),
    frontend=dict(required=True, type='str'),
    name=dict(required=True, type='str'),
    expression=dict(
        required=True,
        type='str',
        choices=[
            'ssl_sni_matches',
            'ssl_sni_contains',
            'ssl_sni_starts_with',
            'ssl_sni_ends_with',
            'ssl_sni_regex',
        ]
    ),
    value=dict(required=True, type='str'),
    casesensitive=dict(required=False, type='bool', default=False),
    negate=dict(required=False, type='bool', default=False),
)


class PFSenseHaproxyFrontendAclModule(PFSenseModuleBase):
    """ module managing pfsense haproxy frontend ACLs """

    @staticmethod
    def get_argument_spec():
        """ return argument spec """
        return HAPROXY_FRONTEND_ACL_ARGUMENT_SPEC

    ##############################
    # init
    #
    def __init__(self, module, pfsense=None):
        super(PFSenseHaproxyFrontendAclModule, self).__init__(module, pfsense)
        self.name = "pfsense_haproxy_frontend_acl"
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
        """ return an ACL dict from module params """
        obj = dict()
        obj['name'] = self.params['name']
        self._get_ansible_param(obj, 'expression')
        self._get_ansible_param(obj, 'value')

        # Handle boolean fields - pfSense uses empty string or 'yes'
        if self.params.get('casesensitive'):
            obj['casesensitive'] = 'yes'
        else:
            obj['casesensitive'] = ''

        if self.params.get('negate'):
            obj['not'] = 'yes'
        else:
            obj['not'] = ''

        return obj

    def _validate_params(self):
        """ do some extra checks on input parameters """

        # get the frontend
        self.frontend = self._find_frontend(self.params['frontend'])
        if self.frontend is None:
            self.module.fail_json(msg="The frontend named '{0}' does not exist".format(self.params['frontend']))

        # Validate frontend type - SNI ACLs require https or tcp mode
        frontend_type = self.frontend.find('type')
        if frontend_type is not None and frontend_type.text == 'http':
            self.module.fail_json(
                msg="SNI-based ACLs (ssl_sni_*) require frontend type 'https' or 'tcp', not 'http'. "
                    "Frontend '{0}' is configured as type 'http'.".format(self.params['frontend'])
            )

        # setup the a_acl container if we don't have it
        self.root_elt = self.frontend.find('a_acl')
        if self.root_elt is None:
            self.root_elt = self.pfsense.new_element('a_acl')
            self.frontend.append(self.root_elt)

    ##############################
    # XML processing
    #
    def _create_target(self):
        """ create the XML target_elt """
        acl_elt = self.pfsense.new_element('item')
        return acl_elt

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
        """ find the XML target_elt by ACL name """
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
            values += self.format_cli_field(self.params, 'name')
            values += self.format_cli_field(self.params, 'expression')
            values += self.format_cli_field(self.params, 'value')
            values += self.format_cli_field(self.params, 'casesensitive')
            values += self.format_cli_field(self.params, 'negate')
        else:
            values += self.format_updated_cli_field(self.obj, before, 'name', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'expression', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'value', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'casesensitive', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'not', add_comma=(values))
        return values

    def _get_obj_name(self):
        """ return obj's name """
        return "'{0}'".format(self.obj['name'])
