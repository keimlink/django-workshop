"""Tasks to build and deploy the Django Workshop.

The build commmands can be used to build the documentation in different
formats.

Use the make_messages commmand to create or update the message catalog
for translations.
"""
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

    @staticmethod
    def _msgfmt(language):
        """Compiles a message object."""
        context = {
            'locale_dir': os.path.join('locale', language, 'LC_MESSAGES')
        }
        for filename in os.listdir(context['locale_dir']):
            if not filename.endswith('.po'):
                continue
            context['po_file'] = filename
            context['mo_file'] = os.path.splitext(filename)[0] + '.mo'
            cmd = 'msgfmt --check-format -D %(locale_dir)s %(po_file)s '
            cmd += '-o %(locale_dir)s/%(mo_file)s'
            local(cmd % context)

    def run(self, builder=None, language=None, linkcheck=False):
        if not builder:
            abort('Missing argument builder.')
        if language:
            if len(language) != 2:
                abort('language must be in ll format.')
        with lcd(self.docs):
            local('make clean')
            if language:
                self._msgfmt(language)
                local('make SPHINXOPTS="-Dlanguage=%s" %s' % (language, builder))
            else:
                local('make %s' % builder)
            if linkcheck:
                fastprint('\n')
                local('make linkcheck')
                fastprint('\nLink check report:\n\n')
                local('cat _build/linkcheck/output.txt')
                fastprint('\n')


class BuildHtmlTask(DjangoWorkshopBaseTask):
    """Builds the Sphinx documentation as HTML.

    The documentation is opened in the default browser after the build.
    Use the language argument to build not the default language.
    Set linkcheck to True to perform a linkcheck after the build.
    """
    name = 'build'

    def run(self, language=None, linkcheck=False, openbrowser=True):
        with hide('running'):
            super(BuildHtmlTask, self).run('html', language, linkcheck)
        if openbrowser:
            path = os.path.join(self.docs, '_build/html/index.html')
            webbrowser.open('file://%s' % path)


class ServeHtmlTask(BuildHtmlTask):
    """Builds and serves the Sphinx documentation as HTML.

    This is useful for testing Disqus integration and search functionality.

    The documentation is opened in the default browser after the build.
    Use the language argument to build not the default language.
    Set linkcheck to True to perform a linkcheck after the build.
    """
    name = 'serve'
    port = 9000

    def run(self, language=None, linkcheck=False):
        super(ServeHtmlTask, self).run(language, linkcheck, False)
        webbrowser.open('http://127.0.0.1:%d' % self.port)
        with hide('running'):
            with lcd(os.path.join(self.docs, '_build/html')):
                local('python -m SimpleHTTPServer %d' % self.port)


class BuildPdfTask(DjangoWorkshopBaseTask):
    """Builds the Sphinx documentation as PDF.

    The PDF is opened after the build with the default application.
    Use the language argument to build not the default language.
    Set linkcheck to True to perform a linkcheck after the build.
    """
    name = 'build_pdf'

    def run(self, language=None, linkcheck=False):
        with hide('running'):
            super(BuildPdfTask, self).run('latexpdf', language, linkcheck)
        pdfpath = os.path.join(self.docs, '_build/latex/DjangoWorkshop.pdf')
        try:
            os.startfile(pdfpath)
        except AttributeError:
            with hide('running'):
                local('open %s' % pdfpath)


class MakeMessageCatalogTask(DjangoWorkshopBaseTask):
    """Creates .po files in locale directory.

    The language argument is required and defines the language of the
    translation. """
    name = 'make_messages'

    def _msginit(self, pot_file, po_file):
        """Creates .po file from .pot file."""
        cmd = 'msginit --no-translator -l %(lang)s '
        cmd += '-i _build/locale/%(pot_file)s '
        cmd += '-o locale/%(lang_short)s/LC_MESSAGES/%(po_file)s'
        context = {
            'lang': self.lang,
            'lang_short': self.lang_short,
            'pot_file': pot_file,
            'po_file': po_file
        }
        local(cmd % context)

    def _msgfilter(self, po_file):
        """Filters the .po file and removes all msgstr strings."""
        po_file = 'locale/%s/LC_MESSAGES/%s' % (self.lang_short, po_file)
        cmd = 'msgfilter -i %(po_file)s --keep-header -o %(po_file)s echo -n'
        local(cmd % {'po_file': po_file})

    def _msgmerge(self, pot_file, po_file):
        """Updates .po file from .pot file."""
        po_file = 'locale/%s/LC_MESSAGES/%s' % (self.lang_short, po_file)
        cmd = 'msgmerge -U %(po_file)s _build/locale/%(pot_file)s'
        context = {
            'lang_short': self.lang_short,
            'pot_file': pot_file,
            'po_file': po_file
        }
        fastprint('Updating %s' % po_file)
        local(cmd % context)

    def run(self, language=None):
        if not language:
            abort('Missing argument language.')
        if len(language) != 5:
            abort('language must be in ll_CC format.')
        self.lang = language
        self.lang_short = language[:2]
        with lcd(self.docs):
            new_catalog = False
            locale_dir = os.path.join('locale', self.lang_short, 'LC_MESSAGES')
            with hide('running'):
                if not os.path.exists(locale_dir):
                    local('mkdir -p %s' % locale_dir)
                    new_catalog = True
                local('make gettext')
                fastprint('\n')
                for filename in os.listdir('_build/locale'):
                    if not filename.endswith('.pot'):
                        continue
                    if new_catalog:
                        self._msginit(filename, filename[:-1])
                        self._msgfilter(filename[:-1])
                    else:
                        self._msgmerge(filename, filename[:-1])


class DeployTask(DjangoWorkshopBaseTask):
    """Builds and deploys the Sphinx documentation as HTML.

    Performs an automatic linkcheck after the build before the deployment.
    """
    name = 'deploy'

    def run(self):
        with hide('running'):
            super(DeployTask, self).run('html', linkcheck=True)
        msg = 'Do you wish to deploy build %s?' % self.get_release()
        if not confirm(msg, default=False):
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
make_messages = MakeMessageCatalogTask()
deploy = DeployTask()
serve = ServeHtmlTask()
