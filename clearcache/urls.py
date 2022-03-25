from django.urls import path

from .views import ClearCacheAdminView, ClearCacheByKeyAdminView

urlpatterns = [
    path("", ClearCacheAdminView.as_view(), name="clearcache_admin"),
    path("bykey", ClearCacheByKeyAdminView.as_view(), name="clearcachebykey_admin"),
]
