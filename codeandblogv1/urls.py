from django.urls import path, include
from .views import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/publicaciones/', views.publicaciones_admin, name='publicaciones_admin'),
    path('panel/publicaciones/crear/', views.crear_publicacion, name='crear_publicacion'),
    path('', views.home_blog, name='home_blog'),
    path('sobre-nosotras/', views.sobre_nosotras, name='sobre_nosotras'),
    path('categoria/<int:categoria_id>/', views.publicaciones_por_categoria, name='publicaciones_por_categoria'),
    path('panel/bloque/<str:nombre>/', views.editar_bloque, name='editar_bloque'),
    path('bloque/<str:nombre>/', views.vista_usuario, name='vista_usuario'),    path('panel/bloque/<str:nombre>/eliminar/', views.eliminar_bloque, name='eliminar_bloque'),
    path('comentario/like/<int:comentario_id>/', views.like_comentario, name='like_comentario'),
    path('comentario/editar/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('comentario/eliminar/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)