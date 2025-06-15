from django.contrib import admin
from .models import BloqueEditable, Categoria_comentario, Comentario

# Register your models here.
admin.site.register(BloqueEditable)
admin.site.register(Categoria_comentario)
admin.site.register(Comentario)