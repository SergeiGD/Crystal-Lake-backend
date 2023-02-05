import uuid


def build_photo_path(instance, filename):
    """
    генерация пути для фотографий
    """
    ext = filename.split('.')[-1]
    code = uuid.uuid4()
    if hasattr(instance, 'offer'):      # если дополнительная фотография, то берем id из оффера
        return 'offer_{0}/{1}.{2}'.format(instance.offer.slug, code, ext)

    return 'offer_{0}/{1}.{2}'.format(instance.slug, code, ext)
