# pfsense_haproxy_frontend

Manage pfSense HAProxy frontends

## Synopsis

- Manage pfSense HAProxy frontends

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| name | str | yes | - | - | The frontend name. |
| status | str | no | - | - | Frontend status (enabled/disabled). |
| desc | str | no | - | - | Frontend description. |
| type | str | no | http | http, https, tcp | Frontend type/mode. `http` - HTTP/HTTPS with offloading (SSL termination); `https` - SSL/HTTPS (TCP mode) for SNI-based routing; `tcp` - Plain TCP proxying for non-HTTP protocols. |
| httpclose | str | no | - | http-keep-alive | HTTP close mode for connection handling. Only valid for `http` type frontends. Defaults to `http-keep-alive` when `type=http` and not specified. |
| backend_serverpool | str | no | - | - | Backend server pool to use. |
| ssloffloadcert | str | no | - | - | SSL certificate for offloading. |
| ssloffloadcert_type_search | str | no | descr | - | Field type to search for SSL certificate. |
| ssloffloadacl_an | str | no | - | - | SSL ACL alternative names. |
| max_connections | int | no | 100 | - | Maximum number of connections. |
| addhttp_https_redirect | bool | no | - | - | Add HTTP to HTTPS redirect rule. Only valid for `http` type frontends. |
| state | str | no | present | present, absent | State in which to leave the frontend |

## Examples

```yaml
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

- name: Remove frontend
  pfsensible.haproxy.pfsense_haproxy_frontend:
    name: web-frontend
    state: absent
```

## Return Values

| Key | Type | Returned | Description | Sample |
|-----|------|----------|-------------|--------|
| commands | list | always | the set of commands that would be pushed to the remote device (if pfSense had a CLI) | `["create haproxy_frontend 'web-frontend', desc='Web frontend', type='https'", "delete haproxy_frontend 'web-frontend'"]` |

## Author

- Chris Morton (@cosmosified)

## Version

Added in version 0.2.0
