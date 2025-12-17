# pfsense_haproxy_backend_server

Manage pfSense haproxy backend servers

## Synopsis

- Manage pfSense haproxy servers

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| backend | str | yes | - | - | The backend name. |
| name | str | yes | - | - | The server name. |
| mode | str | no | active | active, backup, disabled, inactive | How to use the server. |
| forwardto | str | no | - | - | The name of the frontend to forward. When None, forwards to address and port |
| address | str | no | - | - | IP or hostname of the backend (only resolved on start-up.) |
| port | int | no | - | - | The port of the backend. |
| ssl | bool | no | - | - | Should haproxy encrypt the traffic to the backend with SSL (commonly used with mode http on frontend and a port 443 on backend). |
| checkssl | bool | no | - | - | This can be used with for example a LDAPS health-checks where LDAPS is passed along with mode TCP |
| weight | int | no | - | - | A weight between 0 and 256, this setting can be used when multiple servers on different hardware need to be balanced with a different part the traffic. A server with weight 0 wont get new traffic. Default if empty: 1 |
| sslserververify | bool | no | - | - | SSL servers only, The server certificate will be verified against the CA and CRL certificate configured below. |
| verifyhost | str | no | - | - | SSL servers only, when set, must match the hostnames in the subject and subjectAlternateNames of the certificate provided by the server. |
| ca | str | no | - | - | SSL servers only, set the CA authority to check the server certificate against. |
| crl | str | no | - | - | SSL servers only, set the CRL to check revoked certificates. |
| clientcert | str | no | - | - | SSL servers only, This certificate will be sent if the server send a client certificate request. |
| cookie | str | no | - | - | Persistence only, Used to identify server when cookie persistence is configured for the backend. |
| maxconn | int | no | - | - | Tuning, If the number of incoming concurrent requests goes higher than this value, they will be queued |
| advanced | str | no | - | - | Allows for adding custom HAProxy settings to the server. These are passed as written, use escaping where needed. |
| istemplate | str | no | - | - | If set, configures this server item as a template to provision servers from dns/srv responses. |
| state | str | no | present | present, absent | State in which to leave the backend server |

## Examples

```yaml
- name: Add backend server
  pfsense_haproxy_backend_server:
    backend: exchange
    name: exchange.acme.org
    address: exchange.acme.org
    port: 443
    state: present

- name: Remove backend server
  pfsense_haproxy_backend_server:
    backend: exchange
    name: exchange.acme.org
    state: absent
```

## Return Values

| Key | Type | Returned | Description | Sample |
|-----|------|----------|-------------|--------|
| commands | list | always | the set of commands that would be pushed to the remote device (if pfSense had a CLI) | `["create haproxy_backend_server 'exchange.acme.org' on 'exchange', status='active', address='exchange.acme.org', port=443", "delete haproxy_backend_server 'exchange.acme.org' on 'exchange'"]` |

## Author

- Frederic Bor (@f-bor)

## Version

Added in version 0.1.0
