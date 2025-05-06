from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path,include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema = get_schema_view(
    openapi.Info(
        title="LHMS API BACKEND",
        default_version="1.0.0",
        description="backend api"
    ),
    permission_classes= (AllowAny,),
)

# REDIRECT INDEX PAGE TO DOCS
def to_docs(request):
    return redirect("swagger")

urlpatterns = [
    path("",to_docs,name="index"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("Auth.urls")),
    path("swagger/docs/",schema.with_ui("swagger",cache_timeout=0),name="swagger"),
]
