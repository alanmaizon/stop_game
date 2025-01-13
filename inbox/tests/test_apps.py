from django.apps import apps
from user.apps import UserConfig

def test_user_app_config():
    assert UserConfig.name == 'user'
    assert UserConfig.default_auto_field == 'django.db.models.BigAutoField'

def test_user_app_is_installed():
    assert apps.is_installed('user')