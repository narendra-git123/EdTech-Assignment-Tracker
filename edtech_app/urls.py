from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('create-assignment/', views.create_assignment, name='create_assignment'),
    path('submit-assignment/', views.submit_assignment, name='submit_assignment'),
    path('view-submissions/', views.view_submissions, name='view_submissions'),
    path("create/", views.frontend_create),
    path("submit/", views.frontend_submit),
    path("view/", views.frontend_view),




]
