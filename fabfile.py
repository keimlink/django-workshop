from fabric.api import *
from fabric.contrib.console import confirm


env.user = 'zed00-keimlink'
env.hosts = ['zed00.hostsharing.net']


@task
def build():
    """Builds the Sphinx documentation."""
    with lcd('docs'):
        local('make clean')
        local('make html')


@task
def deploy():
    """Builds and deploys the Sphinx documentation."""
    build()
    if not confirm('Do you wish to deploy this build?'):
        abort('Deployment cancelled.')
    with cd('doms/django-workshop.de/subs'):
        run('rm -rf www')
        run('mkdir www')
        put('docs/_build/html/*', 'www')
        put('docs/.htaccess', 'www')
