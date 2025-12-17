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
| type | str | no | http | http, https | Frontend type. |
| httpclose | str | no | http-keep-alive | http-keep-alive | HTTP close mode. |
| backend_serverpool | str | no | - | - | Backend server pool to use. |
| ssloffloadcert | str | no | - | - | SSL certificate for offloading. |
| ssloffloadcert_type_search | str | no | descr | - | Field type to search for SSL certificate. |
| ssloffloadacl_an | str | no | - | - | SSL ACL alternative names. |
| max_connections | int | no | 100 | - | Maximum number of connections. |
| addhttp_https_redirect | bool | no | - | - | Add HTTP to HTTPS redirect rule. |
| state | str | no | present | present, absent | State in which to leave the frontend |

## Examples

```yaml
- name: Add frontend
  pfsensible.haproxy.pfsense_haproxy_frontend:
    name: web-frontend
    desc: "Web frontend"
    status: active
    type: https
    backend_serverpool: web-backend
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
