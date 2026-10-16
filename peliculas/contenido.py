"""Contenido de THE WATCH LIST: checklist de 100 películas y series populares en Argentina.

Títulos como se conocen en Argentina. Cada ítem se tilda al verlo y se completa con datos.
"""

CATEGORIAS = [
    ("Clásicos", [
        "El padrino", "Casablanca", "Lo que el viento se llevó", "El mago de Oz",
        "Tiempos modernos", "Psicosis", "Tiburón", "E.T., el extraterrestre", "Rocky",
        "El resplandor", "Taxi Driver", "Alien, el octavo pasajero", "La lista de Schindler",
        "Tiempos violentos", "Sueños de fuga", "Forrest Gump", "Titanic", "La vida es bella",
        "Cinema Paradiso", "Atrapado sin salida",
    ]),
    ("Las que todos vimos", [
        "Mi pobre angelito", "Jumanji", "Los Goonies", "Matrix", "Gladiador", "El sexto sentido",
        "Corazón valiente", "El club de la pelea", "Mujer bonita", "Ghost, la sombra del amor",
        "Diario de una pasión", "El diablo viste a la moda", "Chicas pesadas", "¿Qué pasó ayer?",
        "Son como niños", "Como si fuera la primera vez", "El origen", "Interestelar",
        "Batman: el caballero de la noche", "Mamma mia!",
    ]),
    ("Cine argentino", [
        "La historia oficial", "El secreto de sus ojos", "Nueve reinas", "Relatos salvajes",
        "Argentina, 1985", "El hijo de la novia", "Esperando la carroza", "Camila",
        "La noche de los lápices", "Un cuento chino", "Elsa y Fred", "El ciudadano ilustre",
        "Kamchatka", "Tango feroz", "Plata dulce", "Tiempo de revancha", "El clan",
        "Mi obra maestra", "Comodines", "Pizza, birra, faso",
    ]),
    ("Sagas", [
        "Harry Potter", "El señor de los anillos", "Star Wars", "Volver al futuro", "Toy Story",
        "Rápido y furioso", "Piratas del Caribe", "Los juegos del hambre", "Shrek", "Indiana Jones",
    ]),
    ("Animadas", [
        "El rey león", "Buscando a Nemo", "Coco", "Intensa-Mente", "Up: una aventura de altura",
        "Mi villano favorito", "La era del hielo", "Los increíbles", "Frozen", "Ratatouille",
    ]),
    ("Series", [
        "Friends", "Breaking Bad", "Los Simpson", "La casa de papel", "Stranger Things",
        "Game of Thrones", "The Office", "Grey's Anatomy", "Dr. House", "Lost", "Peaky Blinders",
        "Los Soprano", "Gilmore Girls", "Dark", "How I Met Your Mother", "Los simuladores",
        "Casados con hijos", "Okupas", "El marginal", "Graduados",
    ]),
]

# Datos para completar en cada ítem
CAMPOS = ["Fecha", "Con quién la vi", "Puntaje", "Frase o escena favorita"]
