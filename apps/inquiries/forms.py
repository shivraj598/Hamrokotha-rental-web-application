from django import forms
from .models import Inquiry, InquiryMessage


class InquiryForm(forms.ModelForm):
    """Form for creating a new inquiry."""
    
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message', 'preferred_visit_date', 'preferred_visit_time']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '+977-98XXXXXXXX'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 5,
                'placeholder': 'I am interested in this property. Please provide more details about...'
            }),
            'preferred_visit_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'preferred_visit_time': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }, choices=[
                ('', 'Select a time'),
                ('morning', 'Morning (9 AM - 12 PM)'),
                ('afternoon', 'Afternoon (12 PM - 4 PM)'),
                ('evening', 'Evening (4 PM - 7 PM)'),
            ])
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill form if user is authenticated
        if user and user.is_authenticated:
            self.fields['name'].initial = user.get_full_name()
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = getattr(user, 'phone', '')


class InquiryMessageForm(forms.ModelForm):
    """Form for sending a message in an inquiry thread."""
    
    class Meta:
        model = InquiryMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Type your message...'
            })
        }


class InquiryFilterForm(forms.Form):
    """Form for filtering inquiries."""
    
    STATUS_CHOICES = [
        ('', 'All Status'),
        ('PENDING', 'Pending'),
        ('RESPONDED', 'Responded'),
        ('CLOSED', 'Closed'),
    ]
    
    READ_CHOICES = [
        ('', 'All'),
        ('unread', 'Unread Only'),
        ('read', 'Read Only'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES, 
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
        })
    )
    
    read_status = forms.ChoiceField(
        choices=READ_CHOICES, 
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
        })
    )
    
    property_id = forms.UUIDField(required=False, widget=forms.HiddenInput())
