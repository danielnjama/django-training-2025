from django.contrib import admin
from .models import Blog, Category, Tag, Comment


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'category')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'blog', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}




admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
