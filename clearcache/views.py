from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from clearcache.forms import ClearCacheForm, ClearCacheByKeyForm
from clearcache.utils import clear_cache, clear_cache_key


class ClearCacheAdminView(UserPassesTestMixin, FormView):
    form_class = ClearCacheForm
    template_name = "clearcache/admin/clearcache_form.html"

    success_url = reverse_lazy("clearcache_admin")

    def test_func(self):
        # Only super user can clear caches via admin.
        return self.request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, args, kwargs)
        return response

    def form_valid(self, form):
        try:
            cache_name = form.cleaned_data["cache_name"]
            clear_cache(cache_name)
            messages.success(
                self.request,
                f"Successfully cleared '{form.cleaned_data['cache_name']}' cache",
            )
        except Exception as err:
            messages.error(
                self.request,
                f"Couldn't clear cache, something went wrong. Received error: {err}",
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clear cache"
        return context


class ClearCacheByKeyAdminView(UserPassesTestMixin, FormView):
    form_class = ClearCacheByKeyForm
    template_name = "clearcache/admin/clearcachebykey_form.html"

    success_url = reverse_lazy("clearcachebykey_admin")

    def test_func(self):
        # Only super user can clear caches via admin.
        return self.request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, args, kwargs)
        return response

    def form_valid(self, form):
        try:
            cache_name = form.cleaned_data["cache_name"]
            cache_key = form.cleaned_data["cache_key"]

            if clear_cache_key(cache_name, cache_key):
                messages.success(
                    self.request,
                    f"Successfully cleared key:'{form.cleaned_data['cache_key']}' from cache: '{form.cleaned_data['cache_name']}'",
                )
            else:
                messages.error(
                    self.request,
                    f"Cache key '{cache_key}' does not exists for cache: '{form.cleaned_data['cache_name']}'",
                )
        except Exception as err:
            messages.error(
                self.request,
                f"Couldn't clear cache, something went wrong. Received error: {err}",
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clear cache by key"
        return context
