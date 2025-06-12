from django.urls import path, include
from .views import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/publicaciones/', views.publicaciones_admin, name='publicaciones_admin'),
    path('', views.home_blog, name='home_blog'),
    #path('', include(router.urls)),
    #path('', views.editar_bloque, name='index'),
    path('panel/bloque/<str:nombre>/', views.editar_bloque, name='editar_bloque'),
    path('bloque/<str:nombre>/', views.vista_usuario, name='vista_usuario'),
    path('panel/bloque/<str:nombre>/eliminar/', views.eliminar_bloque, name='eliminar_bloque'),
    path('comentario/like/<int:comentario_id>/', views.like_comentario, name='like_comentario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)