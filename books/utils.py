import re

from rest_framework import exceptions


def validate_review(data):
    try:
        validator = re.search(r"\S+", data, re.IGNORECASE)
        if not validator:
            raise exceptions.ValidationError({"error": "Review cannot be empty"})
        return data
    except:
        raise exceptions.ValidationError({"error": "Invalid data"})
