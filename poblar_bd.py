from django.contrib.auth.models import User, Group
from codeandblogv1.models import BloqueEditable

# Crear grupos
admin_group, _ = Group.objects.get_or_create(name='admin')
estudiante_group, _ = Group.objects.get_or_create(name='estudiante')

# Crear usuarios
admin = User.objects.create_user(username='admin', password='admin123', is_superuser=True, is_staff=True)
admin.groups.add(admin_group)

est1 = User.objects.create_user(username='estudiante1', password='est12345')
est1.groups.add(estudiante_group)
est2 = User.objects.create_user(username='estudiante2', password='est12345')
est2.groups.add(estudiante_group)
est3 = User.objects.create_user(username='estudiante3', password='est12345')
est3.groups.add(estudiante_group)
est4 = User.objects.create_user(username='estudiante4', password='est12345')
est4.groups.add(estudiante_group)

# Crear publicaciones de ejemplo
BloqueEditable.objects.create(nombre='Inicio', contenido_html='<h2>Bienvenida</h2><p>Este es el inicio del blog.</p>', estilos_css='h2{color:blue;}', usuario_creador=admin, usuario_modificacion=admin)
BloqueEditable.objects.create(nombre='Python', contenido_html='<h2>Python</h2><p>Lenguaje de programación popular.</p>', estilos_css='h2{color:green;}', usuario_creador=est1, usuario_modificacion=est1)
BloqueEditable.objects.create(nombre='Django', contenido_html='<h2>Django</h2><p>Framework web para Python.</p>', estilos_css='h2{color:purple;}', usuario_creador=est2, usuario_modificacion=est2)
BloqueEditable.objects.create(nombre='Tecnología', contenido_html='<h2>Tecnología</h2><p>Noticias y novedades.</p>', estilos_css='h2{color:orange;}', usuario_creador=est3, usuario_modificacion=est3)
BloqueEditable.objects.create(nombre='Mujeres TIC', contenido_html='<h2>Mujeres en las TIC</h2><p>Promoviendo la inclusión.</p>', estilos_css='h2{color:pink;}', usuario_creador=est4, usuario_modificacion=est4)

print('Usuarios, grupos y publicaciones creados correctamente.')
