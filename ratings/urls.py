from django.urls import path

from .views import JobseekerRatingView

urlpatterns = [
    path('jobseeker/create/', JobseekerRatingView.as_view(), name='jobseeker_rating_create')
]
