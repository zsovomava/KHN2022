from django.contrib import admin
from .models import Topic, Post, Comment, Tip

admin.AdminSite.site_title = 'NISZ'
admin.AdminSite.site_header = 'NISZ adminisztráció'
admin.AdminSite.index_title = 'Oldal adminisztráció'


admin.site.register(Topic)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'pub_date')

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('id', 'author', 'title', 'pub_date')
    list_display_links = ('id', 'title')
    list_filter = ['pub_date']
    search_fields = ['title']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tip)
