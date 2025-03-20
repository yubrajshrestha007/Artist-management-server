import datetime
from django.db import connection
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError


def get_raw_login_queries(email, password):
    queries = []
    user = None  # Initialize user to None
    with connection.cursor() as cursor:
        user_query = f"""
            SELECT id, password, email, role FROM {get_user_model()._meta.db_table}
            WHERE email = %s;
        """
        queries.append(user_query)
        cursor.execute(user_query, (email,))
        user_data = cursor.fetchone()

        if user_data:
            user_id, hashed_password, user_email, user_role = user_data
            if check_password(password, hashed_password):
                # Password is correct, create a user object
                User = get_user_model()
                user = User(id=user_id, email=user_email, role=user_role)
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
            FROM {get_user_model()._meta.db_table};
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
        params = (
            data.get("email"),
            data.get("is_staff"),
            data.get("is_active"),
            data.get("role"),
            user_id,
        )
        try:
            cursor.execute(update_query, params)
            return True, {}
        except IntegrityError as e:
            return False, {"error": "An error occurred during user update."}

def delete_raw_user_queries(user_id):
    """Deletes a user using raw SQL."""
    with connection.cursor() as cursor:
        delete_query = f"""
            DELETE FROM {get_user_model()._meta.db_table}
            WHERE id = %s;
        """
        cursor.execute(delete_query, (user_id,))
        return cursor.rowcount > 0
