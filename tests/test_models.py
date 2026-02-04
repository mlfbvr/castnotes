from datetime import datetime
from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from angler.models import Fish, Catch

User = get_user_model()


@pytest.fixture
def fish():
    """Fixture for Fish model instance."""
    return Fish.objects.create(
        official_name="Largemouth Bass",
        nicknames="Black bass, Florida bass",
        identifying_characteristics="Dark green/black coloring, large mouth",
        preferred_baits_lures="Worms, minnows, crankbaits",
        best_fishing_method="Casting to structures",
        preferred_environments="Lakes, ponds, rivers",
    )


@pytest.fixture
def user():
    """Fixture for User instance."""
    return User.objects.create_user(username="angler1", password="securepassword")


@pytest.fixture
def catch(user, fish):
    """Fixture for Catch model instance."""
    return Catch.objects.create(
        user=user,
        fish=fish,
        length=Decimal("30.5"),
        length_unit="cm",
        weight=Decimal("2.3"),
        weight_unit="kg",
        catch_location="Lake Springfield",
        catch_datetime=datetime.fromisoformat("2024-06-01T10:00:00+00:00"),
        released=True,
        is_public=True,
    )


@pytest.mark.django_db
def test_fish_str_representation(fish):
    """Test that Fish model returns official name as string representation."""
    assert str(fish) == "Largemouth Bass"


@pytest.mark.django_db
def test_fish_creation(fish):
    """Test that Fish model can be created and retrieved."""
    retrieved_fish = Fish.objects.get(official_name="Largemouth Bass")
    assert retrieved_fish.nicknames == "Black bass, Florida bass"
    assert "Dark green" in retrieved_fish.identifying_characteristics


@pytest.mark.django_db
def test_catch_creation(catch, fish, user):
    """Test that Catch model can be created and linked to Fish."""
    retrieved_catch = Catch.objects.get(fish=fish)
    assert retrieved_catch.length == Decimal("30.5")
    assert retrieved_catch.weight == Decimal("2.3")
    assert retrieved_catch.catch_location == "Lake Springfield"


@pytest.mark.django_db
def test_catch_str_representation(catch, fish, user):
    """Test that Catch model string representation works."""
    expected = f"{fish.official_name} caught by {user.username} on 2024-06-01 at 10:00"
    assert str(catch) == expected
