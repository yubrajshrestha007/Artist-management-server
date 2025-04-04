# /home/mint/Desktop/ArtistMgntBack/app/musics/services.py

import datetime
from django.db import connection, DatabaseError, IntegrityError
from app.core.models import Music, ArtistProfile
import uuid
from django.http import Http404


def get_raw_music_list_queries():
    """Retrieves a list of music records using raw SQL."""
    with connection.cursor() as cursor:
        query = f"""
            SELECT m.id, m.title, m.album_name, m.release_date, m.genre, a.id as artist_id, a.name as artist_name, m.created_by_id
            FROM {Music._meta.db_table} m
            LEFT JOIN {ArtistProfile._meta.db_table} a ON m.created_by_id = a.id;
        """
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        musics = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return musics


def get_raw_music_detail_queries(music_id):
    """Retrieves a single music record by ID using raw SQL."""
    with connection.cursor() as cursor:
        query = f"""
            SELECT m.id, m.title, m.album_name, m.release_date, m.genre, a.id as artist_id, a.name as artist_name, m.created_by_id
            FROM {Music._meta.db_table} m
            LEFT JOIN {ArtistProfile._meta.db_table} a ON m.created_by_id = a.id
            WHERE m.id = %s;
        """
        cursor.execute(query, (music_id,))
        columns = [col[0] for col in cursor.description]
        music = cursor.fetchone()
        if music:
            return dict(zip(columns, music))
        return None


def create_raw_music_queries(data, artist_profile_id):
    """Creates a new music record using raw SQL."""
    with connection.cursor() as cursor:
        insert_query = f"""
            INSERT INTO {Music._meta.db_table} (id, title, album_name, release_date, genre, created, modified, created_by_id, artist_id)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), %s, %s);
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
            artist_profile_id,
            artist_profile_id,
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
    """Updates an existing music record using raw SQL with improved safety and error handling."""
    try:
        with connection.cursor() as cursor:
            update_query = f"""
                UPDATE {Music._meta.db_table}
                SET title = %s, album_name = %s, release_date = %s, genre = %s, modified = NOW()
                WHERE id = %s;
            """

            release_date = data.get("release_date")
            if release_date:
                if isinstance(release_date, str):
                    # If it's a string, assume it's already in the correct format
                    pass
                elif isinstance(release_date, datetime):
                    # If it's a datetime object, format it
                    release_date = release_date.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    raise ValueError("release_date must be a string or a datetime object")

            params = (
                data["title"],
                data["album_name"],
                release_date,
                data["genre"],
                music_id,
            )

            cursor.execute(update_query, params)

            if cursor.rowcount == 0:
                return False, {"error": "No music record found with the given ID or no changes were made."}

            return True, {}

    except KeyError as e:
        return False, {"error": f"Missing required field: {e}"}
    except IntegrityError as e:
        return False, {"error": "Integrity error occurred during music update.", "detail": str(e)}
    except DatabaseError as e:
        return False, {"error": "A database error occurred during music update.", "detail": str(e)}
    except Exception as e:
        return False, {"error": "An unexpected error occurred during music update.", "detail": str(e)}
def delete_raw_music_queries(music_id):
    """Deletes a music record using raw SQL."""
    with connection.cursor() as cursor:
        delete_query = f"""
            DELETE FROM {Music._meta.db_table}
            WHERE id = %s;
        """
        cursor.execute(delete_query, (music_id,))
        return cursor.rowcount > 0
