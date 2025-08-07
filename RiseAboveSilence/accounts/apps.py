from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "RiseAboveSilence.accounts"

    def ready(self):
        import RiseAboveSilence.accounts.signals
