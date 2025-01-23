#!/usr/bin/env python3
""" Module of Users views
"""


from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth class that inherits from Auth.
    For now, it doesn't add any extra functionality
    but can be extended in the future.
    """
    pass
