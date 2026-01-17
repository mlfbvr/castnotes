from django.db import models
from django.conf import settings


class Fish(models.Model):
    """Model representing a fish species."""

    official_name = models.CharField(max_length=100)
    nicknames = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated nicknames"
    )
    identifying_characteristics = models.TextField()
    preferred_baits_lures = models.TextField(help_text="Preferred baits and lures")
    best_fishing_method = models.CharField(max_length=100)
    preferred_environments = models.CharField(
        max_length=255, help_text="Comma-separated environments"
    )

    class Meta:
        verbose_name_plural = "Fish Species"
        verbose_name = "Fish Species"

    def __str__(self):
        return self.official_name


class Catch(models.Model):
    """Model representing an individual fish caught by a user."""

    fish = models.ForeignKey(Fish, on_delete=models.CASCADE, related_name="catches")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="catches"
    )
    LENGTH_UNIT_CHOICES = [
        ("cm", "Centimeters"),
        ("in", "Inches"),
    ]
    WEIGHT_UNIT_CHOICES = [
        ("kg", "Kilograms"),
        ("lbs", "Pounds"),
    ]

    length = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Length value"
    )
    length_unit = models.CharField(
        max_length=2, choices=LENGTH_UNIT_CHOICES, default="cm"
    )
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Weight value"
    )
    weight_unit = models.CharField(
        max_length=3, choices=WEIGHT_UNIT_CHOICES, default="kg"
    )
    catch_location = models.CharField(max_length=255)
    catch_datetime = models.DateTimeField()
    weather_conditions = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    released = models.BooleanField(
        default=True, help_text="Released (True) or kept (False)"
    )

    class Meta:
        verbose_name_plural = "Catches"
        verbose_name = "Catch"

    def __str__(self):
        return f"{self.fish} caught by {self.user} on {self.catch_datetime.strftime('%Y-%m-%d')}"
