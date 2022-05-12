from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
app_name = 'accounts'

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('profile/<username>', views.profile, name="profile"),
    path('edit-profile/<username>', views.edit_profile, name='edit_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password/password_reset_confirm.html",
             success_url=reverse_lazy("accounts:password_reset_complete")),
         name='password_reset_confirm'),

    path('reset/done/',
             auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
             name='password_reset_complete'),
]
