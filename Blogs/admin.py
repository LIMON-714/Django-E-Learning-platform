from django.contrib import admin
from .models import Blog, Category

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'like_count', 'share_count', 'created_at')
    list_filter = ('category', 'author', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    filter_horizontal = ('likes',)  # optional: select multiple users who liked

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = "Likes"

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
