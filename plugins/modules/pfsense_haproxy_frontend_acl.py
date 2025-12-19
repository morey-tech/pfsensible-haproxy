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
module: pfsense_haproxy_frontend_acl
version_added: 0.3.0
author: Chris Morton (@cosmosified)
short_description: Manage pfSense HAProxy frontend ACLs
description:
  - Manage pfSense HAProxy frontend Access Control Lists (ACLs) for SNI-based routing.
  - ACLs define conditions that can be used with actions to route traffic to different backends.
notes:
  - SNI-based ACLs require the frontend to be configured in 'https' or 'tcp' mode, not 'http'.
options:
  frontend:
    description: The frontend name to add the ACL to.
    required: true
    type: str
  name:
    description:
      - The ACL name.
      - This name is used to reference the ACL in actions.
      - ACLs with the same name are combined using OR logic.
    required: true
    type: str
  expression:
    description:
      - The ACL expression type for SNI matching.
      - C(ssl_sni_matches) - Exact match of the SNI hostname.
      - C(ssl_sni_contains) - SNI hostname contains the specified string.
      - C(ssl_sni_starts_with) - SNI hostname starts with the specified string.
      - C(ssl_sni_ends_with) - SNI hostname ends with the specified string.
      - C(ssl_sni_regex) - SNI hostname matches the specified regex pattern.
    required: true
    type: str
    choices:
      - ssl_sni_matches
      - ssl_sni_contains
      - ssl_sni_starts_with
      - ssl_sni_ends_with
      - ssl_sni_regex
  value:
    description: The value to match against (hostname, pattern, or regex).
    required: true
    type: str
  casesensitive:
    description: Enable case-sensitive matching.
    required: false
    type: bool
    default: false
  negate:
    description: Negate the match (match if condition is NOT met).
    required: false
    type: bool
    default: false
  state:
    description: State in which to leave the ACL.
    choices: [ "present", "absent" ]
    default: present
    type: str
"""

EXAMPLES = """
- name: Add ACL for exact SNI match
  pfsensible.haproxy.pfsense_haproxy_frontend_acl:
    frontend: sni-frontend
    name: is_api
    expression: ssl_sni_matches
    value: api.example.com
    state: present

- name: Add ACL for SNI ending with domain
  pfsensible.haproxy.pfsense_haproxy_frontend_acl:
    frontend: sni-frontend
    name: is_example_domain
    expression: ssl_sni_ends_with
    value: .example.com
    state: present

- name: Add case-sensitive ACL with regex
  pfsensible.haproxy.pfsense_haproxy_frontend_acl:
    frontend: sni-frontend
    name: is_versioned_api
    expression: ssl_sni_regex
    value: "api-v[0-9]+\\\\.example\\\\.com"
    casesensitive: true
    state: present

- name: Add negated ACL (match if NOT internal)
  pfsensible.haproxy.pfsense_haproxy_frontend_acl:
    frontend: sni-frontend
    name: not_internal
    expression: ssl_sni_ends_with
    value: .internal.local
    negate: true
    state: present

- name: Remove ACL
  pfsensible.haproxy.pfsense_haproxy_frontend_acl:
    frontend: sni-frontend
    name: is_api
    expression: ssl_sni_matches
    value: api.example.com
    state: absent
"""

RETURN = """
commands:
    description: the set of commands that would be pushed to the remote device (if pfSense had a CLI)
    returned: always
    type: list
    sample: [
        "create haproxy_frontend_acl 'is_api' on 'sni-frontend', expression='ssl_sni_matches', value='api.example.com'",
        "delete haproxy_frontend_acl 'is_api' on 'sni-frontend'"
    ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfsensible.haproxy.plugins.module_utils.haproxy_frontend_acl import (
    PFSenseHaproxyFrontendAclModule,
    HAPROXY_FRONTEND_ACL_ARGUMENT_SPEC
)


def main():
    module = AnsibleModule(
        argument_spec=HAPROXY_FRONTEND_ACL_ARGUMENT_SPEC,
        supports_check_mode=True)

    pfmodule = PFSenseHaproxyFrontendAclModule(module)
    pfmodule.run(module.params)
    pfmodule.commit_changes()


if __name__ == '__main__':
    main()
