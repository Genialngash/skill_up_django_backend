from django.urls import path

from . import views

urlpatterns = [
    path('verify', views.GetContactVerificationCode.as_view(), name='verify_contact'),
    path('verify/confirm', views.ConfirmContactVerificationView.as_view(), name='confirm_verify_contact'),
]
