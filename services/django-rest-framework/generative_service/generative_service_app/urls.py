from django.urls import path

from generative_service_app import views

urlpatterns = [
    path('title/facts', views.TitleFacts.as_view())
]
