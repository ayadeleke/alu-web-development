#!/usr/bin/env python3
""" Module of Users views
"""

from api.v1.auth.auth import Auth
import uuid
import os
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class that inherits from Auth.
    Now includes session management.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """Returns a cookie value from a request.
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session / logout.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if (session_id is None or self.user_id_for_session_id(session_id)
                is None):
            return False
        del self.user_id_by_session_id[session_id]
        return True
