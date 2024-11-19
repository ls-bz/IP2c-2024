# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator


def index_page(request):
    return render(request, 'index.html')

def home(request, page=2):
    images = services.getAllImages(input=None) # Esta función obtiene todas las imágenes de la API
    favourite_list = []
    if request.user.is_authenticated: # Verificamos si el usuario se encuentra autenticado, de lo contrario devuelve un listado vacío.
         favourite_list = services.getAllFavourites(request) # Obtiene los favoritos del usuario

    # Configura el paginador para mostrar 20 resultados
    paginator = Paginator(images, per_page=20) # Show 20 per page.

    #page_object = paginator.get_page(page)


    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    # Guardamos images y favourites en un limite de 20 elementos
    context = {'page_object': page_object}

    return render(request, 'home.html', context)

def search(request):
    search_msg = request.POST.get('query', '')
    print(search_msg)
    # y luego renderiza el template (similar a home).
    if (search_msg != ''): # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
        images = services.getAllImages(input=search_msg)
        favourite_list = []
        if request.user.is_authenticated: 
            favourite_list = services.getAllFavourites(request)

        paginator = Paginator(images, per_page=20)
 
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        
        context = {'page_object': page_object, 'favourite_list': favourite_list}

        return render(request, 'home.html', context)

    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    getAllFavouritesByUser(request)
    return saveFavourite(request)

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')