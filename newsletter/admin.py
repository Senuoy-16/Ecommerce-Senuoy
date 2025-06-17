from django.contrib import admin
from .models import Subscriber, EmailTemplate
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from ckeditor.fields import RichTextFormField


class EmailTemplateAdmin(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
        widgets = {
            'message':RichTextFormField(),
        }


class EmailTemplateAdmin(admin.ModelAdmin):
    form = EmailTemplateAdmin

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        subject      = obj.subject
        html_message = obj.message
        recipients   = [subscriber.email for subscriber in obj.recipients.all()]
        from_email   = settings.DEFAULT_FROM_EMAIL
        send_mail(
                subject,
                '',
                from_email,
                recipient_list=recipients,
                html_message=html_message,
                fail_silently=False,
            )

admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(Subscriber)








