/etc/apt/sources.list:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - source: salt://apt/sources.list

apt-update:
  cmd.run:
    - name: apt-get update
    - require:
      - file: /etc/apt/sources.list
