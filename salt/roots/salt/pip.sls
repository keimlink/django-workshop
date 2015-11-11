include:
  - curl

curl -sS https://bootstrap.pypa.io/get-pip.py | python -:
  cmd.run:
    - unless: hash pip 2>/dev/null
    - require:
      - pkg: curl
    - reload_modules: True
