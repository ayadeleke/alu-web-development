#!/usr/bin/env python3
"""Create a class to manage the API authentication."""
from flask import request
from typing import TypeVar, List


class Auth:
    """_summary_
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """_summary_

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: _description_
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        path = path + '/' if path[-1] != '/' else path
        excluded_paths = [p + '/' if p[-1] != '/' else
                          p for p in excluded_paths]
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """_summary_

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            str: _description_
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None  # No header
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_

        Returns:
            _type_: _description_
        """
        return None
