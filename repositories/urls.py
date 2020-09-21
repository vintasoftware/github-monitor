from django.urls import path

from .views import commit_list_view, repository_create_view

app_name = 'repositories'

urlpatterns = [
    path('api/commits/', commit_list_view, name='commits-list'),
    path('api/repositories/', repository_create_view, name='repositories-create'),
]
