#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nicholas Morey <nicholas@morey.tech>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: pfsense_haproxy_frontend_action
version_added: 0.3.0
author: Nicholas Morey (@morey-tech)
short_description: Manage pfSense HAProxy frontend actions
description:
  - Manage pfSense HAProxy frontend actions for routing traffic based on ACL conditions.
  - Actions define what happens when ACL conditions are met (e.g., route to a specific backend).
notes:
  - Actions reference ACLs by name. Create ACLs first using pfsense_haproxy_frontend_acl.
  - Multiple ACL names can be specified (space-separated) to combine conditions with AND logic.
options:
  frontend:
    description: The frontend name to add the action to.
    required: true
    type: str
  action:
    description:
      - The action type to perform.
      - C(use_backend) - Route traffic to a specific backend pool.
      - C(custom) - Execute a custom HAProxy directive.
    required: true
    type: str
    choices:
      - use_backend
      - custom
  backend:
    description:
      - The backend pool name to route traffic to.
      - Required when I(action=use_backend).
    required: false
    type: str
  acl:
    description:
      - Space-separated list of ACL names that must match for this action to execute.
      - Multiple ACLs are combined with AND logic.
      - Leave empty for unconditional action (default route).
    required: false
    type: str
  custom_action:
    description:
      - Custom HAProxy directive to execute.
      - Required when I(action=custom).
    required: false
    type: str
  state:
    description: State in which to leave the action.
    choices: [ "present", "absent" ]
    default: present
    type: str
"""

EXAMPLES = """
- name: Route traffic to api-backend when is_api ACL matches
  pfsensible.haproxy.pfsense_haproxy_frontend_action:
    frontend: sni-frontend
    action: use_backend
    backend: api-backend
    acl: is_api
    state: present

- name: Route traffic to web-backend when multiple ACLs match (AND logic)
  pfsensible.haproxy.pfsense_haproxy_frontend_action:
    frontend: sni-frontend
    action: use_backend
    backend: web-backend
    acl: "is_web is_authenticated"
    state: present

- name: Set default backend (no ACL condition)
  pfsensible.haproxy.pfsense_haproxy_frontend_action:
    frontend: sni-frontend
    action: use_backend
    backend: default-backend
    state: present

- name: Add custom action
  pfsensible.haproxy.pfsense_haproxy_frontend_action:
    frontend: sni-frontend
    action: custom
    custom_action: "tcp-request content reject"
    acl: is_blocked
    state: present

- name: Remove action
  pfsensible.haproxy.pfsense_haproxy_frontend_action:
    frontend: sni-frontend
    action: use_backend
    backend: api-backend
    acl: is_api
    state: absent
"""

RETURN = """
commands:
    description: the set of commands that would be pushed to the remote device (if pfSense had a CLI)
    returned: always
    type: list
    sample: [
        "create haproxy_frontend_action 'is_api' -> 'api-backend' on 'sni-frontend', action='use_backend', backend='api-backend', acl='is_api'",
        "delete haproxy_frontend_action 'is_api' -> 'api-backend' on 'sni-frontend'"
    ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfsensible.haproxy.plugins.module_utils.haproxy_frontend_action import (
    PFSenseHaproxyFrontendActionModule,
    HAPROXY_FRONTEND_ACTION_ARGUMENT_SPEC
)


def main():
    module = AnsibleModule(
        argument_spec=HAPROXY_FRONTEND_ACTION_ARGUMENT_SPEC,
        supports_check_mode=True)

    pfmodule = PFSenseHaproxyFrontendActionModule(module)
    pfmodule.run(module.params)
    pfmodule.commit_changes()


if __name__ == '__main__':
    main()
