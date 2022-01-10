from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import gettext as _

from . import utils
from .forms import LoginForm
from .models import Comment, Post, SiteInfo, Tag


def list_of_years(req):
    posts = []
    query = Post.objects.filter(status=Post.Status.PUBLISHED)
    first = query.earliest('created')
    last = query.latest('created')
    for year in range(last.created.year, first.created.year - 1, -1):
        count = query.filter(created__year=year).count()
        if count:
            posts.append((year, count))
    return utils.render_template(
        req, 'core/extensions/list_of_years.part.html',
        {'posts_by_year': posts}
    )


def list_of_tags(req):
    tags = [x for x in Tag.objects.select_related().all() if x.has_posts]
    if not tags:
        raise ValueError('No tags available')
    return utils.render_template(
        req, 'core/extensions/list_of_tags.part.html', {'tags': tags}
    )


def sign_in_out(req):
    return utils.render_template(
        req, 'core/extensions/sign_in_out.part.html', {'form': LoginForm()}
    )


def menu(req):
    comments_count = Comment.objects.filter(active=False).count()
    posts_count = Post.objects.filter(status=Post.Status.DRAFT).count()
    infos = SiteInfo.objects.filter(show_in_menu=True).order_by('ident')
    ctx = dict(comments_count=comments_count, posts_count=posts_count,
               infos=infos)
    return utils.render_template(
        req, 'core/extensions/menu.part.html', ctx
    )


def go_to(req):
    posts = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).order_by('title')
    return utils.render_template(
        req, 'core/extensions/go_to.part.html', {'posts': posts}
    )


def search(req):
    return utils.render_template(req, 'core/extensions/search.html')


def search_result(req):
    search = req.GET.get('search', '').strip()
    if search:
        posts = Post.objects.select_related().filter(
            Q(title__icontains=search) | Q(raw__icontains=search),
            status=Post.Status.PUBLISHED
        ).order_by('-created')
    else:
        posts = []
    ctx = dict(posts=posts, headline=_('Search for "{}"').format(search))
    return render(req, 'core/index.html', ctx)
