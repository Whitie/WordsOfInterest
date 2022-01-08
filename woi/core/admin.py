from django.contrib import admin

from .models import Comment, Extension, Post, SiteInfo, Tag


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created', 'active')
    list_filter = ('active', 'created')
    list_editable = ('active',)
    search_fields = ('name', 'email', 'body')


@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    list_display = ('name', 'side', 'position', 'active')
    list_filter = ('side', 'active')
    list_editable = ('side', 'position', 'active')
    search_fields = ('name', 'decription')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created', 'updated', 'status', 'views')
    list_filter = ('author', 'status', 'updated')
    list_editable = ('title', 'status')
    search_fields = ('title', 'author__username')
    readonly_fields = ('views',)
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    class Media:
        css = {'all': ('3rd/css/all.min.css', '3rd/css/easymde.min.css',)}
        js = ('3rd/js/easymde.min.js', 'core/js/init_easymde.js')


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('ident', 'name', 'show_in_menu', 'fa_icon')
    list_filter = ('show_in_menu',)
    list_editable = ('name', 'show_in_menu', 'fa_icon')
    search_fields = ('name',)
    prepopulated_fields = {'ident': ('name',)}

    class Media:
        css = {'all': ('3rd/css/all.min.css', '3rd/css/easymde.min.css',)}
        js = ('3rd/js/easymde.min.js', 'core/js/init_easymde.js')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'description')
    list_editable = ('tag', 'description')
    search_fields = ('tag', 'description')
