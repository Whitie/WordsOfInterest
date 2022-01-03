from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify, Truncator
from django.utils.translation import gettext_lazy as _

from . import utils


def get_sentinel_user() -> User:
    return User.objects.get_or_create(username='deleted')[0]


def js_path(instance, filename):
    return f'extensions/{instance.html_id}/{filename}'


class Tag(models.Model):
    tag = models.CharField(_('Tag'), max_length=30, unique=True)
    description = models.CharField(_('Description'), max_length=150,
                                   blank=True)

    def __str__(self) -> str:
        return self.tag

    @property
    def has_posts(self) -> bool:
        return bool(self.posts.all().count())

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['tag']


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')

    title = models.CharField(_('Title'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=150, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.SET(get_sentinel_user),
        verbose_name=_('Author'), related_name='posts'
    )
    image = models.ImageField(_('Image'), upload_to='uploads/%Y/%m',
                              blank=True)
    raw = models.TextField(_('Raw content'))
    html = models.TextField(editable=False, blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    status = models.CharField(
        _('Status'), max_length=10, choices=Status.choices,
        default=Status.DRAFT
    )
    tags = models.ManyToManyField(
        Tag, verbose_name=_('Tags'), related_name='posts', blank=True
    )
    comments_allowed = models.BooleanField(_('Comments allowed'), default=True)

    def __str__(self) -> str:
        return f'{self.title} - {self.author.username}'

    def save(self, *args, **kw) -> None:
        self.html = utils.create_html(self.raw)
        super().save(*args, **kw)

    def get_plaintext(self, max_chars: int = 0) -> str:
        plain = utils.unmark(self.raw)
        if max_chars:
            return Truncator(plain).chars(max_chars)
        else:
            return plain

    @property
    def has_comments(self) -> bool:
        return bool(self.comments.filter(active=True).count())

    @property
    def is_updated(self) -> bool:
        delta = self.updated - self.created
        return delta.total_seconds() > 120

    def _reading_time(self) -> int:
        """Calculated with 4 words per second (240 words per minute).
           +30s for every image.
        """
        words = len(self.get_plaintext().split())
        seconds = words // 4
        if self.image:
            seconds += 30
        seconds += 30 * self.images.all().count()
        if seconds < 30:
            return 30
        return seconds

    @property
    def reading_time(self) -> str:
        rt = self._reading_time()
        if rt <= 120:
            return _('{}sec').format(rt)
        if rt % 60:
            rt += 60
        return _('{}min').format(rt // 60)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-created']
        permissions = [
            ('can_write', _('Can write Post')),
            ('can_publish', _('Can publish Post')),
        ]


class View(models.Model):
    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, verbose_name=_('Post'),
        related_name='views'
    )
    clicks = models.PositiveIntegerField(_('Clicks'), default=0,
                                         editable=False)

    def __str__(self) -> str:
        return f'{self.post} [{self.clicks}]'

    class Meta:
        verbose_name = _('View')
        verbose_name_plural = _('Views')


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name=_('Post'),
        related_name='comments'
    )
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'), blank=True)
    body = models.TextField(_('Message'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    active = models.BooleanField(_('Active'), default=False)

    def __str__(self) -> str:
        return _('Comment {} by {}').format(self.body, self.name)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['post', '-created']


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name=_('Post'),
        related_name='images', blank=True, null=True
    )
    file = models.ImageField(_('File'), upload_to='uploads/%Y/%m')
    caption = models.CharField(_('Caption'), max_length=150, blank=True)

    def __str__(self) -> str:
        return f'{self.post.title} - {self.file.name}'

    class Meta:
        verbose_name = _('Post Image')
        verbose_name_plural = _('Post Images')
        ordering = ['post']


class Extension(models.Model):

    class Side(models.TextChoices):
        LEFT = 'left', _('Left')
        RIGHT = 'right', _('Right')

    name = models.CharField(_('Name'), max_length=50, unique=True)
    description = models.TextField(_('Description'), blank=True)
    side = models.CharField(_('Side'), max_length=5, choices=Side.choices,
                            default=Side.LEFT)
    position = models.PositiveSmallIntegerField(_('Position'), default=1)
    callable = models.CharField(_('Function'), max_length=150)
    login_required = models.BooleanField(_('Login required'), default=False)
    js_file = models.FileField(_('JS File'), upload_to=js_path, blank=True)
    added = models.DateTimeField(_('Added'), auto_now_add=True)
    active = models.BooleanField(_('Active'), default=False)
    errors = models.TextField(_('Errors'), blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def html_id(self) -> str:
        return slugify(self.name)

    class Meta:
        verbose_name = _('Extension')
        verbose_name_plural = _('Extensions')
        ordering = ['side', 'position']


class SiteInfo(models.Model):
    name = models.CharField(_('Name'), unique=True, max_length=100)
    ident = models.SlugField(_('Identifier'), unique=True, max_length=100)
    raw = models.TextField(_('Raw content'))
    html = models.TextField(editable=False, blank=True)
    show_in_menu = models.BooleanField(_('Show in menu'), default=False)
    fa_icon = models.CharField(_('Font Awesome Icon'), max_length=30,
                               default='fas fa-info')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kw) -> None:
        self.html = utils.create_html(self.raw)
        super().save(*args, **kw)

    class Meta:
        verbose_name = _('Site Info')
        verbose_name_plural = _('Site Infos')
        ordering = ['name']
