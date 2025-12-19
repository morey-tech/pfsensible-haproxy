# pfsensible.haproxy

This is a set of modules to allow you to configure HAProxy on pfSense firewalls with ansible.

## Installation from GitHub

Since this is a fork of the pfsensible.haproxy collection, you can install it directly from the GitHub repository.

### Install from default branch

To install the latest version from the main branch:

```bash
ansible-galaxy collection install git+https://github.com/morey-tech/pfsensible-haproxy.git
```

### Install from a specific branch

To install from a specific branch (e.g., for testing new features):

```bash
# Install from feature branch
ansible-galaxy collection install git+https://github.com/morey-tech/pfsensible-haproxy.git,feature/add_haproxy_frontend

# Install from main branch (explicit)
ansible-galaxy collection install git+https://github.com/morey-tech/pfsensible-haproxy.git,main
```

### Install to custom path

Optionally, you can specify the installation path with the `-p` option:

```bash
ansible-galaxy collection install git+https://github.com/morey-tech/pfsensible-haproxy.git -p ./collections
```

### Configuration

Additionally, you can set the `collections_paths` option in your `ansible.cfg` file to automatically designate install locations.

```ini
# ansible.cfg
[defaults]
collections_paths=collections
```

## Configuration

If Python discovery fails, you can set ansible_python_interpreter in your playbook or hosts vars:

pfSense >= 2.5.2:
```
ansible_python_interpreter: /usr/local/bin/python3.8
```
pfSense >= 2.4.5, < 2.5.2:
```
ansible_python_interpreter: /usr/local/bin/python3.7
```

Modules must run as root in order to make changes to the system.  By default pfSense does not have sudo capability so `become` will not work.  You can install it with:
```
  - name: "Install packages"
    package:
      name:
        - pfSense-pkg-sudo
      state: present
```
and then configure sudo so that your user has permission to use sudo.
## Modules

The following modules are currently available:

### Backend Management

* [pfsense_haproxy_backend](docs/modules/pfsense_haproxy_backend.md) - Manage HAProxy backends
* [pfsense_haproxy_backend_server](docs/modules/pfsense_haproxy_backend_server.md) - Manage HAProxy backend servers

### Frontend Management

* [pfsense_haproxy_frontend](docs/modules/pfsense_haproxy_frontend.md) - Manage HAProxy frontends
* [pfsense_haproxy_frontend_server](docs/modules/pfsense_haproxy_frontend_server.md) - Manage HAProxy frontend bind addresses
* [pfsense_haproxy_frontend_acl](docs/modules/pfsense_haproxy_frontend_acl.md) - Manage HAProxy frontend ACLs for SNI-based routing
* [pfsense_haproxy_frontend_action](docs/modules/pfsense_haproxy_frontend_action.md) - Manage HAProxy frontend actions

The modules assume that you have already installed the haproxy pfSense package.

## Supported Frontend Types

The frontend module supports the following modes:

- **http** - HTTP / HTTPS with offloading (SSL termination) - default mode
- **https** - SSL / HTTPS in TCP mode for SNI-based routing
- **tcp** - Plain TCP mode for non-HTTP protocols (MySQL, PostgreSQL, Redis, etc.)

See [frontend documentation](docs/modules/pfsense_haproxy_frontend.md) for parameter compatibility and examples.

## Development

### Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to run automated tests before each commit:

- **pycodestyle**: Python code style checking
- **ansible-test sanity**: Ansible module validation
- **ansible-test units**: Unit tests

Hooks are automatically installed when using the devcontainer.

#### Skipping Hooks

For quick commits when needed:

```bash
# Skip unit tests only (faster commits)
SKIP=ansible-test-units git commit -m "docs: update README"

# Skip all hooks (use sparingly)
git commit --no-verify -m "wip: experimental changes"
```

#### Running Hooks Manually

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ansible-test-sanity --all-files
```

### GitHub Actions CI

Pull requests automatically run the same checks as pre-commit hooks:

- **pycodestyle**: Python code style validation
- **ansible-test sanity**: Ansible module validation
- **ansible-test units**: Unit test suite

#### Status Checks

The `PR Checks` job must pass before merging. View detailed results in the Actions tab.

To configure as a required check:
1. Go to repository Settings → Branches → Branch protection rules
2. Select the main branch
3. Enable "Require status checks to pass before merging"
4. Select "PR Checks (pycodestyle, sanity, units)"

#### Full Test Matrix

The `build` job runs comprehensive tests across multiple Ansible versions (2.14, 2.15, 2.16) on pushes to main.

## [Change Log](https://github.com/pfsensible/haproxy/blob/master/CHANGELOG.rst)

## Operation

Modules in the collection work by editing `/cf/conf/config.xml` using xml.etree.ElementTree, then
calling the appropriate PHP update function via the pfSense PHP developer shell.

Some formatting is lost, and CDATA items are converted to normal entries,
but so far no problems with that have been noted.

## License

GPLv3.0 or later
