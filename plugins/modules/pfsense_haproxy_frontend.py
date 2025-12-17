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
module: pfsense_haproxy_frontend
version_added: 0.2.0
author: Chris Morton (@cosmosified)
short_description: Manage pfSense HAProxy frontends
description:
  - Manage pfSense HAProxy frontends
notes:
options:
  name:
    description: The frontend name.
    required: true
    type: str
  status:
    description: Frontend status (enabled/disabled).
    required: false
    type: str
  desc:
    description: Frontend description.
    required: false
    type: str
  type:
    description:
      - Frontend type/mode.
      - C(http) - HTTP / HTTPS with offloading (SSL termination).
      - C(https) - SSL / HTTPS (TCP mode) for SNI-based routing.
      - C(tcp) - Plain TCP proxying for non-HTTP protocols.
    required: false
    type: str
    choices: ['http', 'https', 'tcp']
    default: 'http'
  httpclose:
    description:
      - HTTP close mode for connection handling.
      - Only valid for C(http) type frontends.
    required: false
    type: str
    choices: ['http-keep-alive']
    default: 'http-keep-alive'
  backend_serverpool:
    description: Backend server pool to use.
    required: false
    type: str
  ssloffloadcert:
    description: SSL certificate for offloading.
    required: false
    type: str
  ssloffloadcert_type_search:
    description: Field type to search for SSL certificate.
    required: false
    type: str
    default: 'descr'
  ssloffloadacl_an:
    description: SSL ACL alternative names.
    required: false
    type: str
  max_connections:
    description: Maximum number of connections.
    required: false
    type: int
    default: 100
  addhttp_https_redirect:
    description:
      - Add HTTP to HTTPS redirect rule.
      - Only valid for C(http) type frontends.
    required: false
    type: bool
  state:
    description: State in which to leave the frontend
    choices: [ "present", "absent" ]
    default: present
    type: str
"""

EXAMPLES = """
- name: Add HTTP frontend with SSL offloading
  pfsensible.haproxy.pfsense_haproxy_frontend:
    name: web-frontend
    desc: "HTTP frontend with SSL termination"
    status: active
    type: http
    httpclose: http-keep-alive
    ssloffloadcert: my-certificate
    backend_serverpool: web-backend
    state: present

- name: Add HTTPS frontend (TCP mode) for SNI routing
  pfsensible.haproxy.pfsense_haproxy_frontend:
    name: sni-frontend
    desc: "HTTPS in TCP mode for SNI-based routing"
    status: active
    type: https
    backend_serverpool: secure-backend
    state: present

- name: Add TCP frontend for MySQL load balancing
  pfsensible.haproxy.pfsense_haproxy_frontend:
    name: mysql-frontend
    desc: "MySQL TCP Load Balancer"
    status: active
    type: tcp
    backend_serverpool: mysql-backend
    max_connections: 500
    state: present

- name: Add TCP frontend for Redis
  pfsensible.haproxy.pfsense_haproxy_frontend:
    name: redis-frontend
    desc: "Redis TCP proxy"
    status: active
    type: tcp
    backend_serverpool: redis-backend
    state: present

- name: Remove frontend
  pfsensible.haproxy.pfsense_haproxy_frontend:
    name: web-frontend
    state: absent
"""

RETURN = """
commands:
    description: the set of commands that would be pushed to the remote device (if pfSense had a CLI)
    returned: always
    type: list
    sample: ["create haproxy_frontend 'web-frontend', desc='Web frontend', type='https'", "delete haproxy_frontend 'web-frontend'"]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfsensible.haproxy.plugins.module_utils.haproxy_frontend import (
    PFSenseHaproxyFrontendModule,
    HAPROXY_FRONTEND_ARGUMENT_SPEC
)


def main():
    module = AnsibleModule(
        argument_spec=HAPROXY_FRONTEND_ARGUMENT_SPEC,
        supports_check_mode=True)

    pfmodule = PFSenseHaproxyFrontendModule(module)
    pfmodule.run(module.params)
    pfmodule.commit_changes()


if __name__ == '__main__':
    main()
