# Changelog

All notable changes to this project will be documented in this file.

- [1.3.1 (2022-03-30)](#131-2022-03-30)
- [1.3.0 (2022-03-30)](#130-2022-03-30)
- [1.2.0 (2022-01-28)](#120-2022-01-28)
- [1.1.0 (2021-10-11)](#110-2021-10-11)
- [1.0.0 (2021-05-10)](#100-2021-05-10)

---

<a name="1.3.1"></a>
## [1.3.1](https://github.com/aisbergg/ansible-role-beats/compare/v1.3.0...v1.3.1) (2022-03-30)

### CI Configuration

- bump Ansible Galaxy action


<a name="1.3.0"></a>
## [1.3.0](https://github.com/aisbergg/ansible-role-beats/compare/v1.2.0...v1.3.0) (2022-03-30)

### Code Refactoring

- clean up config

### Features

- change mode for configuration files to 640
- add 'install state' for every beat app
- use nicer YAML formatting


<a name="1.2.0"></a>
## [1.2.0](https://github.com/aisbergg/ansible-role-beats/compare/v1.1.0...v1.2.0) (2022-01-28)

### Bug Fixes

- file path of repository GPG key

### Build System

- correct collection dependencies

### CI Configuration

- fix automatic release and publish process

### Chores

- include changelog in bump commits
- update changelog template
- **requirements.yml:** add role requirements


<a name="1.1.0"></a>
## [1.1.0](https://github.com/aisbergg/ansible-role-beats/compare/v1.0.0...v1.1.0) (2021-10-11)

### Chores

- update changelog
- update linter config
- update platform info
- **.pre-commit-config.yaml:** bump pre-commit hook versions
- **CHANGELOG.tpl.md:** update changelog template

### Documentation

- **README.md:** update readme

### Features

- add option *_restart_on_change


<a name="1.0.0"></a>
## [1.0.0]() (2021-05-10)

Initial Release
