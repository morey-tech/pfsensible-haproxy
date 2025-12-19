# pfsense_haproxy_frontend_acl

Manage pfSense HAProxy frontend ACLs

## Synopsis

- Manage pfSense HAProxy frontend Access Control Lists (ACLs) for SNI-based routing.
- ACLs define conditions that can be used with actions to route traffic to different backends.

## Notes

- SNI-based ACLs require the frontend to be configured in 'https' or 'tcp' mode, not 'http'.

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| frontend | str | yes | - | - | The frontend name to add the ACL to. |
| name | str | yes | - | - | The ACL name. This name is used to reference the ACL in actions. ACLs with the same name are combined using OR logic. |
| expression | str | yes | - | ssl_sni_matches, ssl_sni_contains, ssl_sni_starts_with, ssl_sni_ends_with, ssl_sni_regex | The ACL expression type for SNI matching. |
| value | str | yes | - | - | The value to match against (hostname, pattern, or regex). |
| casesensitive | bool | no | false | - | Enable case-sensitive matching. |
| negate | bool | no | false | - | Negate the match (match if condition is NOT met). |
| state | str | no | present | present, absent | State in which to leave the ACL. |

## Expression Types

| Expression | Description |
|------------|-------------|
| ssl_sni_matches | Exact match of the SNI hostname |
| ssl_sni_contains | SNI hostname contains the specified string |
| ssl_sni_starts_with | SNI hostname starts with the specified string |
| ssl_sni_ends_with | SNI hostname ends with the specified string |
| ssl_sni_regex | SNI hostname matches the specified regex pattern |

## Examples

```yaml
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
    value: "api-v[0-9]+\\.example\\.com"
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
```

## Return Values

| Key | Type | Returned | Description | Sample |
|-----|------|----------|-------------|--------|
| commands | list | always | the set of commands that would be pushed to the remote device (if pfSense had a CLI) | `["create haproxy_frontend_acl 'is_api' on 'sni-frontend', expression='ssl_sni_matches', value='api.example.com'", "delete haproxy_frontend_acl 'is_api' on 'sni-frontend'"]` |

## Author

- Nicholas Morey (@morey-tech)

## Version

Added in version 0.3.0
