from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# Create your models here.
class BloqueEditable(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # ej: "bloque_inicio"
    contenido_html = models.TextField()
    estilos_css = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    usuario_creador = models.ForeignKey(User, related_name='publicaciones_creadas', on_delete=models.SET_NULL, null=True, blank=True)
    usuario_modificacion = models.ForeignKey(User, related_name='publicaciones_modificadas', on_delete=models.SET_NULL, null=True, blank=True)
    aparece_en_inicio = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='publicaciones/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'svg'])])

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not self.pk and user:
            self.usuario_creador = user
        if user:
            self.usuario_modificacion = user
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.imagen and self.imagen.size > 3*1024*1024:
            raise ValidationError('La imagen no puede superar los 3MB.')

class Comentario(models.Model):
    bloque = models.ForeignKey(BloqueEditable, related_name='comentarios', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comentarios_likeados', blank=True)

    def total_likes(self):
        return self.likes.count()