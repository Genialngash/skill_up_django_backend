from django.urls import path

from . import views

urlpatterns = [
    path('jobcards/list/', views.EmployerListAllJobCardsView.as_view(), name='all_jobcards_list_view'),
    # path('jobcards/<int:company_id>/', views.EmployerJobCardListView.as_view(), name='employer_jobcards'),
    path('job/applications/<int:job_card_id>/', views.EmployerJobApplicationsListView.as_view(), name='employer_jobcard_applications'),
]
