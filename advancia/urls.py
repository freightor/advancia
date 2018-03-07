"""freightor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from accounts import views
from website import views as homepage


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", homepage.index, name="home"),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("employer/", include("employers.urls", namespace="employers")),
    path("payroll/", include("payroll.urls", namespace="payroll")),
    path("stores/", include("stores.urls", namespace="stores")),
    path("api/v1/", include("api.urls", namespace="api")),
    path("password_reset/", auth_views.password_reset, {
         "template_name": "accounts/password_reset.html"}, name="password_reset"),
    path("password_reset/done/", auth_views.password_reset_done,
         {"template_name": "accounts/password_reset_done.html"}, name="password_reset_done"),
    path("password_reset/confirm/", auth_views.password_reset_confirm,
         {"template_name": "accounts/password_reset_confirm.html"}, name="password_reset_confirm"),
    path("password_reset/complete/", auth_views.password_reset_complete,
         {"template_name": "accounts/password_reset_complete.html"}, name="password_reset_complete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
