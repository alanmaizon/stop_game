from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views
from .forms import CustomPasswordResetForm

app_name = 'user'

urlpatterns = [
    # Registration and Login
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),

    # Password Reset Workflow
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='user/password_reset_form.html',
            email_template_name='user/password_reset_email.html',
            success_url=reverse_lazy('user:password_reset_done'),
            form_class=CustomPasswordResetForm
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='user/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='user/password_reset_confirm.html',
            success_url=reverse_lazy('user:password_change_done')
        ),
        name='password_reset_confirm'
    ),

    # Password Change Workflow (For Logged-In Users)
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='user/password_change_form.html',
            success_url=reverse_lazy('user:password_change_done')
        ),
        name='password_change'
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='user/password_change_done.html'
        ),
        name='password_change_done'
    ),
]