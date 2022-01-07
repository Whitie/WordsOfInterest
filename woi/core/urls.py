from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('info/<slug:ident>/', views.info, name='info'),
    path('by-year/<int:year>/', views.posts_by_year, name='by-year'),
    path('by-tag/<tag_name>/', views.posts_by_tag, name='by-tag'),
    path('article/<slug:slug>/', views.article, name='article'),
    path('article/views/<int:post_id>/', views.inc_views, name='inc-views'),
    path('comment/save/', views.save_comment, name='save-comment'),
    path('write-article/', views.edit_article, name='write-article'),
    path('edit-article/<slug:slug>/', views.edit_article, name='edit-article'),
    path('upload/', views.image_upload, name='upload'),
    path('_convert_markdown/', views.markdown_preview, name='preview'),
    path('extensions/', views.extensions, name='extensions'),
    path('extensions/<side>/', views.extensions, name='extensions'),
    path('extensions-js/', views.extensions_js, name='extensions-js'),
]
