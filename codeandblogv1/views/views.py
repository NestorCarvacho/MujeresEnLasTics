# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..models import BloqueEditable, Comentario, Categoria_comentario
from ..forms import BloqueEditableForm
from django.http import JsonResponse

def is_admin(user):
    return user.groups.filter(name='admin').exists() or user.is_superuser

def is_estudiante(user):
    return user.groups.filter(name='estudiante').exists()

@login_required
def editar_bloque(request, nombre):
    bloque = get_object_or_404(BloqueEditable, nombre=nombre)

    if request.method == 'POST':
        form = BloqueEditableForm(request.POST, request.FILES, instance=bloque)
        if form.is_valid():
            bloque = form.save(commit=False)
            bloque.save(user=request.user)
            return redirect('publicaciones_admin')
    else:
        form = BloqueEditableForm(instance=bloque)

    return render(request, 'admin/editar_bloque.html', {'form': form, 'bloque': bloque})

def vista_usuario(request, nombre):
    bloque = get_object_or_404(BloqueEditable, nombre=nombre)
    comentarios = bloque.comentarios.select_related('usuario').all().order_by('-fecha')
    categorias = Categoria_comentario.objects.all()
    if request.method == 'POST' and request.user.is_authenticated:
        texto = request.POST.get('comentario')
        if texto:
            Comentario.objects.create(bloque=bloque, usuario=request.user, texto=texto)
            return redirect('vista_usuario', nombre=nombre)
    return render(request, 'usuario/ver_bloque.html', {'bloque': bloque, 'comentarios': comentarios, 'categorias': categorias})

@login_required
def like_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user in comentario.likes.all():
        comentario.likes.remove(request.user)
        liked = False
    else:
        comentario.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': comentario.total_likes()})

def home_blog(request):
    publicaciones = BloqueEditable.objects.filter(aparece_en_inicio=True).order_by('-fecha_registro')
    categorias = Categoria_comentario.objects.all()
    return render(request, 'usuario/publicaciones_recientes.html', {
        'publicaciones': publicaciones,
        'categorias': categorias
    })

@login_required
def publicaciones_admin(request):
    if not is_admin(request.user):
        return redirect('home_blog')
    publicaciones = BloqueEditable.objects.all()
    return render(request, 'admin/publicaciones_admin.html', {'publicaciones': publicaciones})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='admin').exists() or user.is_superuser:
                return redirect('publicaciones_admin')
            else:
                return redirect('home_blog')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'usuario/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def eliminar_bloque(request, nombre):
    bloque = get_object_or_404(BloqueEditable, nombre=nombre)
    if request.method == 'POST':
        bloque.delete()
        messages.success(request, 'Publicación eliminada correctamente.')
        return redirect('publicaciones_admin')
    return render(request, 'admin/confirmar_eliminar.html', {'bloque': bloque})

@login_required
def crear_publicacion(request):
    if not is_admin(request.user):
        return redirect('home_blog')
    if request.method == 'POST':
        form = BloqueEditableForm(request.POST, request.FILES)
        if form.is_valid():
            bloque = form.save(commit=False)
            bloque.save(user=request.user)
            return redirect('publicaciones_admin')
    else:
        form = BloqueEditableForm()
    return render(request, 'admin/crear_bloque.html', {'form': form})

def publicaciones_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria_comentario, Id_categoria=categoria_id)
    publicaciones = BloqueEditable.objects.filter(categoria=categoria).order_by('-fecha_registro')
    categorias = Categoria_comentario.objects.all()
    return render(request, 'usuario/publicaciones_recientes.html', {
        'publicaciones': publicaciones,
        'categorias': categorias,
        'categoria_actual': categoria
    })

@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verificar permisos
    if not request.user.is_superuser and request.user != comentario.usuario:
        return JsonResponse({'success': False, 'error': 'No tienes permiso para editar este comentario'})
    
    if request.method == 'POST':
        nuevo_texto = request.POST.get('texto')
        if nuevo_texto:
            comentario.texto = nuevo_texto
            comentario.save()
            return JsonResponse({
                'success': True,
                'texto': nuevo_texto
            })
    return JsonResponse({'success': False})

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verificar permisos
    if not request.user.is_superuser and request.user != comentario.usuario:
        return JsonResponse({'success': False, 'error': 'No tienes permiso para eliminar este comentario'})
    
    if request.method == 'POST':
        comentario.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def sobre_nosotras(request):
    categorias = Categoria_comentario.objects.all()
    return render(request, 'usuario/sobre_nosotras.html', {
        'categorias': categorias
    })