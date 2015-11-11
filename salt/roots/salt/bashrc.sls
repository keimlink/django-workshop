user-bashrc:
  file.append:
    - name: {{ pillar['project']['home'] }}/.bashrc
    - text: |
        # Start SaltStack automated configuration
        export LC_ALL=en_US.UTF-8
        export LANG=en_US.UTF-8
        export LANGUAGE=en_US.UTF-8
        # End SaltStack automated configuration
