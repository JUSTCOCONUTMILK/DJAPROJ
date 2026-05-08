from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ArticleForm, RatingForm
from .models import Article, ArticleRating, Bookmark, Category

User = get_user_model()


def _can_manage_article(user, article):
    return user.is_superuser or user.is_staff or article.author_id == user.id


def article_list_view(request):
    articles = Article.objects.filter(status=Article.Status.PUBLISHED).select_related("author", "category")
    return render(request, "articles/article_list.html", {"articles": articles, "title": "Статьи"})


def popular_view(request):
    articles = [a for a in Article.objects.filter(status=Article.Status.PUBLISHED).select_related("author", "category") if a.rating >= 4]
    return render(request, "articles/article_list.html", {"articles": articles, "title": "Популярное"})


def categories_view(request):
    categories = Category.objects.annotate(total=Count("articles"))
    return render(request, "articles/categories.html", {"categories": categories})


def by_category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category, status=Article.Status.PUBLISHED).select_related("author", "category")
    return render(request, "articles/article_list.html", {"articles": articles, "title": f"Категория: {category.name}"})


def article_detail_view(request, article_id):
    article = get_object_or_404(Article.objects.select_related("author", "category"), pk=article_id)
    if article.status != Article.Status.PUBLISHED and not (request.user.is_authenticated and _can_manage_article(request.user, article)):
        return redirect("articles:article_list")
    user_rating = ArticleRating.objects.filter(article=article, user=request.user).first() if request.user.is_authenticated else None
    return render(request, "articles/article_detail.html", {"article": article, "user_rating": user_rating})


@login_required
def article_create_view(request):
    if request.user.is_banned:
        return redirect("articles:article_list")
    form = ArticleForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        
        if request.user.is_staff or request.user.is_superuser:
            if form.cleaned_data["submit_for_moderation"]:
                article.status = Article.Status.PUBLISHED
                article.approved_by = request.user
            else:
                article.status = Article.Status.DRAFT
        else:
            article.status = Article.Status.PENDING if form.cleaned_data["submit_for_moderation"] else Article.Status.DRAFT
        
        article.save()
        return redirect("articles:article_detail", article_id=article.id)
    return render(request, "articles/article_form.html", {"form": form, "title": "Создать статью"})


@login_required
def article_edit_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if not _can_manage_article(request.user, article):
        return redirect("articles:article_detail", article_id=article.id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article, user=request.user)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        
        if request.user.is_staff or request.user.is_superuser:
            if form.cleaned_data["submit_for_moderation"]:
                article.status = Article.Status.PUBLISHED
                article.approved_by = request.user
            else:
                article.status = Article.Status.DRAFT
        else:
            article.status = Article.Status.PENDING if form.cleaned_data["submit_for_moderation"] else Article.Status.DRAFT
            article.approved_by = None
        
        article.save()
        return redirect("articles:article_detail", article_id=article.id)
    return render(request, "articles/article_form.html", {"form": form, "title": "Редактировать статью"})


@login_required
def article_delete_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if not _can_manage_article(request.user, article):
        return redirect("articles:article_detail", article_id=article.id)
    if request.method == "POST":
        article.delete()
        return redirect("articles:article_list")
    return render(request, "articles/article_delete_confirm.html", {"article": article})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def moderation_list_view(request):
    articles = Article.objects.filter(status=Article.Status.PENDING).select_related("author", "category")
    return render(request, "articles/moderation_list.html", {"articles": articles})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def moderation_approve_view(request, article_id):
    if request.method != "POST":
        return redirect("articles:moderation")
    article = get_object_or_404(Article, pk=article_id)
    article.status = Article.Status.PUBLISHED
    article.approved_by = request.user
    article.save(update_fields=["status", "approved_by", "updated_at"])
    return redirect("articles:moderation")


@login_required
def rate_article_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id, status=Article.Status.PUBLISHED)
    rating, _ = ArticleRating.objects.get_or_create(article=article, user=request.user, defaults={"score": 5})
    form = RatingForm(request.POST, instance=rating)
    if form.is_valid():
        form.save()
    return redirect("articles:article_detail", article_id=article.id)


@login_required
def toggle_bookmark_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id, status=Article.Status.PUBLISHED)
    bookmark = Bookmark.objects.filter(article=article, user=request.user).first()
    if bookmark:
        bookmark.delete()
    else:
        Bookmark.objects.create(article=article, user=request.user)
    return redirect("articles:article_detail", article_id=article.id)


@login_required
def favorites_view(request):
    articles = Article.objects.filter(status=Article.Status.PUBLISHED, bookmarked_by__user=request.user).select_related("author", "category")
    return render(request, "articles/article_list.html", {"articles": articles, "title": "Избранное"})


def authors_view(request):
    authors = User.objects.annotate(published_count=Count("articles", filter=Q(articles__status=Article.Status.PUBLISHED))).order_by("-published_count", "username")
    return render(request, "articles/authors.html", {"authors": authors})
