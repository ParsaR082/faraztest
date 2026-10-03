from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'phone', 'city', 'project_type', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'interactable', 'id': 'fullName', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'interactable', 'id': 'phone', 'required': True}),
            'city': forms.TextInput(attrs={'class': 'interactable', 'id': 'city', 'required': True}),
            'project_type': forms.Select(attrs={'class': 'interactable', 'id': 'projectType', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'interactable', 'id': 'message', 'required': True}),
        }
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'phone': 'شماره تماس',
            'city': 'شهر / منطقه پروژه',
            'project_type': 'نوع پروژه',
            'message': 'توضیح کوتاه درباره وضعیت پروژه',
        }