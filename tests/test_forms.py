from decimal import Decimal
import pytest
from django.utils import timezone
from angler.models import Fish
from angler.forms import CatchForm


@pytest.fixture
def existing_fish():
    """Fixture for existing Fish instance."""
    return Fish.objects.create(
        official_name="Bass",
        identifying_characteristics="Striped body",
        preferred_baits_lures="Worms, small fish",
        best_fishing_method="Casting",
        preferred_environments="Lakes, rivers",
    )


@pytest.fixture
def user():
    """Fixture for User instance."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(username="testangler", password="testpass123")


@pytest.fixture
def existing_session(user):
    """Fixture for existing FishingSession instance."""
    from angler.models import FishingSession

    return FishingSession.objects.create(
        user=user,
        start_datetime=timezone.now(),
        end_datetime=timezone.now(),
        location="45,-73",
        weather_conditions="Sunny, light breeze",
    )


# Catch tests
@pytest.mark.django_db
def test_catch_form_no_session_requires_fish_or_new_species():
    """Test that form requires either existing fish or new species."""
    form_data = {
        "length": Decimal("25.5"),
        "length_unit": "cm",
        "weight": Decimal("1.5"),
        "weight_unit": "kg",
        "catch_location": "Lake Michigan",
        "catch_datetime": timezone.now(),
        "released": True,
        "is_public": True,
    }
    form = CatchForm(data=form_data)
    assert not form.is_valid()
    assert "Please select an existing fish species" in str(form.errors)


@pytest.mark.django_db
def test_catch_form_with_session_requires_fish_or_new_species(existing_session):
    """Test that form with session requires either existing fish or new species."""
    form_data = {
        "session_uuid": existing_session.uuid,
        "length": Decimal("25.5"),
        "length_unit": "cm",
        "weight": Decimal("1.5"),
        "weight_unit": "kg",
        "catch_location": existing_session.location,
        "catch_datetime": timezone.now(),
        "released": True,
        "is_public": True,
    }
    form = CatchForm(data=form_data)
    assert not form.is_valid()
    assert "Please select an existing fish species" in str(form.errors)


@pytest.mark.django_db
def test_catch_form_accepts_existing_fish(existing_fish):
    """Test that form accepts existing fish species."""
    form_data = {
        "fish": existing_fish.id,
        "length": Decimal("25.5"),
        "length_unit": "cm",
        "weight": Decimal("1.5"),
        "weight_unit": "kg",
        "catch_location": "Lake Michigan",
        "catch_datetime": timezone.now(),
        "released": True,
        "is_public": True,
    }
    form = CatchForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_catch_form_accepts_new_fish_species():
    """Test that form accepts new fish species."""
    form_data = {
        "new_fish_species": "Pike",
        "length": Decimal("30.0"),
        "length_unit": "cm",
        "weight": Decimal("2.0"),
        "weight_unit": "kg",
        "catch_location": "Lake Superior",
        "catch_datetime": timezone.now(),
        "released": True,
        "is_public": True,
    }
    form = CatchForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_catch_form_rejects_both_fish_and_new_species(existing_fish):
    """Test that form rejects both existing and new species being filled."""
    form_data = {
        "fish": existing_fish.id,
        "new_fish_species": "Pike",
        "length": Decimal("25.5"),
        "length_unit": "cm",
        "weight": Decimal("1.5"),
        "weight_unit": "kg",
        "catch_location": "Lake Michigan",
        "catch_datetime": timezone.now(),
        "released": True,
        "is_public": True,
    }
    form = CatchForm(data=form_data)
    assert not form.is_valid()
    assert "either select an existing" in str(form.errors)


@pytest.mark.django_db
def test_catch_form_rejects_missing_length():
    """Test that form rejects missing length."""
    form_data = {
        "new_fish_species": "Pike",
        "weight": Decimal("2.0"),
        "weight_unit": "kg",
        "length_unit": "cm",
        "catch_location": "Lake Superior",
        "catch_datetime": timezone.now(),
        "released": True,
        "is_public": True,
    }
    form = CatchForm(data=form_data)
    assert not form.is_valid()
    assert "This field is required." in str(form.errors)


@pytest.mark.django_db
def test_catch_form_rejects_missing_weight():
    """Test that form rejects missing weight."""
    form_data = {
        "new_fish_species": "Pike",
        "weight_unit": "kg",
        "length": Decimal("2.0"),
        "length_unit": "cm",
        "catch_location": "Lake Superior",
        "catch_datetime": timezone.now(),
        "released": True,
        "is_public": True,
    }
    form = CatchForm(data=form_data)
    assert not form.is_valid()
    print(form.errors)
    assert "This field is required." in str(form.errors)


@pytest.mark.django_db
def test_catch_form_with_session_location_is_session_location(existing_session):
    """Test that form with session uses session location."""
    form_data = {
        "session_uuid": existing_session.uuid,
        "new_fish_species": "Pike",
        "length": Decimal("25.5"),
        "length_unit": "cm",
        "weight": Decimal("1.5"),
        "weight_unit": "kg",
        "catch_location": existing_session.location,
        "catch_datetime": timezone.now(),
        "released": True,
        "is_public": True,
    }
    form = CatchForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data["catch_location"] == existing_session.location


@pytest.mark.django_db
def test_catch_form_has_all_fields_from_model():
    """Test that form includes all fields from Catch model."""
    form = CatchForm()
    expected_fields = {
        "fish",
        "new_fish_species",
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
    }
    assert set(form.fields.keys()) == expected_fields
