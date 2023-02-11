from django.contrib import admin
from .models import Product, Category
from review.models import Comment
# Register your models here.

# 
admin.site.register(Category)

class CommentInLine(admin.TabularInline):
    model = Comment


class ProductAdmin(admin.ModelAdmin):
    list_filter = ['title', 'price']
    list_display = ['title', 'slug']
    search_fields = ['title', 'description']
    inlines = [CommentInLine]

admin.site.register(Product, ProductAdmin)