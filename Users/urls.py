from django.urls import path
from Users.views import register_user, login, logout, password_reset_request, password_reset_confirm, set_new_password,admin_login,admin_logout,user_list, user_detail, send_custom_email


urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login, name='login'),
    path('logout/',logout , name = 'logout'),
    path('password_reset/', password_reset_request, name='custom_password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='custom_password_reset_confirm'),
    path('set_new_password/<uidb64>/<token>/', set_new_password, name='set_new_password'),
    path('admin/login/', admin_login, name='admin_login'),
    path('admin/logout/', admin_logout, name='admin_logout'),
    path('admin/userlist/', user_list.as_view(), name='user-list'),
    path('admin/users/<int:user_id>/', user_detail.as_view(), name='user-detail'),
    path('admin/send_custom_email/', send_custom_email, name='send-custom_email' ),
    # Other URLs for user-related operations (profile update, etc.) can be added here
]
