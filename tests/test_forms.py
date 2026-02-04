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


@pytest.mark.django_db
def test_catch_form_requires_fish_or_new_species():
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
