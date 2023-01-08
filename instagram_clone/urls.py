"""
instagram_clone URL Configuration
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from instagram_clone import settings
from instagram_clone.user.urls import url_path as user_app_urls
from instagram_clone.user_relationship.urls import url_path as user_relationship_app_urls

urlpatterns = [path("admin/", admin.site.urls), *user_app_urls, *user_relationship_app_urls]

# adds static file URIs in debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
