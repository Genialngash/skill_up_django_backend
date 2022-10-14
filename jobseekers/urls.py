from django.urls import path

from . import views
from .views import JobseekerProfessionalInfoView

urlpatterns = [
    path('', views.JobseekersListView.as_view(), name='jobseekers_list'),
    path('professional-info/', JobseekerProfessionalInfoView.as_view(), name='jobseeker_prof_info')
]
