from django.conf import settings


def settings_context(request):
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", ""),
        "SITE_DOMAIN": getattr(settings, "SITE_DOMAIN", ""),
    }
