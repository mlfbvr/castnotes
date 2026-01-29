"""Forms for the angler app."""

from django import forms
from .models import Catch, Fish, FishingSession
from datetime import datetime


class CatchForm(forms.ModelForm):
    """Form for logging a new catch with all details."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.initial.get("session_uuid"):
            # No active session id found, removing session_uuid field
            del self.fields["session_uuid"]

    fish = forms.ModelChoiceField(
        queryset=Fish.objects.all(),
        label="Fish Species",
        empty_label="Select a fish species or create new",
        widget=forms.Select(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                "id": "id_fish_select",
            }
        ),
        required=False,
    )

    new_fish_species = forms.CharField(
        label="Add New Fish Species",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "Enter fish species name (if not in list)",
                "id": "id_new_fish_species",
            }
        ),
    )

    length = forms.DecimalField(
        label="Length",
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            }
        ),
    )

    length_unit = forms.ChoiceField(
        label="Length Unit",
        choices=Catch.LENGTH_UNIT_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            }
        ),
    )

    weight = forms.DecimalField(
        label="Weight",
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            }
        ),
    )

    weight_unit = forms.ChoiceField(
        label="Weight Unit",
        choices=Catch.WEIGHT_UNIT_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            }
        ),
    )

    catch_location = forms.CharField(
        label="Location",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "Where did you catch this fish?",
            }
        ),
    )

    catch_datetime = forms.DateTimeField(
        label="Date & Time",
        widget=forms.DateTimeInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                "type": "datetime-local",
            }
        ),
    )

    photo = forms.ImageField(
        label="Photo",
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            }
        ),
    )

    weather_conditions = forms.CharField(
        label="Weather Conditions",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                "rows": 3,
                "placeholder": "e.g., Sunny, 72°F, light breeze",
            }
        ),
    )

    notes = forms.CharField(
        label="Notes",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                "rows": 4,
                "placeholder": "Any additional notes about your catch...",
            }
        ),
    )

    released = forms.BooleanField(
        label="Released",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            }
        ),
        help_text="Check if released, uncheck if kept",
    )

    is_public = forms.BooleanField(
        label="Make Public",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            }
        ),
        help_text="Share this catch with other anglers",
    )

    session_uuid = forms.UUIDField(
        label="Fishing Session",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                "readonly": "readonly",
            }
        ),
    )

    class Meta:
        model = Catch
        fields = [
            "fish",
            "length",
            "length_unit",
            "weight",
            "weight_unit",
            "catch_location",
            "catch_datetime",
            "photo",
            "weather_conditions",
            "notes",
            "released",
            "is_public",
        ]

    def clean(self):
        """Validate that either an existing fish is selected or a new species name is provided."""
        cleaned_data = super().clean()
        fish = cleaned_data.get("fish")
        new_fish_species = cleaned_data.get("new_fish_species")

        if not fish and not new_fish_species:
            raise forms.ValidationError(
                "Please select an existing fish species or enter a new one."
            )

        if fish and new_fish_species:
            raise forms.ValidationError(
                "Please either select an existing fish species or enter a new one, not both."
            )

        return cleaned_data


class FishingSessionForm(forms.ModelForm):
    """Form for logging a fishing session."""

    start_datetime = forms.DateTimeField(
        label="Start Date & Time",
        initial=datetime.now,
        widget=forms.DateTimeInput(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                "type": "datetime-local",
            }
        ),
    )
    location = forms.CharField(
        label="Location",
        max_length=255,
        widget=forms.HiddenInput(),
    )

    weather_conditions = forms.CharField(
        label="Weather Conditions",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                "rows": 3,
                "placeholder": "e.g., Cloudy, 65°F, windy",
            }
        ),
    )

    class Meta:
        model = FishingSession
        fields = ["start_datetime", "location", "weather_conditions"]
