# pfsense_haproxy_frontend_server

Manage pfSense HAProxy frontend servers

## Synopsis

- Manage pfSense HAProxy frontend bind addresses/ports

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| frontend | str | yes | - | - | The frontend name. |
| extaddr | str | no | - | - | External address to bind to. |
| extaddr_port | int | no | - | - | External port to bind to. |
| extaddr_ssl | str | no | - | - | SSL configuration for external address. |
| state | str | no | present | present, absent | State in which to leave the frontend server |

## Examples

```yaml
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
```

## Return Values

| Key | Type | Returned | Description | Sample |
|-----|------|----------|-------------|--------|
| commands | list | always | the set of commands that would be pushed to the remote device (if pfSense had a CLI) | `["create haproxy_frontend_server '0.0.0.0_443' on 'web-frontend', extaddr='0.0.0.0', port=443", "delete haproxy_frontend_server '0.0.0.0_443' on 'web-frontend'"]` |

## Author

- Chris Morton (@cosmosified)

## Version

Added in version 0.2.0
