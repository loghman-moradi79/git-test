from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "sabzwebapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('posts/<category>', views.posts, name='posts_category'),
    path('posts/detail/<pk>', views.post_detail, name='post_detail'),
    path('ticket/', views.ticket, name='ticket'),
    path('posts/<post_id>/comments', views.post_comment, name='post_comment'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.post_search, name='post_search'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit_post/<post_id>/', views.edit_post, name='edit_post'),
    path('profile/delete_post/<post_id>/', views.delete_post, name='delete_post'),
    path('profile/delete_image/<img_id>/', views.delete_image, name='delete_image'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='log_out'),
    path('register/', views.register, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url="done"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/sabzwebapp/password_reset/complete'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='change_password_done'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('posts/author_list/', views.authors_list, name='author_list'),
    path('posts/info_authors/<int:author_id>/', views.information_authors, name='information_authors'),


]


















