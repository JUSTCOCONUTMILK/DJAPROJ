from django.core.management.base import BaseCommand
from articles.models import Category


class Command(BaseCommand):
    help = 'Initialize required categories'

    def handle(self, *args, **options):
        categories = [
            'Backend',
            'Frontend', 
            'AI',
            'Cyber security',
            'Cyber sport',
            'Game Development'
        ]
        
        created_count = 0
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category_name}'))
        
        self.stdout.write(self.style.SUCCESS(f'Initialization complete. Created {created_count} new categories.'))
