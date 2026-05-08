from django.urls import path
from .views import (
    article_create_view, article_delete_view, article_detail_view, article_edit_view,
    article_list_view, authors_view, by_category_view, categories_view, favorites_view,
    moderation_approve_view, moderation_list_view, popular_view, rate_article_view, toggle_bookmark_view,
)

app_name = "articles"
urlpatterns = [
    path("", article_list_view, name="article_list"),
    path("popular/", popular_view, name="popular"),
    path("categories/", categories_view, name="categories"),
    path("categories/<slug:slug>/", by_category_view, name="by_category"),
    path("authors/", authors_view, name="authors"),
    path("favorites/", favorites_view, name="favorites"),
    path("create/", article_create_view, name="article_create"),
    path("<int:article_id>/", article_detail_view, name="article_detail"),
    path("<int:article_id>/edit/", article_edit_view, name="article_edit"),
    path("<int:article_id>/delete/", article_delete_view, name="article_delete"),
    path("<int:article_id>/rate/", rate_article_view, name="rate_article"),
    path("<int:article_id>/bookmark/", toggle_bookmark_view, name="toggle_bookmark"),
    path("moderation/", moderation_list_view, name="moderation"),
    path("moderation/<int:article_id>/approve/", moderation_approve_view, name="moderation_approve"),
]
