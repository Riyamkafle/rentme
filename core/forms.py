# forms.py
from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'location', 'price', 'bedrooms', 'bathrooms', 'image', 'available_for_rent']

    widgets = {
        'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500'}),
        'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500'}),
        'location': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500'}),
        'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500'}),
        'bedrooms': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500'}),
        'bathrooms': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500'}),
        'image': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500'}),
        'available_for_rent': forms.CheckboxInput(attrs={'class': 'mr-2'}),
    }
