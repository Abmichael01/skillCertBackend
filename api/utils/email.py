from django.conf import settings
from djoser import email


class CustomActivationEmail(email.ActivationEmail):
    template_name = "email/activation.html"
    
    def get_context_data(self):
        context = super().get_context_data()
        context["frontend_url"] = settings.FRONTEND_URL
        context["site_name"] = "SkillCert"
        return context