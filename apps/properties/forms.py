"""
Forms for property listings.
"""

from django import forms
from django.core.validators import MinValueValidator
from .models import Property, PropertyImage
from apps.core.choices import (
    District, PropertyType, KATHMANDU_AREAS, 
    BHAKTAPUR_AREAS, LALITPUR_AREAS, AMENITIES
)


class PropertyForm(forms.ModelForm):
    """Form for creating and editing property listings."""
    
    # Amenities as multiple checkboxes
    amenities = forms.MultipleChoiceField(
        choices=AMENITIES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
        }),
        required=False
    )
    
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 
            'district', 'area', 'address', 'google_maps_link',
            'price_per_month', 'negotiable', 'security_deposit',
            'bedrooms', 'bathrooms', 'floor_number', 'total_floors', 'area_sq_ft',
            'amenities', 'parking_available', 'pets_allowed',
            'preferred_tenant', 'available_from', 'minimum_stay_months'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Spacious 2BHK Apartment in Lazimpat'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 5,
                'placeholder': 'Describe the property in detail...'
            }),
            'property_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
            }),
            'district': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'x-model': 'district',
                '@change': 'updateAreas()'
            }),
            'area': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Lazimpat, Basundhara'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Full address with landmark'
            }),
            'google_maps_link': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'https://maps.google.com/...'
            }),
            'price_per_month': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '15000',
                'min': '1000'
            }),
            'negotiable': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
            }),
            'security_deposit': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '30000 (optional)'
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'min': '0',
                'max': '20'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'min': '1',
                'max': '10'
            }),
            'floor_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Ground, 1st, 2nd'
            }),
            'total_floors': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'min': '1',
                'max': '20'
            }),
            'area_sq_ft': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., 800'
            }),
            'parking_available': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
            }),
            'pets_allowed': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
            }),
            'preferred_tenant': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Family, Bachelor, Any'
            }),
            'available_from': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'type': 'date'
            }),
            'minimum_stay_months': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'min': '1',
                'max': '24'
            }),
        }
    
    def clean_price_per_month(self):
        price = self.cleaned_data.get('price_per_month')
        if price and price < 1000:
            raise forms.ValidationError("Monthly rent should be at least Rs. 1,000")
        return price
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 10:
            raise forms.ValidationError("Title should be at least 10 characters")
        return title


class PropertyImageForm(forms.ModelForm):
    """Form for property images."""
    
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm',
                'placeholder': 'Image caption (optional)'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary-600'
            })
        }


PropertyImageFormSet = forms.inlineformset_factory(
    Property,
    PropertyImage,
    form=PropertyImageForm,
    extra=4,
    max_num=10,
    can_delete=True
)


class PropertyFilterForm(forms.Form):
    """Form for filtering properties."""
    
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Search properties...'
        })
    )
    
    district = forms.ChoiceField(
        choices=[('', 'All Districts')] + list(District.choices),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
        })
    )
    
    property_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(PropertyType.choices),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
        })
    )
    
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Min Price'
        })
    )
    
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Max Price'
        })
    )
    
    bedrooms = forms.ChoiceField(
        choices=[
            ('', 'Any'),
            ('1', '1+'),
            ('2', '2+'),
            ('3', '3+'),
            ('4', '4+'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
        })
    )
    
    area = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'placeholder': 'Area name'
        })
    )
    
    sort = forms.ChoiceField(
        choices=[
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
            ('price_per_month', 'Price: Low to High'),
            ('-price_per_month', 'Price: High to Low'),
            ('-views_count', 'Most Viewed'),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
        })
    )
