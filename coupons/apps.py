from django.apps import AppConfig



class CouponsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coupons'

    def ready(self):
     import coupons.signals  # Replace 'your_app' with your app name
