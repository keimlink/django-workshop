import os
import sys
import webbrowser

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.tasks import Task


class DjangoWorkshopBaseTask(Task):
    def __init__(self, *args, **kwargs):
        super(DjangoWorkshopBaseTask, self).__init__(*args, **kwargs)
        self.prj_root = os.path.realpath(os.path.dirname(__file__))
        self.docs = os.path.join(self.prj_root, 'docs')

    def get_release(self):
        """Returns the release number."""
        sys.path.append(self.docs)
        import conf
        return conf.release


class BuildHtmlTask(DjangoWorkshopBaseTask):
    """Builds the Sphinx documentation as HTML."""
    name = 'build'

    def run(self, open_browser=True, linkcheck=False):
        with lcd(self.docs):
            local('make clean')
            local('make html')
            if linkcheck:
                local('make linkcheck')
        if open_browser:
            webbrowser.open(os.path.join(self.docs, '_build/html/index.html'))


class BuildPdfTask(DjangoWorkshopBaseTask):
    """Builds the Sphinx documentation as PDF."""
    name = 'build_pdf'

    def run(self):
        with lcd(self.docs):
            local('make clean')
            local('make latexpdf')
        pdfpath = os.path.join(self.docs, '_build/latex/DjangoWorkshop.pdf')
        try:
            os.startfile(pdfpath)
        except AttributeError:
            local('open %s' % pdfpath)


class DeployTask(BuildHtmlTask):
    """Builds and deploys the Sphinx documentation as HTML."""
    name = 'deploy'

    def run(self):
        super(DeployTask, self).run(open_browser=False, linkcheck=True)
        if not confirm('Do you wish to deploy build %s?' % self.get_release()):
            abort('Deployment cancelled.')
        with cd('doms/django-workshop.de/subs'):
            run('rm -rf www')
            run('mkdir www')
            put('docs/_build/html/*', 'www')
            put('docs/.htaccess', 'www')


env.user = 'zed00-keimlink'
env.hosts = ['zed00.hostsharing.net']
build = BuildHtmlTask()
build_pdf = BuildPdfTask()
deploy = DeployTask()
