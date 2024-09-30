from django.urls import path

from tests import views

urlpatterns = [
    path("block", views.BlockView.as_view(), name="block"),
]
