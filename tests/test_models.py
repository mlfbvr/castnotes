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


@pytest.fixture
def session(user):
    """Fixture for FishingSession model instance."""
    from angler.models import FishingSession

    return FishingSession.objects.create(
        user=user,
        start_datetime=datetime.fromisoformat("2024-06-01T09:00:00+00:00"),
        end_datetime=datetime.fromisoformat("2024-06-01T11:00:00+00:00"),
        location="45,-73",
        weather_conditions="Sunny, light breeze",
    )


@pytest.fixture
def catch_with_session(user, fish, session):
    """Fixture for Catch model instance linked to a fishing session."""
    from angler.models import FishingSession

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
        session=session,
    )


@pytest.fixture
def catch_without_session(user, fish):
    """Fixture for Catch model instance without a fishing session."""
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
def test_fish_str_representation_is_fish_official_name(fish):
    """Test that Fish model returns official name as string representation."""
    assert str(fish) == fish.official_name


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


@pytest.mark.django_db
def test_catch_with_session_can_be_submitted(catch_with_session):
    """Test that Catch can be linked to a FishingSession."""
    assert catch_with_session.session is not None
    assert catch_with_session.session.location == "45,-73"
    assert catch_with_session.fish is not None
    assert catch_with_session.length == Decimal("30.5")
    assert catch_with_session.weight == Decimal("2.3")
    assert catch_with_session.catch_location == "Lake Springfield"
    assert catch_with_session.released is True
    assert catch_with_session.is_public is True
    assert catch_with_session.catch_datetime == datetime.fromisoformat(
        "2024-06-01T10:00:00+00:00"
    )
    assert catch_with_session.save() is None  # Should save with errors


@pytest.mark.django_db
def test_catch_without_session_can_be_submitted(catch_without_session):
    """Test that a catch without a fishing session can be created."""
    assert catch_without_session.session is None
    assert catch_without_session.fish is not None
    assert catch_without_session.length == Decimal("30.5")
    assert catch_without_session.weight == Decimal("2.3")
    assert catch_without_session.catch_location == "Lake Springfield"
    assert catch_without_session.released is True
    assert catch_without_session.is_public is True
    assert catch_without_session.catch_datetime == datetime.fromisoformat(
        "2024-06-01T10:00:00+00:00"
    )
    assert catch_without_session.save() is None  # Should save without errors


@pytest.mark.django_db
def test_fishing_session_str_representation(session, user):
    """Test that FishingSession model string representation works."""
    longitude, latitude = session.location.split(",")
    assert longitude == "45"
    assert latitude == "-73"
    expected = f"Fishing session started by {user.username} at ({float(longitude)}, {float(latitude)}) on 2024-06-01 at 09:00"
    assert str(session) == expected
