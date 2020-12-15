import folium


from pokemon_entities.models import PokemonEntity
from pokemon_entities.models import Pokemon
from django.http import HttpResponseNotFound
from django.shortcuts import render


from django.core.exceptions import MultipleObjectsReturned

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL= "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    http_path = request.build_absolute_uri()[:-1]

    pokemonentitys = PokemonEntity.objects.all()
    for pokemon_entity in pokemonentitys:
        full_url_image = '{0}{1}'.format(http_path, pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon, full_url_image)

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for current_pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': current_pokemon.id,
            'img_url': current_pokemon.image.url,
            'title_ru': current_pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
        })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.filter(id=pokemon_id).get()
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    except  MultipleObjectsReturned:
        return HttpResponseNotFound('<h1>много  покемонов с одним id Так никак не может быть</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    http_path = request.build_absolute_uri('/pokemon/')[:-9]

    pokemon_entitys = requested_pokemon.vid_pokemon.all()
    for pokemon_entity in pokemon_entitys:
        full_url_image = '{0}{1}'.format(http_path, pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon, full_url_image)
    else:
        full_url_image = '{0}{1}'.format(http_path, requested_pokemon.image.url)


    current_pokemon = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': full_url_image,
    }
    parent_pokemon = requested_pokemon.previous_evolution
    if parent_pokemon:
        full_url_parent_image = '{0}{1}'.format(http_path, parent_pokemon.image.url)
        parent_pokemon_properties = {
            'pokemon_id': parent_pokemon.id,
            'title_ru': parent_pokemon.title,
            'img_url': full_url_parent_image,
        }
        current_pokemon['previous_evolution'] = parent_pokemon_properties

    if requested_pokemon.next_evolution.count():
        next_evolution_pokemon = requested_pokemon.next_evolution.all()[0]
        full_url_next_evolution_image = '{0}{1}'.format(http_path, next_evolution_pokemon.image.url)
        next_evolution_pokemon_properties = {
            'pokemon_id': next_evolution_pokemon.id,
            'title_ru': next_evolution_pokemon.title,
            'img_url': full_url_next_evolution_image,
        }
        current_pokemon['next_evolution'] = next_evolution_pokemon_properties

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                'pokemon': current_pokemon})
