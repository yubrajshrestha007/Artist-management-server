# /home/mint/Desktop/ArtistMgntBack/app/musics/services.py

from django.db import connection
from app.core.models import Music, ArtistProfile, User  # Import User
import uuid
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


def get_raw_music_list_queries():
    """Retrieves a list of music records using raw SQL."""
    with connection.cursor() as cursor:
        query = f"""
            SELECT m.id, m.title, m.album_name, m.release_date, m.genre, a.id as artist_id, a.name as artist_name, m.created_by_id  -- Changed here
            FROM {Music._meta.db_table} m
            LEFT JOIN {ArtistProfile._meta.db_table} a ON m.created_by_id = a.id; -- Changed here
        """
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        musics = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return musics


def get_raw_music_detail_queries(music_id):
    """Retrieves a single music record by ID using raw SQL."""
    with connection.cursor() as cursor:
        query = f"""
            SELECT m.id, m.title, m.album_name, m.release_date, m.genre, a.id as artist_id, a.name as artist_name, m.created_by_id  -- Changed here
            FROM {Music._meta.db_table} m
            LEFT JOIN {ArtistProfile._meta.db_table} a ON m.created_by_id = a.id -- Changed here
            WHERE m.id = %s;
        """
        cursor.execute(query, (music_id,))
        columns = [col[0] for col in cursor.description]
        music = cursor.fetchone()
        if music:
            return dict(zip(columns, music))
        return None


def create_raw_music_queries(data, created_by_id):  # Changed here
    """Creates a new music record using raw SQL."""
    try:
        ArtistProfile.objects.get(id=created_by_id)  # Check if the artist exists
    except ArtistProfile.DoesNotExist:
        return False, {"error": "Artist does not exist."}
    with connection.cursor() as cursor:
        insert_query = f"""
            INSERT INTO {Music._meta.db_table} (id, title, album_name, release_date, genre, created, modified, created_by_id, artist_id)  -- Changed here
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), %s, %s);  -- Changed here
        """
        music_id = uuid.uuid4()
        release_date = data.get("release_date")
        if release_date:
            release_date = release_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            release_date = None
        params = (
            music_id,
            data.get("title"),
            data.get("album_name"),
            release_date,
            data.get("genre"),
            created_by_id,
            created_by_id,
        )
        try:
            cursor.execute(insert_query, params)
            return True, {"id": str(music_id)}
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            return False, {"error": "An error occurred during music creation."}
        except Exception as e:
            print(f"Exception: {e}")
            return False, {"error": "An error occurred during music creation."}


def update_raw_music_queries(music_id, data):
    """Updates an existing music record using raw SQL."""
    with connection.cursor() as cursor:
        update_query = f"""
            UPDATE {Music._meta.db_table}
            SET title = %s, album_name = %s, release_date = %s, genre = %s, modified = NOW()  -- Changed here
            WHERE id = %s;
        """
        release_date = data.get("release_date")
        if release_date:
            release_date = release_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            release_date = None
        params = (
            data.get("title"),
            data.get("album_name"),
            release_date,
            data.get("genre"),
            music_id,
        )
        try:
            cursor.execute(update_query, params)
            return True, {}
        except IntegrityError as e:
            return False, {"error": "An error occurred during music update."}
        except Exception as e:
            return False, {"error": "An error occurred during music update."}


def delete_raw_music_queries(music_id):
    """Deletes a music record using raw SQL."""
    with connection.cursor() as cursor:
        delete_query = f"""
            DELETE FROM {Music._meta.db_table}
            WHERE id = %s;
        """
        cursor.execute(delete_query, (music_id,))
        return cursor.rowcount > 0
