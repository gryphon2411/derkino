from django.urls import path

from generative_service_app import views

urlpatterns = [
    path('title/<str:title_id>/facts', views.TitleFacts.as_view())
]
