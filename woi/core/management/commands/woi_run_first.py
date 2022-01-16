import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core import management
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from core.models import Extension, SiteInfo


PROJECT_BASE = settings.BASE_PATH.parent
ENV_PATH = settings.BASE_PATH / '.env'
README = PROJECT_BASE / 'README.md'
TERMS_TPL = """\
## Page details

Website Owner: YOUR NAME HERE

This is the standard template. The Owner has not written the full
terms yet.
"""
PRIVACY_TPL = """\
## Privacy

This site uses cookies to track user sessions. If Google Analytics is
enabled by the admin, it uses cookies for statistics.
"""


def create_menus():
    Extension.objects.get_or_create(
        name=_('List of years'),
        description=_('List of all years with articles'),
        side=Extension.Side.LEFT, position=1, active=True,
        callable='core.builtin_extensions.list_of_years'
    )
    Extension.objects.get_or_create(
        name=_('List of tags'),
        description=_('List of all tags with articles'),
        side=Extension.Side.LEFT, position=2, active=True,
        callable='core.builtin_extensions.list_of_tags'
    )
    Extension.objects.get_or_create(
        name=_('Menu'),
        side=Extension.Side.LEFT, position=3, active=True,
        callable='core.builtin_extensions.menu'
    )
    Extension.objects.get_or_create(
        name=_('Sign in/out'),
        description=_('Form to enter credentials or to sign out'),
        side=Extension.Side.RIGHT, position=1, active=True,
        callable='core.builtin_extensions.sign_in_out'
    )
    Extension.objects.get_or_create(
        name=_('Simple Search'),
        description=_('Simple search in title and raw (Markdown) body.'),
        side=Extension.Side.RIGHT, position=2, active=True,
        callable='core.builtin_extensions.search'
    )
    Extension.objects.get_or_create(
        name=_('Go to'),
        description=_('Dropdown with all published articles'),
        side=Extension.Side.RIGHT, position=3, active=True,
        callable='core.builtin_extensions.go_to'
    )


def create_pages():
    SiteInfo.objects.get_or_create(
        name=_('Terms'), ident='terms', raw=TERMS_TPL,
        show_in_menu=True
    )
    SiteInfo.objects.get_or_create(
        name=_('Privacy'), ident='privacy', raw=PRIVACY_TPL,
        fa_icon='fas fa-user-shield'
    )


def add_readme():
    with README.open() as fp:
        SiteInfo.objects.get_or_create(
            name='README', ident='readme', raw=fp.read(),
            fa_icon='fab fa-readme', show_in_menu=True
        )


def _ask(prompt, default=None):
    if default is not None:
        prompt = f'{prompt} [{default}]: '
    while True:
        answer = input(prompt).strip()
        if answer:
            return answer
        if default is not None:
            return default


class Command(BaseCommand):
    help = _('Setup base configuration for WoI')
    woi_env = {
        'debug': 'off',
        'secret_key': os.urandom(40),
        'allowed_hosts': ['127.0.0.1'],
        'woi_title': '',
        'woi_subtitle': '',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--deploy',
            action='store_true',
            default=False,
            help=_('Copy static files to STATIC_ROOT')
        )
        parser.add_argument(
            '--readme',
            action='store_true',
            default=False,
            help=_('Store README.md as info page')
        )

    def handle(self, *args, **options):
        management.call_command('migrate')
        if not User.objects.all().count():
            management.call_command('createsuperuser')
        self.stdout.write(_('### Creating menus'))
        create_menus()
        self.stdout.write(_('### Creating standard pages'))
        create_pages()
        if options['readme'] and README.is_file():
            add_readme()
        if options['deploy']:
            management.call_command('collectstatic', '--no-input')
        self._ask_for_local_install()
        self._create_env_file()

    def _create_env_file(self):
        with ENV_PATH.open('w', encoding='utf-8') as fp:
            for k, v in self.woi_env.items():
                if isinstance(v, list):
                    val = ' '.join(v)
                elif isinstance(v, bool):
                    val = 'on' if v else 'off'
                else:
                    val = v
                fp.write(f'{k.upper()}={val}{os.linesep}')

    def _ask_for_local_install(self):
        self.stdout.write(_('Enter title for your blog'))
        self.woi_env['woi_title'] = _ask('Title', 'WoI')
        self.stdout.write(_('Enter subtitle'))
        self.woi_env['woi_subtitle'] = _ask('Subtitle', 'Words Of Interest')
