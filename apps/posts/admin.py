from django.contrib import admin
from .models import Post, Tag, Comment, PostReport

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'count_likes')
    inlines = [CommentInline]
    
    def count_likes(self, obj):
        return obj.likes.count()

@admin.register(PostReport)
class PostReportAdmin(admin.ModelAdmin):
    list_display = ('post', 'reported_by', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')

admin.site.register(Tag)
admin.site.register(Comment)
