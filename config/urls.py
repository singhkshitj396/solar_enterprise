from django.contrib import admin
from django.urls import include, path


admin.site.site_header = "S.K Bright Solar Energy"
admin.site.site_title = "S.K Bright operations"
admin.site.index_title = "Branch and appointment management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
