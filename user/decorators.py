from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'Admin', login_url='user:login')

def player_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'Player', login_url='user:login')
