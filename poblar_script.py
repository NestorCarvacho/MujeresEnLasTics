import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mujeresenlastics.settings')
django.setup()

# Aquí importamos el contenido del script de poblado
exec(open('poblar_bd.py').read())
