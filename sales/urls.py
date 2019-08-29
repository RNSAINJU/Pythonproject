from django.urls import path

from .views import employeeList

app_name="sales"

urlpatterns=[
        path('employees/',employeeList.as_view()),
        path('employees/<int:pk>',employeeList.as_view()),
        # path('employees/<int:pk>', employeelist)
    ]
