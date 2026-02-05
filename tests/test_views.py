import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from angler.models import Fish, Catch

User = get_user_model()


@pytest.fixture
def user():
    """Fixture for User instance."""
    return User.objects.create_user(
        username="testangler", password="testpass123"
    )


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
def client():
    """Fixture for Django test client."""
    from django.test import Client

    return Client()


@pytest.mark.django_db
def test_log_catch_creates_new_fish_species(client, user):
    """Test that log_catch view creates a new fish species."""
    client.login(username="testangler", password="testpass123")
    catch_data = {
        "new_fish_species": "Trout",
        "length": "22.5",
        "length_unit": "cm",
        "weight": "1.2",
        "weight_unit": "kg",
        "catch_location": "Rocky Stream",
        "catch_datetime": timezone.now().isoformat(),
        "released": True,
        "is_public": True,
    }
    response = client.post("/log-catch/", catch_data)

    assert response.status_code == 200
    assert Fish.objects.filter(official_name="Trout").exists()

    trout = Fish.objects.get(official_name="Trout")
    catch = Catch.objects.filter(user=user, fish=trout).first()
    assert catch is not None


@pytest.mark.django_db
def test_log_catch_with_existing_fish(client, user, existing_fish):
    """Test that log_catch view works with existing fish species."""
    client.login(username="testangler", password="testpass123")
    catch_data = {
        "fish": existing_fish.id,
        "length": "25.5",
        "length_unit": "cm",
        "weight": "1.5",
        "weight_unit": "kg",
        "catch_location": "Lake Michigan",
        "catch_datetime": timezone.now().isoformat(),
        "released": True,
        "is_public": True,
    }
    response = client.post("/log-catch/", catch_data)  # Log catch with existing fish

    assert response.status_code == 200  # Check for successful response

    catch = Catch.objects.filter(
        user=user, fish=existing_fish
    ).first()  # Retrieve the catch
    assert catch is not None


@pytest.mark.django_db
def test_duplicate_fish_species_not_created(client, user):
    """Test that duplicate fish species are not created using get_or_create."""
    fish_count_before = Fish.objects.count()  # 0
    client.login(username="testangler", password="testpass123")

    catch_data_1 = {
        "new_fish_species": "Salmon",
        "length": "35.0",
        "length_unit": "cm",
        "weight": "3.0",
        "weight_unit": "kg",
        "catch_location": "River",
        "catch_datetime": timezone.now().isoformat(),
        "released": True,
        "is_public": True,
    }
    client.post("/log-catch/", catch_data_1)  # Log first catch

    catch_data_2 = {
        "new_fish_species": "Salmon",
        "length": "32.0",
        "length_unit": "cm",
        "weight": "2.8",
        "weight_unit": "kg",
        "catch_location": "River",
        "catch_datetime": timezone.now().isoformat(),
        "released": True,
        "is_public": True,
    }
    client.post("/log-catch/", catch_data_2)  # Log second catch with same species

    fish_count_after = Fish.objects.count()  # 1
    assert (
        fish_count_after - fish_count_before == 1
    )  # 1 species created. 2 would be duplicate
    assert (
        Catch.objects.filter(fish__official_name="Salmon").count() == 2
    )  # 2 catches logged
