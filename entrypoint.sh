#!/bin/sh
set -e

python floresta/manage.py migrate

echo "from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@floresta.com').exists():
    User.objects.create_superuser(email='admin@floresta.com', password='admin')
" | python floresta/manage.py shell

exec "$@"
