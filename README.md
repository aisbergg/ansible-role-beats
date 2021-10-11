# Ansible Role: `aisbergg.beats`

This Ansible role can install and configure different Beats data shippers from the official [beats family](https://www.elastic.co/de/beats/). Following Beats are supported by this role:

- [auditbeat](https://www.elastic.co/beats/auditbeat)
- [filebeat](https://www.elastic.co/beats/filebeat)
- [functionbeat](https://www.elastic.co/functionbeat/auditbeat)
- [heartbeat](https://www.elastic.co/beats/heartbeat)
- [journalbeat](https://www.elastic.co/beats/journalbeat)
- [metricbeat](https://www.elastic.co/beats/metricbeat)
- [packetbeat](https://www.elastic.co/beats/packetbeat)

## Requirements

None.

## Role Variables

| Variable | Default | Comments |
|----------|---------|----------|
| `beats_centos_repo_url` | `https://artifacts.elastic.co/`<br>`packages/7.x/yum` | RPM repository URL to be used for installation |
| `beats_debian_repo_url` | `https://artifacts.elastic.co/`<br>`packages/7.x/apt` | APT repository URL to be used for installation |
| `auditbeat_service_enabled` | `false` | Install and enable Auditbeat on boot |
| `auditbeat_service_state` | `stopped` | Auditbeat Service run state (`started`, `stopped`, `restarted`) |
| `auditbeat_service_restart_on_change` | `true` | Restart Docker daemon service on configuration changes. |
| `filebeat_service_enabled` | `false` | Install and enable Filebeat on boot |
| `filebeat_service_state` | `stopped` | Filebeat Service run state (`started`, `stopped`, `restarted`) |
| `filebeat_service_restart_on_change` | `true` | Restart Docker daemon service on configuration changes. |
| `functionbeat_service_enabled` | `false` | Install and enable Functionbeat on boot |
| `functionbeat_service_state` | `stopped` | Functionbeat Service run state (`started`, `stopped`, `restarted`) |
| `functionbeat_service_restart_on_change` | `true` | Restart Docker daemon service on configuration changes. |
| `heartbeat_service_enabled` | `false` | Install and enable Heartbeat on boot |
| `heartbeat_service_state` | `stopped` | Heartbeat Service run state (`started`, `stopped`, `restarted`) |
| `heartbeat_service_restart_on_change` | `true` | Restart Docker daemon service on configuration changes. |
| `journalbeat_service_enabled` | `false` | Install and enable Journalbeat on boot |
| `journalbeat_service_state` | `stopped` | Journalbeat Service run state (`started`, `stopped`, `restarted`) |
| `journalbeat_service_restart_on_change` | `true` | Restart Docker daemon service on configuration changes. |
| `metricbeat_service_enabled` | `false` | Install and enable Metricbeat on boot |
| `metricbeat_service_state` | `stopped` | Metricbeat Service run state (`started`, `stopped`, `restarted`) |
| `metricbeat_service_restart_on_change` | `true` | Restart Docker daemon service on configuration changes. |
| `packetbeat_service_enabled` | `false` | Install and enable Packetbeat on boot |
| `packetbeat_service_state` | `stopped` | Packetbeat Service run state (`started`, `stopped`, `restarted`) |
| `packetbeat_service_restart_on_change` | `true` | Restart Docker daemon service on configuration changes. |
| `auditbeat_config` | `{}` | Configuration of Auditbeat. ([Reference](https://github.com/elastic/beats/blob/master/auditbeat/auditbeat.reference.yml)) |
| `filebeat_config` | `{}` | Configuration of Filebeat. ([Reference](https://github.com/elastic/beats/blob/master/filebeat/filebeat.reference.yml)) |
| `functionbeat_config` | `{}` | Configuration of Functionbeat. ([Reference](https://github.com/elastic/beats/blob/master/functionbeat/functionbeat.reference.yml)) |
| `heartbeat_config` | `{}` | Configuration of Heartbeat. ([Reference](https://github.com/elastic/beats/blob/master/heartbeat/heartbeat.reference.yml)) |
| `journalbeat_config` | `{}` | Configuration of Journalbeat. ([Reference](https://github.com/elastic/beats/blob/master/journalbeat/journalbeat.reference.yml)) |
| `metricbeat_config` | `{}` | Configuration of Metricbeat. ([Reference](https://github.com/elastic/beats/blob/master/metricbeat/metricbeat.reference.yml)) |
| `packetbeat_config` | `{}` | Configuration of Packetbeat. ([Reference](https://github.com/elastic/beats/blob/master/packetbeat/packetbeat.reference.yml)) |

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  vars:
    # install and manage Auditbeat service
    auditbeat_service_enabled: true
    auditbeat_service_state: started

    auditbeat_config:
      # transfer logs to central log collector
      output.logstash:
        hosts:
          - graylog1.example.org:5555
          - graylog2.example.org:5555
        loadbalance: true
        slow_start: true

      logging.level: warning
      logging.to_files: false
      logging.metrics.enabled: false

      auditbeat.modules:
        # https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-module-auditd.html
        # this replaces the Auditd program (should not run parallel to Auditd)
        - module: auditd
          resolve_ids: true
          failure_mode: silent
          backlog_limit: 8196
          rate_limit: 0
          include_raw_message: false
          include_warnings: false
          audit_rule_files: [ '${path.config}/audit.rules.d/*.conf' ]
          # taken from: https://github.com/Neo23x0/auditd/blob/master/audit.rules
          audit_rules: |
            # Self Auditing ---------------------------------------------------------------

            ## Audit the audit logs
            ### Successful and unsuccessful attempts to read information from the audit records
            -w /var/log/audit/ -k auditlog

            ## Auditd configuration
            ### Modifications to audit configuration that occur while the audit collection functions are operating
            -w /etc/audit/ -p wa -k auditconfig
            -w /etc/libaudit.conf -p wa -k auditconfig
            -w /etc/audisp/ -p wa -k audispconfig

            ## Monitor for use of audit management tools
            -w /sbin/auditctl -p x -k audittools
            -w /sbin/auditd -p x -k audittools
            -w /usr/sbin/augenrules -p x -k audittools

            # Filters ---------------------------------------------------------------------

            ### We put these early because audit is a first match wins system.

            ## Ignore SELinux AVC records
            -a always,exclude -F msgtype=AVC

            ## Ignore current working directory records
            -a always,exclude -F msgtype=CWD

            ## Ignore EOE records (End Of E

        # https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-module-file_integrity.html
        - module: file_integrity
          paths:
            - /bin
            - /usr/bin
            - /sbin
            - /usr/sbin
            - /etc
          exclude_files:
            - '(?i)\.sw[nop]$'
            - '~$'
            - '/\.git($|/)'
            - '/etc/mtab'
          scan_at_start: true
          scan_rate_per_sec: 50 MiB
          max_file_size: 300 MiB
          hash_types: [blake2b_256]
          recursive: true

        # https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-module-system.html
        - module: system
          datasets:
            - package # Installed, updated, and removed packages
          period: 30m # The frequency at which the datasets check for changes

        - module: system
          datasets:
            - host    # General host information, e.g. uptime, IPs
            - login   # User logins, logouts, and system boots.
            - process # Started and stopped processes
            - user    # User information
          state.period: 6h
          user.detect_password_changes: true
          # File patterns of the login record files.
          login.wtmp_file_pattern: /var/log/wtmp*
          login.btmp_file_pattern: /var/log/btmp*

  roles:
    - aisbergg.beats
```

## License

MIT

## Author Information

Andre Lehmann (aisberg@posteo.de)
