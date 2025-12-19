# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Chris Morton, cosmo@cosmo.2y.net
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.pfsensible.core.plugins.module_utils.module_base import PFSenseModuleBase

HAPROXY_FRONTEND_ACTION_ARGUMENT_SPEC = dict(
    state=dict(default='present', choices=['present', 'absent']),
    frontend=dict(required=True, type='str'),
    action=dict(required=True, type='str', choices=['use_backend', 'custom']),
    backend=dict(required=False, type='str'),
    acl=dict(required=False, type='str'),
    custom_action=dict(required=False, type='str'),
)


class PFSenseHaproxyFrontendActionModule(PFSenseModuleBase):
    """ module managing pfsense haproxy frontend actions """

    @staticmethod
    def get_argument_spec():
        """ return argument spec """
        return HAPROXY_FRONTEND_ACTION_ARGUMENT_SPEC

    ##############################
    # init
    #
    def __init__(self, module, pfsense=None):
        super(PFSenseHaproxyFrontendActionModule, self).__init__(module, pfsense)
        self.name = "pfsense_haproxy_frontend_action"
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
        """ return an action dict from module params """
        obj = dict()
        obj['action'] = self.params['action']

        # Handle action-specific fields
        if self.params['action'] == 'use_backend':
            if self.params.get('backend'):
                obj['use_backendbackend'] = self.params['backend']
        elif self.params['action'] == 'custom':
            if self.params.get('custom_action'):
                obj['customcustomaction'] = self.params['custom_action']

        # ACL condition (space-separated ACL names)
        if self.params.get('acl'):
            obj['acl'] = self.params['acl']
        else:
            obj['acl'] = ''

        return obj

    def _validate_params(self):
        """ do some extra checks on input parameters """

        # get the frontend
        self.frontend = self._find_frontend(self.params['frontend'])
        if self.frontend is None:
            self.module.fail_json(msg="The frontend named '{0}' does not exist".format(self.params['frontend']))

        # Validate action-specific required fields
        if self.params['action'] == 'use_backend':
            if not self.params.get('backend'):
                self.module.fail_json(msg="Parameter 'backend' is required when action is 'use_backend'")
        elif self.params['action'] == 'custom':
            if not self.params.get('custom_action'):
                self.module.fail_json(msg="Parameter 'custom_action' is required when action is 'custom'")

        # setup the a_actionitems container if we don't have it
        self.root_elt = self.frontend.find('a_actionitems')
        if self.root_elt is None:
            self.root_elt = self.pfsense.new_element('a_actionitems')
            self.frontend.append(self.root_elt)

    ##############################
    # XML processing
    #
    def _create_target(self):
        """ create the XML target_elt """
        action_elt = self.pfsense.new_element('item')
        return action_elt

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
        """ find the XML target_elt by action type and backend/custom_action """
        for item_elt in self.root_elt:
            if item_elt.tag != 'item':
                continue

            action_elt = item_elt.find('action')
            if action_elt is None or action_elt.text != self.obj['action']:
                continue

            # For use_backend, also match by backend name
            if self.obj['action'] == 'use_backend':
                backend_elt = item_elt.find('use_backendbackend')
                if backend_elt is not None and backend_elt.text == self.obj.get('use_backendbackend'):
                    # Also check ACL matches
                    acl_elt = item_elt.find('acl')
                    acl_text = acl_elt.text if acl_elt is not None else ''
                    if acl_text == self.obj.get('acl', ''):
                        return item_elt
            # For custom, match by custom action
            elif self.obj['action'] == 'custom':
                custom_elt = item_elt.find('customcustomaction')
                if custom_elt is not None and custom_elt.text == self.obj.get('customcustomaction'):
                    acl_elt = item_elt.find('acl')
                    acl_text = acl_elt.text if acl_elt is not None else ''
                    if acl_text == self.obj.get('acl', ''):
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
            values += self.format_cli_field(self.params, 'action')
            values += self.format_cli_field(self.params, 'backend')
            values += self.format_cli_field(self.params, 'acl')
            values += self.format_cli_field(self.params, 'custom_action')
        else:
            values += self.format_updated_cli_field(self.obj, before, 'action', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'use_backendbackend', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'acl', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'customcustomaction', add_comma=(values))
        return values

    def _get_obj_name(self):
        """ return obj's name """
        if self.obj['action'] == 'use_backend':
            return "'{0}' -> '{1}'".format(self.obj.get('acl', 'default'), self.obj.get('use_backendbackend', ''))
        elif self.obj['action'] == 'custom':
            return "'{0}' -> custom".format(self.obj.get('acl', 'default'))
        return "'{0}'".format(self.obj['action'])
