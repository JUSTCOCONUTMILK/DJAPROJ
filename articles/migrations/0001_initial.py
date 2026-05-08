import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("image", models.ImageField(blank=True, null=True, upload_to="articles/")),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("status", models.CharField(choices=[("draft", "Черновик"), ("pending", "На модерации"), ("published", "Опубликовано")], default="pending", max_length=20)),
                ("approved_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="approved_articles", to=settings.AUTH_USER_MODEL)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="articles", to=settings.AUTH_USER_MODEL)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="articles", to="articles.category")),
            ],
        ),
        migrations.CreateModel(
            name="ArticleRating",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("article", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ratings", to="articles.article")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ratings", to=settings.AUTH_USER_MODEL)),
            ],
            options={"unique_together": {("user", "article")}},
        ),
        migrations.CreateModel(
            name="Bookmark",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("article", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookmarked_by", to="articles.article")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookmarks", to=settings.AUTH_USER_MODEL)),
            ],
            options={"unique_together": {("user", "article")}},
        ),
    ]
