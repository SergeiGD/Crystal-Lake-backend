#!/bin/sh
docker exec -it crystal_lake_app sh -c 'echo "from apps.user.models import CustomUser; CustomUser.objects.create_superuser('\'$1\'', '\'$2\'')" | python3 manage.py shell'