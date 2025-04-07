from django.db import connection
from django.contrib.auth import get_user_model
from app.core.models import ArtistProfile, User, ManagerProfile  # Import User and ManagerProfile
import uuid
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def get_raw_artist_profile_list_queries():
    """Retrieves a list of artist profiles using raw SQL."""
    with connection.cursor() as cursor:
        query = f"""
            SELECT id, name, date_of_birth, gender, address, first_release_year, no_of_albums_released, manager_id_id, created, modified
            FROM {ArtistProfile._meta.db_table};
        """
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        artists = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return artists


def get_raw_artist_profile_detail_queries(artist_id):
    """Retrieves a single artist profile by ID using raw SQL."""
    with connection.cursor() as cursor:
        query = f"""
            SELECT id, name, date_of_birth, gender, address, first_release_year, no_of_albums_released, manager_id_id, created, modified
            FROM {ArtistProfile._meta.db_table}
            WHERE id = %s;
        """
        cursor.execute(query, (artist_id,))
        columns = [col[0] for col in cursor.description]
        artist = cursor.fetchone()
        if artist:
            return dict(zip(columns, artist))
        return None


def create_raw_artist_profile_queries(user_id, data):
    """Creates a new artist profile using raw SQL."""
    try:
        User.objects.get(id=user_id)  # Check if the user exists
    except (User.DoesNotExist, ValueError):  # Handle both DoesNotExist and invalid UUID format
        return False, {"error": "User does not exist."}

    with connection.cursor() as cursor:
        insert_query = f"""
            INSERT INTO {ArtistProfile._meta.db_table} (id, user_id, name, date_of_birth, gender, address, first_release_year, no_of_albums_released, manager_id_id, created, modified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW());
        """
        artist_id = uuid.uuid4()
        date_of_birth = data.get("date_of_birth")
        if date_of_birth:
            date_of_birth = date_of_birth.strftime("%Y-%m-%d")
        else:
            date_of_birth = None

        manager = data.get("manager")
        if manager:
            try:
                ManagerProfile.objects.get(id=manager)
            except (ManagerProfile.DoesNotExist, ValueError):
                return False, {"error": "Manager does not exist."}

        params = (
            artist_id,
            user_id,  # Use the UUID object here
            data.get("name"),
            date_of_birth,
            data.get("gender"),
            data.get("address"),
            data.get("first_release_year"),
            data.get("no_of_albums_released"),
            manager,
        )
        try:
            cursor.execute(insert_query, params)
            return True, {"id": str(artist_id)}
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            return False, {"error": "An error occurred during artist profile creation."}
        except Exception as e:
            print(f"Exception: {e}")
            return False, {"error": "An error occurred during artist profile creation."}


def update_raw_artist_profile_queries(artist_id, data):
    """Updates an existing artist profile using raw SQL."""
    with connection.cursor() as cursor:
        update_query = f"""
            UPDATE {ArtistProfile._meta.db_table}
            SET name = %s, date_of_birth = %s, gender = %s, address = %s, first_release_year = %s, no_of_albums_released = %s, manager_id_id = %s, modified = NOW()
            WHERE id = %s;
        """
        date_of_birth = data.get("date_of_birth")
        if date_of_birth:
            date_of_birth = date_of_birth.strftime("%Y-%m-%d")
        else:
            date_of_birth = None

        manager = data.get("manager_id_id")  # Corrected key name
        if manager:
            try:
                ManagerProfile.objects.get(id=manager)
            except ManagerProfile.DoesNotExist:
                return False, {"error": "Manager does not exist."}
            except ValueError:
                return False, {"error": "Invalid manager ID format."}
        else:
            manager = None

        params = (
            data.get("name"),
            date_of_birth,  # Correctly formatted date
            data.get("gender"),
            data.get("address"),
            data.get("first_release_year"),
            data.get("no_of_albums_released"),
            manager,
            artist_id,
        )
        try:
            cursor.execute(update_query, params)
            return True, {}
        except IntegrityError as e:
            return False, {"error": "An error occurred during artist profile update."}
        except Exception as e:
            return False, {"error": "An error occurred during artist profile update."}


def delete_raw_artist_profile_queries(artist_id):
    """Deletes an artist profile using raw SQL."""
    with connection.cursor() as cursor:
        delete_query = f"""
            DELETE FROM {ArtistProfile._meta.db_table}
            WHERE id = %s;
        """
        cursor.execute(delete_query, (artist_id,))
        return cursor.rowcount > 0


def get_raw_artist_profile_by_user_id_queries(user_id):
    """Retrieves an artist profile by user ID using raw SQL."""
    try:
        User.objects.get(id=user_id)
    except (User.DoesNotExist, ValueError):
        raise Http404("User does not exist.")

    with connection.cursor() as cursor:
        query = f"""
            SELECT id, name, date_of_birth, gender, address, first_release_year, no_of_albums_released, user_id, manager_id_id, created, modified
            FROM {ArtistProfile._meta.db_table}
            WHERE user_id = %s;
        """
        cursor.execute(query, (user_id,))
        columns = [col[0] for col in cursor.description]
        artist = cursor.fetchone()
        if artist:
            return dict(zip(columns, artist))
        else:
            raise Http404("Artist profile not found for this user.")
