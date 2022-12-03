from django.contrib import admin

from .models import Comment, Like, Tweet

# Register your models here.

admin.site.register(Like)

class TweetInline(admin.TabularInline):
    model = Comment

admin.site.register(Comment)

class MyInline(admin.ModelAdmin):
    list_display=["text","image","owner","is_public","likes_count"]
    list_filter = ['text','is_public']
    inlines = [TweetInline]
    sortable_field_name = "likes_count"
admin.site.register(Tweet,MyInline)