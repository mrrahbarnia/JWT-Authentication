from django.urls import path

from . import apis

urlpatterns = [
    path('register/', apis.RegisterApiView.as_view(), name='register'),
    path('login/', apis.LoginApiView.as_view(), name='login'),
    path('my-profile/', apis.MyProfileApiView.as_view(), name='my_profile'),
    path('list-users/', apis.ListUsersApiView.as_view(), name='list_users'),
    path('change-role/<int:id>/', apis.ChangeRolesApiView.as_view(), name='change_role')
]
