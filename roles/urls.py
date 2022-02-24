from django.urls import path

from .views import (
    BusinessRegistration,
    ClassListView,
    ClassRegistration,
    StudentListView,
    StudentRegistration,
    TeacherListView,
    TeacherRegistration,
)

app_name = "roles"

urlpatterns = [
    path("teacher/create/", TeacherRegistration.as_view(), name="teacher_registration"),
    path("teacher/list/", TeacherListView.as_view(), name="teachers_list"),
    path("student/create/", StudentRegistration.as_view(), name="student_registration"),
    path("class/create/", ClassRegistration.as_view(), name="class_registration"),
    path(
        "business/create/", BusinessRegistration.as_view(), name="business_registration"
    ),
    # path("teachers/", MinisterListView.as_view(), name='ministers'),
    path("students/", StudentListView.as_view(), name="students"),
    path("classes/", ClassListView.as_view(), name="classes"),
]
