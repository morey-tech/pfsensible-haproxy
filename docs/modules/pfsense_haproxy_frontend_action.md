# pfsense_haproxy_frontend_action

Manage pfSense HAProxy frontend actions

## Synopsis

- Manage pfSense HAProxy frontend actions for routing traffic based on ACL conditions.
- Actions define what happens when ACL conditions are met (e.g., route to a specific backend).

## Notes

- Actions reference ACLs by name. Create ACLs first using pfsense_haproxy_frontend_acl.
- Multiple ACL names can be specified (space-separated) to combine conditions with AND logic.

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| frontend | str | yes | - | - | The frontend name to add the action to. |
| action | str | yes | - | use_backend, custom | The action type to perform. |
| backend | str | no* | - | - | The backend pool name to route traffic to. Required when action=use_backend. |
| acl | str | no | - | - | Space-separated list of ACL names that must match for this action to execute. Multiple ACLs are combined with AND logic. Leave empty for unconditional action (default route). |
| custom_action | str | no* | - | - | Custom HAProxy directive to execute. Required when action=custom. |
| state | str | no | present | present, absent | State in which to leave the action. |

## Action Types

| Action | Description |
|--------|-------------|
| use_backend | Route traffic to a specific backend pool |
| custom | Execute a custom HAProxy directive |

## Examples

```yaml
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
```

## Complete SNI Routing Example

```yaml
# 1. Create HTTPS frontend (TCP mode for SNI routing)
- name: Create HTTPS frontend
  pfsensible.haproxy.pfsense_haproxy_frontend:
    name: sni-frontend
    type: https
    state: present

# 2. Add listener
- name: Add HTTPS listener
  pfsensible.haproxy.pfsense_haproxy_frontend_server:
    frontend: sni-frontend
    extaddr: 0.0.0.0
    extaddr_port: 443
    state: present

# 3. Add ACL for api.example.com
- name: ACL for api domain
  pfsensible.haproxy.pfsense_haproxy_frontend_acl:
    frontend: sni-frontend
    name: is_api
    expression: ssl_sni_matches
    value: api.example.com
    state: present

# 4. Add ACL for web.example.com
- name: ACL for web domain
  pfsensible.haproxy.pfsense_haproxy_frontend_acl:
    frontend: sni-frontend
    name: is_web
    expression: ssl_sni_matches
    value: web.example.com
    state: present

# 5. Route api to api-backend
- name: Route api traffic
  pfsensible.haproxy.pfsense_haproxy_frontend_action:
    frontend: sni-frontend
    action: use_backend
    backend: api-backend
    acl: is_api
    state: present

# 6. Route web to web-backend
- name: Route web traffic
  pfsensible.haproxy.pfsense_haproxy_frontend_action:
    frontend: sni-frontend
    action: use_backend
    backend: web-backend
    acl: is_web
    state: present
```

## Return Values

| Key | Type | Returned | Description | Sample |
|-----|------|----------|-------------|--------|
| commands | list | always | the set of commands that would be pushed to the remote device (if pfSense had a CLI) | `["create haproxy_frontend_action 'is_api' -> 'api-backend' on 'sni-frontend', action='use_backend', backend='api-backend', acl='is_api'", "delete haproxy_frontend_action 'is_api' -> 'api-backend' on 'sni-frontend'"]` |

## Author

- Nicholas Morey (@morey-tech)

## Version

Added in version 0.3.0
