from django import forms
from django.conf import settings


def get_cache_choices():
    caches = settings.CACHES or {}
    return [
        (cache_name, f"{cache_name} ({cache['BACKEND']}") for cache_name, cache in caches.items()
    ]


class ClearCacheForm(forms.Form):
    cache_name = forms.ChoiceField(choices=get_cache_choices)


class ClearCacheByKeyForm(forms.Form):
    cache_name = forms.ChoiceField(choices=get_cache_choices)
    cache_key = forms.CharField(required=True)
