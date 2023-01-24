from enum import Enum


STATUS_CHOICES = (
    ('process', 'в процессе'),
    ('canceled', 'отменен'),
    ('finished', 'завершен'),
)


# class syntax
class Status(Enum):
    process = 'в процессе'
    canceled = 'отменен'
    finished = 'завершен'


def get_status_by_name(name):
    for status in STATUS_CHOICES:
        if status[1] == name:
            return status[0]
    return 'unknown status'


def get_status_by_code(code):
    for status in STATUS_CHOICES:
        if status[0] == code:
            return status[1]
    return 'неизвестный статус'
