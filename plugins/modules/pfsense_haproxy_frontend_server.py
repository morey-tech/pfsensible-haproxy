#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Chris Morton <cosmo@cosmo.2y.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: pfsense_haproxy_frontend_server
version_added: 0.2.0
author: Chris Morton (@cosmosified)
short_description: Manage pfSense HAProxy frontend servers
description:
  - Manage pfSense HAProxy frontend bind addresses/ports
notes:
options:
  frontend:
    description: The frontend name.
    required: true
    type: str
  extaddr:
    description: External address to bind to.
    required: false
    type: str
  extaddr_port:
    description: External port to bind to.
    required: false
    type: int
  extaddr_ssl:
    description: SSL configuration for external address.
    required: false
    type: str
  state:
    description: State in which to leave the frontend server
    choices: [ "present", "absent" ]
    default: present
    type: str
"""

EXAMPLES = """
- name: Add frontend server binding
  pfsensible.haproxy.pfsense_haproxy_frontend_server:
    frontend: web-frontend
    extaddr: 0.0.0.0
    extaddr_port: 443
    extaddr_ssl: "yes"
    state: present

- name: Remove frontend server binding
  pfsensible.haproxy.pfsense_haproxy_frontend_server:
    frontend: web-frontend
    extaddr: 0.0.0.0
    extaddr_port: 443
    state: absent
"""

RETURN = """
commands:
    description: the set of commands that would be pushed to the remote device (if pfSense had a CLI)
    returned: always
    type: list
    sample: [
        "create haproxy_frontend_server '0.0.0.0_443' on 'web-frontend', extaddr='0.0.0.0', port=443",
        "delete haproxy_frontend_server '0.0.0.0_443' on 'web-frontend'"
    ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfsensible.haproxy.plugins.module_utils.haproxy_frontend_server import (
    PFSenseHaproxyFrontendServerModule,
    HAPROXY_FRONTEND_SERVER_ARGUMENT_SPEC
)


def main():
    module = AnsibleModule(
        argument_spec=HAPROXY_FRONTEND_SERVER_ARGUMENT_SPEC,
        supports_check_mode=True)

    pfmodule = PFSenseHaproxyFrontendServerModule(module)
    pfmodule.run(module.params)
    pfmodule.commit_changes()


if __name__ == '__main__':
    main()
