import datetime
from django.db import connection
import uuid
import datetime
from django.db import IntegrityError

def get_all_raw_user_profiles_queries():
    """
    Retrieves all user profiles from the database using raw SQL.

    Returns:
        list: A list of dictionaries, where each dictionary represents a user profile.
    """
    queries = []
    with connection.cursor() as cursor:
        query = f"""
            SELECT id, user_id, first_name, last_name, gender, date_of_birth, address, phone, created, modified
            FROM core_userprofile;
        """
        queries.append(query)
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        profiles = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return profiles

def get_raw_user_profile_list_queries(user_id):
    """
    Retrieves a list of user profiles associated with a specific user using raw SQL.

    Args:
        user_id (str): The ID of the user.

    Returns:
        list: A list of dictionaries, where each dictionary represents a user profile.
    """
    queries = []
    with connection.cursor() as cursor:
        query = f"""
            SELECT id, first_name, last_name, gender, date_of_birth, address, phone
            FROM core_userprofile
            WHERE user_id = %s;
        """
        queries.append(query)
        cursor.execute(query, (user_id,))
        columns = [col[0] for col in cursor.description]
        profiles = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return profiles


def get_raw_user_profile_detail_queries(user_id, profile_id):
    """
    Retrieves a single user profile using raw SQL.

    Args:
        user_id (str): The ID of the user.
        profile_id (str): The ID of the user profile.

    Returns:
        dict or None: A dictionary representing the user profile, or None if not found.
    """
    queries = []
    with connection.cursor() as cursor:
        query = f"""
            SELECT id, first_name, last_name, gender, date_of_birth, address, phone
            FROM core_userprofile
            WHERE user_id = %s AND id = %s;
        """
        queries.append(query)
        cursor.execute(query, (user_id, profile_id))
        columns = [col[0] for col in cursor.description]
        profile = cursor.fetchone()
        if profile:
            return dict(zip(columns, profile))
        return None



def create_raw_user_profile_queries(user_id, data):
    """
    Creates a new user profile using raw SQL.

    Args:
        user_id (str): The ID of the user.
        data (dict): The data for the new user profile.

    Returns:
        tuple: A tuple containing a boolean indicating success and a dictionary with error messages if any.
    """
    queries = []
    with connection.cursor() as cursor:
        insert_query = f"""
            INSERT INTO core_userprofile (id, user_id, first_name, last_name, gender, date_of_birth, address, phone, created, modified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW());
        """
        profile_id = uuid.uuid4()
        date_of_birth = data.get("date_of_birth")
        if date_of_birth:
            date_of_birth = date_of_birth.strftime("%Y-%m-%d")
        else:
            date_of_birth = None
        params = (
            profile_id,
            user_id,
            data.get("first_name"),
            data.get("last_name"),
            data.get("gender"),
            date_of_birth,
            data.get("address"),
            data.get("phone"),
        )
        queries.append(insert_query)
        try:
            cursor.execute(insert_query, params)
            return True, {"id": str(profile_id)}
        except IntegrityError as e:
            return False, {"error": "An error occurred during profile creation."}
        except Exception as e:
            return False, {"error": "An error occurred during profile creation."}
def update_raw_user_profile_queries(user_id, profile_id, data):
    """
    Updates an existing user profile using raw SQL.

    Args:
        user_id (str): The ID of the user.
        profile_id (str): The ID of the user profile to update.
        data (dict): The data to update the user profile with.

    Returns:
        tuple: A tuple containing a boolean indicating success and a dictionary with error messages if any.
    """
    queries = []
    with connection.cursor() as cursor:
        update_query = f"""
            UPDATE core_userprofile
            SET first_name = %s, last_name = %s, gender = %s, date_of_birth = %s, address = %s, phone = %s
            WHERE user_id = %s AND id = %s;
        """
        date_of_birth = data.get("date_of_birth")
        if date_of_birth:
            date_of_birth = date_of_birth.strftime("%Y-%m-%d")
        else:
            date_of_birth = None
        params = (
            data.get("first_name"),
            data.get("last_name"),
            data.get("gender"),
            date_of_birth,
            data.get("address"),
            data.get("phone"),
            user_id,
            profile_id,
        )
        queries.append(update_query)
        try:
            cursor.execute(update_query, params)
            return True, {}
        except IntegrityError as e:
            return False, {"error": "An error occurred during profile update."}


def delete_raw_user_profile_queries(user_id, profile_id):
    """
    Deletes a user profile using raw SQL.

    Args:
        user_id (str): The ID of the user.
        profile_id (str): The ID of the user profile to delete.

    Returns:
        bool: True if the profile was deleted, False otherwise.
    """
    queries = []
    with connection.cursor() as cursor:
        delete_query = f"""
            DELETE FROM core_userprofile
            WHERE user_id = %s AND id = %s;
        """
        queries.append(delete_query)
        cursor.execute(delete_query, (user_id, profile_id))
        return cursor.rowcount > 0
