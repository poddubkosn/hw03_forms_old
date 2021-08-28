from django.contrib import admin
from .models import Post
from .models import Group


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    list_editable = ('group',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'description',)
    search_fields = ('title', 'slug',)
    empty_value_display = '-пусто-'
    list_editable = ('title', 'description')


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
