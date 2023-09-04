from django.urls import path, include
from .views import upload_csv, download_json

urlpatterns = [
    path("upload_csv_file/", upload_csv),
    path("download_json/", download_json)
]