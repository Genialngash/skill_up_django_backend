from django.urls import path

from .views import EmployeesListView

# app_name = 'establishments'

urlpatterns = [
    path('my-employees/', EmployeesListView.as_view(), name='employee_list_view'),
]
