from django.urls import path, include
from django.contrib import admin
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.obtain_auth_token, name="obtain-auth-token"),
    path("list/", include('core.urls'), )
]
