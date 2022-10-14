from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.JobsListView.as_view(), name='jobs_list_view'),
    path('bookmark/create/', views.JobseekerBookmarksCreateView.as_view(), name='joseeker_bookmark_create'),
    path('bookmark/delete/<int:id>/', views.JobseekerBookmarksDestroyView.as_view(), name='joseeker_bookmark_delete'),
    path('bookmarks/list/', views.JobseekerBookmarksListView.as_view(), name='jobseeker_bookmarks_list'),
    path('bookmarks/delete/', views.JobseekerBookmarksClearView.as_view(), name='jobseeker_bookmarks_clear'),
    
    # path('co/applications/<int:company_id>', views.CompanyApplicationsListView.as_view(), name='job_application_list_view_per_company'),
    # path('jobseeker/applications', views.JobseekerApplicationsListView.as_view(), name='job_application_list_view_per_user'),
]
