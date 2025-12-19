# pfsense_haproxy_frontend_server

Manage pfSense HAProxy frontend servers

## Synopsis

- Manage pfSense HAProxy frontend bind addresses/ports

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| frontend | str | yes | - | - | The frontend name. |
| extaddr | str | no | - | See description | External address to bind to. Can be a standard pfSense address option, an interface-specific option, or a custom IP address. Standard options: `any_ipv4`, `localhost_ipv4`, `wan_ipv4`, `lan_ipv4`, `any_ipv6`, `localhost_ipv6`, `wan_ipv6`, `lan_ipv6`. Interface options: `opt<N>_ipv4` or `opt<N>_ipv6` where N is the interface number (e.g., `opt1_ipv4`, `opt2_ipv6`). Custom addresses: Any valid IPv4 or IPv6 address. |
| extaddr_port | int | no | - | - | External port to bind to. |
| extaddr_ssl | str | no | - | - | SSL configuration for external address. |
| state | str | no | present | present, absent | State in which to leave the frontend server |

## Examples

```yaml
- name: Add frontend server binding with custom IPv4 address
  pfsensible.haproxy.pfsense_haproxy_frontend_server:
    frontend: web-frontend
    extaddr: 192.168.1.100
    extaddr_port: 443
    extaddr_ssl: "yes"
    state: present

- name: Bind to any IPv4 address
  pfsensible.haproxy.pfsense_haproxy_frontend_server:
    frontend: web-frontend
    extaddr: any_ipv4
    extaddr_port: 80
    state: present

- name: Bind to WAN interface address
  pfsensible.haproxy.pfsense_haproxy_frontend_server:
    frontend: web-frontend
    extaddr: wan_ipv4
    extaddr_port: 443
    extaddr_ssl: "yes"
    state: present

- name: Bind to optional interface (e.g., LAB network)
  pfsensible.haproxy.pfsense_haproxy_frontend_server:
    frontend: internal-frontend
    extaddr: opt1_ipv4
    extaddr_port: 8080
    state: present

- name: Bind to IPv6 address
  pfsensible.haproxy.pfsense_haproxy_frontend_server:
    frontend: web-frontend
    extaddr: any_ipv6
    extaddr_port: 443
    state: present

- name: Remove frontend server binding
  pfsensible.haproxy.pfsense_haproxy_frontend_server:
    frontend: web-frontend
    extaddr: wan_ipv4
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
