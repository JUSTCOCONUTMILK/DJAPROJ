from django import forms
from .models import Article, ArticleRating


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and (user.is_staff or user.is_superuser):
            self.fields['submit_for_moderation'].label = "Опубликовать сразу"
        else:
            self.fields['submit_for_moderation'].label = "Отправить на модерацию"
    
    submit_for_moderation = forms.BooleanField(required=False, initial=True, label="Отправить на модерацию")

    class Meta:
        model = Article
        fields = ("title", "image", "content", "category", "submit_for_moderation")


class RatingForm(forms.ModelForm):
    class Meta:
        model = ArticleRating
        fields = ("score",)
