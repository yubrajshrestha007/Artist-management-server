from django.db import connection, IntegrityError, transaction, DatabaseError
from django.contrib.auth import get_user_model
from app.core.models import UserProfile, ArtistProfile, ManagerProfile  # Import related models
import datetime
from django.db import connection
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
from django.db import connection, IntegrityError, DatabaseError
from django.contrib.auth import get_user_model
from django.db import transaction



def get_raw_login_queries(email, password):
    """
    Retrieves a user from the database by email and verifies the password using raw SQL.

    Args:
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        User or None: The User object if the credentials are valid, None otherwise.
    """
    queries = []
    user = None  # Initialize user to None
    with connection.cursor() as cursor:
        user_query = f"""
            SELECT id, password, email, role, is_staff, is_active, is_superuser FROM {get_user_model()._meta.db_table}
            WHERE email = %s;
        """
        queries.append(user_query)
        cursor.execute(user_query, (email,))
        user_data = cursor.fetchone()

        if user_data:
            user_id, hashed_password, user_email, user_role, is_staff, is_active, is_superuser = user_data
            if check_password(password, hashed_password):
                # Password is correct, create a user object
                User = get_user_model()
                user = User(id=user_id, email=user_email, role=user_role, is_staff=is_staff, is_active=is_active, is_superuser=is_superuser)
                user.password = hashed_password
            else:
                user = None
        else:
            pass

    return user


def get_raw_register_queries(email, password, role):
    queries = []
    with connection.cursor() as cursor:
        # Simulate the registration process
        # 1. Check if the email already exists
        email_check_query = f"""
            SELECT 1 FROM {get_user_model()._meta.db_table}
            WHERE email = %s;
        """
        queries.append(email_check_query)
        cursor.execute(email_check_query, (email,))
        email_exists = cursor.fetchone()

        if not email_exists:
            # 3. Insert the new user into the database
            insert_user_query = f"""
                INSERT INTO {get_user_model()._meta.db_table} (id, email, password, is_staff, is_active, date_joined, role, created, modified, is_superuser)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            user_id = uuid.uuid4()
            hashed_password = make_password(password)  # Hash the password
            is_staff = False
            is_active = True
            is_superuser = False  # Add this line

            date_joined = timezone.now()
            created = timezone.now()
            modified = timezone.now()

            params = (
                user_id,
                email,
                hashed_password,
                is_staff,
                is_active,
                date_joined,
                role,
                created,
                modified,
                is_superuser,
            )
            queries.append(insert_user_query)
            try:
                cursor.execute(insert_user_query, params)
                return True, {"id": str(user_id)}  # Registration successful
            except IntegrityError as e:
                return False, {"error": "An error occurred during registration."}
        else:
            return False, {"email": ["This email already exists."]}


def get_raw_user_list_queries():
    with connection.cursor() as cursor:
        query = f"""
            SELECT id, email, is_staff, is_active, date_joined, role
            FROM {get_user_model()._meta.db_table}
            WHERE role!='super_admin';
        """
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        users = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return users

def get_raw_user_detail_queries(user_id):
    with connection.cursor() as cursor:
        query = f"""
            SELECT id, email, is_staff, is_active, date_joined, role
            FROM {get_user_model()._meta.db_table}
            WHERE id = %s;
        """
        cursor.execute(query, (user_id,))
        columns = [col[0] for col in cursor.description]
        user = cursor.fetchone()
        if user:
            return dict(zip(columns, user))
        return None

def update_raw_user_queries(user_id, data):
    """Updates an existing user using raw SQL."""
    with connection.cursor() as cursor:
        update_query = f"""
            UPDATE {get_user_model()._meta.db_table}
            SET email = %s, is_staff = %s, is_active = %s, role = %s, modified = NOW()
            WHERE id = %s;
        """
        staff = data.get("is_staff", False)
        params = (
            data.get("email"),
            staff,
            data.get("is_active"),
            data.get("role"),
            user_id,
        )
        try:
            cursor.execute(update_query, params)
            return True, {}
        except IntegrityError as e:
            return False, {"error": "An error occurred during user update."}


from django.db import connection, IntegrityError, transaction, DatabaseError
from django.contrib.auth import get_user_model
from app.core.models import ArtistProfile, ManagerProfile  # Import related models

from django.db import connection, IntegrityError, transaction, DatabaseError
from django.contrib.auth import get_user_model
from django.contrib.admin.models import LogEntry
from app.core.models import UserProfile, ArtistProfile, ManagerProfile  # Import related models

def delete_raw_user_queries(user_id):
    """Deletes a user and their related records using raw SQL."""
    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                # 1. Check if the user exists
                user_exists_query = f"""
                    SELECT 1 FROM {get_user_model()._meta.db_table}
                    WHERE id = %s;
                """
                cursor.execute(user_exists_query, (user_id,))
                if not cursor.fetchone():
                    return False, {"error": "User not found."}

                # 2. Delete related django_admin_log records
                delete_admin_log_query = f"""
                    DELETE FROM {LogEntry._meta.db_table}
                    WHERE user_id = %s;
                """
                cursor.execute(delete_admin_log_query, (user_id,))

                # 3. Delete related UserProfile records
                delete_user_profile_query = f"""
                    DELETE FROM {UserProfile._meta.db_table}
                    WHERE user_id = %s;
                """
                cursor.execute(delete_user_profile_query, (user_id,))

                # 4. Delete related ArtistProfile records
                delete_artist_profile_query = f"""
                    DELETE FROM {ArtistProfile._meta.db_table}
                    WHERE user_id = %s;
                """
                cursor.execute(delete_artist_profile_query, (user_id,))

                # 5. Delete related ManagerProfile records
                delete_manager_profile_query = f"""
                    DELETE FROM {ManagerProfile._meta.db_table}
                    WHERE user_id = %s;
                """
                cursor.execute(delete_manager_profile_query, (user_id,))

                # 6. Delete the user
                delete_user_query = f"""
                    DELETE FROM {get_user_model()._meta.db_table}
                    WHERE id = %s;
                """
                cursor.execute(delete_user_query, (user_id,))

                # Check if the user was actually deleted
                if cursor.rowcount > 0:
                    return True, {}  # Deletion successful
                else:
                    return False, {"error": "User not found."}

    except (IntegrityError, DatabaseError) as e:
        return False, {"error": "An error occurred during user deletion.", "detail": str(e)}
    except Exception as e:
        return False, {"error": "An unexpected error occurred.", "detail": str(e)}
