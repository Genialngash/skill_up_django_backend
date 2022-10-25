import os
from unicodedata import name

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from establishments.views import (
        CompanyViewSet, 
        UserCompaniesListView,
        CoursesViewSet,
        LessonsViewSet,
        CompletedViewSet,
        EnrolmentViewSet,
        CheckerViewSet
)
from jobs.views import (
    AprroveJobApplicationViewSet,
    JobApplicationViewSet,
    JobCardViewSet,
)
from jobseekers import views as jobseekers_views
from notifications.views import NotificationUpdateViewSet
from payments import session_view
from profile_unlock.views import UnlockedProfilesListView
from rest_framework import routers
from users.views import DeleteUserAccountView


app_name = 'core'
router = routers.DefaultRouter()

# notification_update = NotificationUpdateViewSet.as_view({'patch': 'partial_update'})

router.register(
    r'notification/update',
    NotificationUpdateViewSet,
    basename='user_notification_update'
),

router.register(
    r'company', CompanyViewSet,
    basename='companies'
)

router.register(
    r'my-companies', UserCompaniesListView,
    basename='user-companies'
)

router.register(
    r'jobs/card', JobCardViewSet, 
    basename='job-card',
)

router.register(
    r'job-applications', JobApplicationViewSet, 
    basename='job-application',
)

# router.register(
#     r'job-application/approve', AprroveJobApplicationViewSet,
#     basename='approve-job-application'
# )

from employers.views import JobOfferViewSet
from jobseekers.views import (
    CertificationViewSet,
    JobOfferAcceptView,
    JobOffersListView,
    LanguageViewSet,
    WorkExperienceViewSet,
)

create_work_experience = WorkExperienceViewSet.as_view({'post': 'create'})
get_work_experience = WorkExperienceViewSet.as_view({'get': 'retrieve'})
update_work_experience = WorkExperienceViewSet.as_view({'put': 'update'})
destroy_work_experience = WorkExperienceViewSet.as_view({'delete': 'destroy'})

# Job Offers
create_job_offer = JobOfferViewSet.as_view({'post': 'create'})
delete_job_offer = JobOfferViewSet.as_view({'delete': 'destroy'})


# Jobseeker Profile
# router.register(
#     r'jobseeker/work-experience', WorkExperienceViewSet,
#     basename='jobseeker-work-experience'
# )

# router.register(
#     r'jobseeker/language', LanguageViewSet,
#     basename='jobseeker-language'
# )

# router.register(
#     r'jobseeker/certification', CertificationViewSet,
#     basename='jobseeker-certification'
# )

# Customize Titles
admin.site.site_header  =  "Veeta Administration"  
admin.site.site_title  =  "Veeta UK"
admin.site.index_title  =  "Administration"


urlpatterns = [
    path('products/unlock-packages/', session_view.PackagesListView.as_view(), name='packages_list_view'),
    path(
        'profile-unlocks/<str:unlock_code>/',
        UnlockedProfilesListView.as_view(),
        name='unlocked_profiles'
    ),
    path('user/account/delete/', DeleteUserAccountView.as_view(), name='delete_account'),

    # Seperation
    # path('jobseeker/languages/list/', jobseekers_views.JobseekerLanguagesListView.as_view(), name='languages_list'),
    # path('jobseeker/certifications/list/', jobseekers_views.JobseekerCertificationsListView.as_view(), name='certifications_list'),

    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('contact/', include('contact.urls')),
    path('companies/', include('establishments.urls')),
    path('jobs/', include('jobs.urls')),
    path('course/create', CoursesViewSet.as_view({'post': 'create'})),
    path('course/list', CoursesViewSet.as_view({'get': 'list'})),
    path('course/get/<str:pk>/', CoursesViewSet.as_view({'get': 'retrieve'})),
    path('lesson/create', LessonsViewSet.as_view({'post': 'create'})),
    path('lesson/list', LessonsViewSet.as_view({'get': 'list'})),
    path('lesson/get/<str:pk>/', LessonsViewSet.as_view({'get': 'retrieve'})),
    path('complete/create', CompletedViewSet.as_view({'post': 'create'})),
    path('complete/list', CompletedViewSet.as_view({'get': 'list'})),
    path('complete/get/<str:pk>/', CompletedViewSet.as_view({'get': 'retrieve'})),
    path('enrolment/create', EnrolmentViewSet.as_view({'post': 'create'})),
    path('enrolment/list', EnrolmentViewSet.as_view({'get': 'list'})),
    path('enrolment/get/<str:pk>/', EnrolmentViewSet.as_view({'get': 'retrieve'})),
    path('enrolment/get_by_course/<str:pk>/', EnrolmentViewSet.as_view({'get': 'course_retrieve'})),
    path('check/create', CheckerViewSet.as_view({'post': 'create'})),
    path('check/list', CheckerViewSet.as_view({'get': 'list'})),
    path('check/get/<str:pk>/', CheckerViewSet.as_view({'get': 'retrieve'})),

    path(r'job-offer/create/', create_job_offer, name='create_job_offer'),
    path(r'job-offer/delete/<int:pk>/', delete_job_offer, name='delete_job_offer'),

    path(
        r'work-experience/create/',
        create_work_experience,
        name='create_work_experience'
    ),
    path(
        r'work-experience/<int:pk>/',
        get_work_experience,
        name='get_work_experience'
    ),

    path(r'work-experience/update/<int:pk>/', update_work_experience, name='update_work_experience'),
    path(r'work-experience/delete/<int:pk>/', destroy_work_experience, name='destroy_work_experience'),

    path('jobseeker/offers/list/', JobOffersListView.as_view(), name='jobseeker_job_offers_list'),
    path(
        'jobseeker/offer/accept/<int:job_offer_id>/',
        JobOfferAcceptView.as_view(),
        name='jobseeker_accept_offer'
    ),
    
    path('jobseekers/', include('jobseekers.urls')),
    path('ratings/', include('ratings.urls')),
    path('payments/', include('payments.urls')),
    # path(
    #     r'notification/update/',
    #     notification_update,
    #     name='user_notification_update'
    # ),
    path('notifications/', include('notifications.urls')),
    path('profile/', include('profile_unlock.urls')),
    path('employer/', include('employers.urls')),
]


swagger_patterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if os.getenv('VEETA_ENV') == 'core.settings.dev':
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if os.getenv('VEETA_ENV') == 'core.settings.dev':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if os.getenv('VEETA_ENV') == 'core.settings.dev' or os.getenv('VEETA_ENV') == 'core.settings.staging':
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

if os.getenv('VEETA_ENV') == 'core.settings.dev' or  os.getenv('VEETA_ENV') == 'core.settings.staging':
    urlpatterns += swagger_patterns
