from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView 

app_name = 'main'

urlpatterns = [
    # user login
    path("login/", LoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", HomeView.as_view(), name="home"),
    # teacher
    path("update_teacher/<pk>", TeacherUpdateView.as_view(), name="update_teacher"),
    path("delete_teacher/<pk>", TeacherDeleteView.as_view(), name="delete_teacher"),
    path("add_teacher/", TeacherCreateView.as_view(), name="add_teacher"),
    path("teachers/", TeachersView.as_view(), name="teachers"),
    path("pay_for_teacher/", pay_for_teacher, name="forteacher"),
    # students
    path("delete_student/<pk>", StudentDeleteView.as_view(), name="delete_student"),
    path("update_student/<pk>", StudentUpdateView.as_view(), name="update_student"),
    path("add_student/", create_student, name="add_student"),
    path("students/", StudentsView.as_view(), name="students"),
    path("student/<pk>", student_detail, name="student"),
    path("get_plus/", get_plus, name="get_plus"),
    path("pay/", pay, name="pay"),
    # groups
    path("delete_group/<pk>", GroupDeleteView.as_view(), name="delete_group"),
    path("update_group/<pk>", GroupUpdateView.as_view(), name="update_group"),
    path("groups/", GroupsView.as_view(), name="groups"),
    path("add_group/", create_group, name="add_group"),
    path("group/<pk>", group_detail, name="group"),
    path("history_group/<pk>", group_history, name="group_history"),
    path("new_groups/", NewGroupsView.as_view(), name="new_groups"),

    path("add_subject/", add_subject, name="add_subject"),
    path("add_camewith/", add_camewith, name="add_camewith"),
    path("brithdays/", brithdays, name="brithday"),
    path("faq/", FaqView.as_view(), name="faq"),
    path("call/", call, name="call"),
    path("active_group/<pk>", active_group, name="activate"),
]   