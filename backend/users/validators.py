import re
from django.core.exceptions import ValidationError


def validate_username(value):
    """ Валидатор для username.
    Не допускает использование имени пользователя <me>.
    """
    if re.match(r'^[Mm][Ee]$', value):
        raise ValidationError(
            "Имя пользователя 'me'(вне зависимости от регистра) не допустимо."
        )
    return value
