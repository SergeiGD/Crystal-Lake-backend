from enum import Enum


PRICE_CHOICES = (
        ('hour', 'час'),
        ('day', 'сутки'),
    )


class PriceType(Enum):
    hour = 'час'
    day = 'сутки'


