from django.core.exceptions import ValidationError


def validate_username(value):
    """ Валидатор для username.
    Не допускает использование имени пользователя <me>.
    """
    if value in ['me', 'Me', 'mE', 'ME']:
        raise ValidationError(
            "Имя пользователя 'me' не допустимо для использования."
        )
    return value
