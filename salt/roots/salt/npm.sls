include:
  - git

nodejs:
  pkg:
    - installed

nodejs-legacy:
  pkg.installed:
    - require:
      - pkg: nodejs

npm:
  pkg.installed:
    - require:
      - pkg: nodejs

bower:
  npm.installed:
    - name: bower
    - require:
      - pkg: git
      - pkg: nodejs-legacy
      - pkg: npm

gulp:
  npm.installed:
    - name: gulp
    - require:
      - pkg: npm
