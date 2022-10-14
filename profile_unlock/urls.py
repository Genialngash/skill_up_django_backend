from django.urls import path

from .views import UnlockProfileView

urlpatterns = [
    path('unlock/', UnlockProfileView.as_view(), name='unlock_contact'),
]
