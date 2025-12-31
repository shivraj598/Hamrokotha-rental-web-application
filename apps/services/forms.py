from django import forms
from .models import FindRoomRequest, ShiftHomeRequest, RoomRequestReply


class FindRoomRequestForm(forms.ModelForm):
    """Form for Find Room service requests - tenant posting a room ad."""
    
    class Meta:
        model = FindRoomRequest
        fields = [
            'title', 'name', 'email', 'phone',
            'property_type', 'district', 'preferred_areas',
            'budget_range', 'bedrooms', 'move_in_date',
            'duration_months', 'additional_requirements'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Looking for 2BHK in Baneshwor Area'
            }),
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
            'property_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'district': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'preferred_areas': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 2,
                'placeholder': 'e.g., Baneshwor, Koteshwor, Tinkune'
            }),
            'budget_range': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'min': 1,
                'max': 10
            }),
            'move_in_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'duration_months': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'min': 1,
                'max': 60
            }),
            'additional_requirements': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Any specific requirements like parking, pet-friendly, etc.'
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name'].initial = user.get_full_name()
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = getattr(user, 'phone_number', '')


class RoomRequestReplyForm(forms.ModelForm):
    """Form for landlords to reply to room requests."""
    
    class Meta:
        model = RoomRequestReply
        fields = ['message', 'property_link']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Write your reply... You can describe your property or ask questions.'
            }),
            'property_link': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
        }
    
    def __init__(self, *args, landlord=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['property_link'].required = False
        self.fields['property_link'].empty_label = "-- Select a property (optional) --"
        if landlord:
            from apps.properties.models import Property
            from apps.core.choices import PropertyStatus
            self.fields['property_link'].queryset = Property.objects.filter(
                owner=landlord,
                status=PropertyStatus.APPROVED
            )


class ShiftHomeRequestForm(forms.ModelForm):
    """Form for Shift Home service requests."""
    
    class Meta:
        model = ShiftHomeRequest
        fields = [
            'name', 'email', 'phone',
            'shift_type', 'property_size',
            'from_district', 'from_area', 'from_address',
            'to_district', 'to_area', 'to_address',
            'preferred_date', 'preferred_time', 'flexible_date',
            'has_heavy_items', 'needs_packing', 'special_items',
            'additional_notes'
        ]
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
            'shift_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'property_size': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'from_district': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'from_area': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Baneshwor'
            }),
            'from_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 2,
                'placeholder': 'Full address for pickup'
            }),
            'to_district': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'to_area': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Koteshwor'
            }),
            'to_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 2,
                'placeholder': 'Full address for delivery'
            }),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }),
            'preferred_time': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            }, choices=[
                ('', 'Select a time'),
                ('morning', 'Morning (6 AM - 10 AM)'),
                ('mid_morning', 'Mid Morning (10 AM - 12 PM)'),
                ('afternoon', 'Afternoon (12 PM - 4 PM)'),
                ('evening', 'Evening (4 PM - 7 PM)'),
            ]),
            'flexible_date': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-primary-600 focus:ring-primary-500 border-gray-300 rounded',
            }),
            'has_heavy_items': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-primary-600 focus:ring-primary-500 border-gray-300 rounded',
            }),
            'needs_packing': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-primary-600 focus:ring-primary-500 border-gray-300 rounded',
            }),
            'special_items': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 2,
                'placeholder': 'e.g., Piano, Aquarium, Antique furniture'
            }),
            'additional_notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Any additional information we should know'
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name'].initial = user.get_full_name()
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = getattr(user, 'phone_number', '')
