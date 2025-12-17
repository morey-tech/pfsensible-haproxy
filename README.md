# pfsensible.haproxy

This is a set of modules to allow you to configure HAProxy on pfSense firewalls with ansible.

## Installation using ansible galaxy

To install:

```
ansible-galaxy collection install pfsensible.haproxy
```

Optionally, you can specify the path of the collection installation with the `-p` option.

```
ansible-galaxy collection install pfsensible.haproxy -p ./collections
```

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

* [pfsense_haproxy_backend](https://github.com/pfsensible/haproxy/wiki/pfsense_haproxy_backend) for HAProxy backends
* [pfsense_haproxy_backend_server](https://github.com/pfsensible/haproxy/wiki/pfsense_haproxy_backend_server) for HAProxy backends servers

The modules assume that you have already installed the haproxy pfSense package.

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
