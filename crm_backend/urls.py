"""crm_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Swagger imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
      title="CognCise API",
      default_version='v1',
      description="CognCise Api's documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email=""),
      license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
]

api_urls = [
    path(
        "api/v1/",
        include(
            [
                path('companies/', include('company.urls.api_urls', namespace='company')),
                path('leads/',     include('lead.urls.api_urls',    namespace='lead')),
                path('jobs/',      include('job.urls.api_urls',     namespace='job')),
                path('',      include('core.urls.api_urls',    namespace='core')),
            ]

        )
    ),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


urlpatterns += api_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)