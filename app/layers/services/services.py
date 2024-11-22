# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from ..transport import transport
from django.contrib.auth import get_user
from django.contrib.auth.models import User

def getAllImages(input=None):
    json_collection = transport.getAllImages(input)
    images = []
    
    for img in json_collection: # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
        card = translator.fromRequestIntoCard(img)
        #if card not in images:
        images.append(card)

    return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request) # transformamos un request del template en una Card.
    fav.user = request.POST.get("user") # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.getAllFavourites(user) # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.fromRepositoryIntoCard(request) # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.
