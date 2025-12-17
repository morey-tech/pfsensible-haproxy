# pfsense_haproxy_backend

Manage pfSense HAProxy backends

## Synopsis

- Manage pfSense HAProxy backends

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| name | str | yes | - | - | The backend name. |
| balance | str | no | none | none, roundrobin, static-rr, leastconn, source, uri | The load balancing option. Note that `uri` option is only meaningful when used with HTTP/HTTPS frontends. |
| balance_urilen | int | no | - | - | Indicates that the algorithm should only consider that many characters at the beginning of the URI to compute the hash. |
| balance_uridepth | int | no | - | - | Indicates the maximum directory depth to be used to compute the hash. One level is counted for each slash in the request. |
| balance_uriwhole | bool | no | - | - | Allow using whole URI including url parameters behind a question mark. |
| connection_timeout | int | no | - | - | The time (in milliseconds) we give up if the connection does not complete within (default 30000). |
| server_timeout | int | no | - | - | The time (in milliseconds) we accept to wait for data from the server, or for the server to accept data (default 30000). |
| retries | int | no | - | - | After a connection failure to a server, it is possible to retry, potentially on another server. |
| check_type | str | no | none | none, Basic, HTTP, Agent, LDAP, MySQL, PostgreSQL, Redis, SMTP, ESMTP, SSL | Health check method. |
| check_frequency | int | no | - | - | The check interval (in milliseconds). For HTTP/HTTPS defaults to 1000 if left blank. For TCP no check will be performed if left empty. |
| log_checks | bool | no | - | - | When this option is enabled, any change of the health check status or to the server's health will be logged. |
| httpcheck_method | str | no | - | OPTIONS, HEAD, GET, POST, PUT, DELETE, TRACE | HTTP check method. Only relevant when used with HTTP/HTTPS frontends and `check_type=HTTP`. OPTIONS is the method usually best to perform server checks. |
| monitor_uri | str | no | - | - | URL used by HTTP check requests. Only relevant when used with HTTP/HTTPS frontends and `check_type=HTTP`. |
| monitor_httpversion | str | no | - | - | Defaults to "HTTP/1.0" if left blank. |
| monitor_username | str | no | - | - | Username used in checks (MySQL and PostgreSQL) |
| monitor_domain | str | no | - | - | Domain used in checks (SMTP and ESMTP) |
| state | str | no | present | present, absent | State in which to leave the backend |

## Examples

```yaml
- name: Add HTTP backend with HTTP health checks
  pfsensible.haproxy.pfsense_haproxy_backend:
    name: web-backend
    balance: roundrobin
    check_type: HTTP
    httpcheck_method: OPTIONS
    monitor_uri: /health
    state: present

- name: Add TCP backend for MySQL with basic health checks
  pfsensible.haproxy.pfsense_haproxy_backend:
    name: mysql-backend
    balance: leastconn
    check_type: Basic
    check_frequency: 2000
    state: present

- name: Add TCP backend with SSL health checks
  pfsensible.haproxy.pfsense_haproxy_backend:
    name: redis-backend
    balance: roundrobin
    check_type: SSL
    check_frequency: 1000
    state: present

- name: Remove backend
  pfsensible.haproxy.pfsense_haproxy_backend:
    name: exchange
    state: absent
```

## Return Values

| Key | Type | Returned | Description | Sample |
|-----|------|----------|-------------|--------|
| commands | list | always | the set of commands that would be pushed to the remote device (if pfSense had a CLI) | `["create haproxy_backend 'exchange', balance='leastconn', httpcheck_method='OPTIONS'", "delete haproxy_backend 'exchange'"]` |

## Author

- Frederic Bor (@f-bor)

## Version

Added in version 0.1.0
