
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),  # admin 경로
    path("GivemeJson/<str:input_string>/", views.GivemeJson),  # GivemeJson 경로
    path("invest_chat/<str:invest_rank>/", views.invest_chat),  # invest_chat 경로
    path("tts/", views.tts),  # TTS 경로
]


