import json

from django.contrib import messages
from django.contrib.auth import (
    authenticate, login as auth_login, logout as auth_logout
)
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.module_loading import import_string
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods, require_POST

from . import utils
from .forms import ArticleForm, LoginForm
from .models import Comment, Extension, Post, PostImage, SiteInfo, Tag


def index(req):
    posts = Post.objects.select_related().filter(
        status=Post.Status.PUBLISHED
    ).order_by('-updated')[:10]
    ctx = dict(posts=posts, headline=_('Last 10 Articles'), index=True)
    return render(req, 'core/index.html', ctx)


def posts_by_year(req, year):
    posts = Post.objects.select_related().filter(
        status=Post.Status.PUBLISHED, created__year=year
    ).order_by('-created')
    ctx = dict(posts=posts, headline=_('Articles {}').format(year))
    return render(req, 'core/index.html', ctx)


def posts_by_tag(req, tag_name):
    tag = get_object_or_404(Tag, tag=tag_name)
    posts = tag.posts.filter(status=Post.Status.PUBLISHED).order_by('-updated')
    ctx = dict(posts=posts, headline=_('Articles tagged {}').format(tag_name))
    return render(req, 'core/index.html', ctx)


def article(req, slug):
    q = Post.objects.select_related().filter(status=Post.Status.PUBLISHED)
    post = get_object_or_404(q, slug=slug)
    comments = post.comments.filter(active=True).order_by('-created')
    unpublished = post.comments.filter(active=False).count()
    ctx = dict(post=post, comments=comments, unpublished=unpublished)
    return render(req, 'core/article.html', ctx)


@permission_required('core.can_write', raise_exception=True)
def edit_article(req, slug=None):
    if slug:
        post = get_object_or_404(Post, slug=slug)
    else:
        post = None
    if req.method == 'POST':
        form = ArticleForm(req.POST, req.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if not post:
                post = Post(slug=slugify(cd['title']))
            else:
                post.updated = timezone.now()
            post.title = cd['title']
            post.image = cd['image']
            post.raw = cd['raw']
            post.tags.set(cd['tags'])
            post.comments_allowed = cd['comments_allowed']
            post.save()
            messages.success(req, _('Article was saved.'))
            return redirect('core:index')
    else:
        if post:
            form = ArticleForm({
                'title': post.title,
                'image': post.image,
                'raw': post.raw,
                'tags': post.tags.all(),
                'comments_allowed': post.comments_allowed
            })
        else:
            form = ArticleForm()
    ctx = dict(form=form, post=post)
    return render(req, 'core/edit_article.html', ctx)


def info(req, ident):
    site_info = get_object_or_404(SiteInfo, ident=ident)
    return render(req, 'core/info.html', {'info': site_info})


@require_POST
def login(req):
    form = LoginForm(req.POST)
    if form.is_valid():
        user = authenticate(req, **form.cleaned_data)
        if user is not None:
            auth_login(req, user)
            messages.success(req, _('Login successful.'))
            return redirect('core:index')
    messages.error(req, _('Login failed, check username and/or password.'))
    return redirect('core:index')


@login_required
def logout(req):
    auth_logout(req)
    messages.success(req, _('Your are now logged out.'))
    return redirect('core:index')


@login_required
@require_POST
def image_upload(req):
    img = PostImage.objects.create(file=req.FILES['image'])
    url = req.build_absolute_uri(img.file.url)
    return JsonResponse({'data': {'filePath': url}})


@login_required
@require_POST
def markdown_preview(req):
    data = json.loads(req.body)
    html = utils.create_html(data['markdown'])
    return JsonResponse({'html': html})


@require_http_methods(['PUT'])
def save_comment(req):
    data = json.loads(req.body)
    post_id = data.pop('post_id')
    data['post'] = Post.objects.get(pk=post_id)
    Comment.objects.create(**data)
    return utils.HttpResponseCreated()


def inc_views(req, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.views += 1
    post.save()
    return HttpResponse('OK')


def extensions(req, side):
    q = Extension.objects.filter(active=True, side=side)
    if not req.user.is_authenticated:
        q = q.exclude(login_required=True)
    extensions = []
    for ext in q.order_by('position', 'id'):
        try:
            func = import_string(ext.callable)
            extensions.append({
                'name': ext.name,
                'id': ext.html_id,
                'content': func(req),
            })
        except Exception as err:
            ext.errors = str(err)
            ext.save()
    return JsonResponse({'data': extensions})


def extensions_js(req):
    q = Extension.objects.filter(active=True)
    scripts = []
    for ext in q.exclude(js_file__in=['', None]):
        scripts.append(ext.js_file.read())
    return HttpResponse(b'\n'.join(scripts))
