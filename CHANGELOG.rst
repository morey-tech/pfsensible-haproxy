=============================
pfSensible.HAProxy Release Notes
=============================

.. contents:: Topics


v0.2.0
======

New Features
------------

- Added ``pfsense_haproxy_frontend`` module for managing HAProxy frontends
- Added ``pfsense_haproxy_frontend_server`` module for managing frontend bind addresses
- Added ``pfsense_haproxy_frontend_acl`` module for ACL-based routing
- Added ``pfsense_haproxy_frontend_action`` module for frontend actions
- Added TCP mode support for HAProxy frontends (http, https, tcp modes)
- Added extaddr parameter validation for frontend_server
- Added pre-commit hooks for automated testing
- Added GitHub Actions PR checks workflow

Bug Fixes
---------

- Fixed frontend ACL writing to ha_acls section for config generation
- Fixed httpclose default to only apply for http type frontends
- Fixed ansible-test sanity failures

Documentation
-------------

- Added module documentation in ``docs/modules/``
- Added AGENTS.md development guidelines
- Updated installation instructions for GitHub fork

v0.1.0
======

This simply moved the pfsense_haproxy_backend and pfsense_haproxy_backend_server modules from version 0.6.0 of pfsensible.core to pfsensible.haproxy.
