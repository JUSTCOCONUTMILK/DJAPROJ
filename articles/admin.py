from django.contrib import admin
from .models import Article, ArticleRating, Bookmark, Category

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(ArticleRating)
admin.site.register(Bookmark)
