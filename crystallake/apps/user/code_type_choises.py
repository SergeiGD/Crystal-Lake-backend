from enum import Enum

CODE_TYPE_CHOICES = (
    ('register', 'регистрация'),
    ('password_reset', 'сброс пароля')
)


class CodeType(Enum):
    register = 'регистрация'
    password_reset = 'сброс пароля'
