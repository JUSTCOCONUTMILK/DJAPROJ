from django.db import migrations
from django.utils.text import slugify


def seed_categories(apps, schema_editor):
    Category = apps.get_model("articles", "Category")
    names = ["Backend", "Frontend", "AI", "Cyber security", "Cyber sport", "Game Development"]
    for name in names:
        Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})


class Migration(migrations.Migration):
    dependencies = [("articles", "0001_initial")]
    operations = [migrations.RunPython(seed_categories, migrations.RunPython.noop)]
