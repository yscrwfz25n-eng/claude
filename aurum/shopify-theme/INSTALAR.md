# Cómo instalar las secciones Aurum en Shopify

Funciona en cualquier tema moderno de Shopify ("Online Store 2.0"): Dawn, Sense, Refresh, Craft, Horizon y la mayoría de los temas pagos. Se hace una sola vez.

## 0. Antes de empezar: copia de seguridad
**Tienda online → Temas →** en tu tema, **⋯ → Duplicar.** Trabajá sobre la copia y publicala cuando esté lista.

## 1. Subir los archivos (en la copia del tema)
**⋯ → Editar código** y creá estos archivos, pegando el contenido de cada uno:

| Carpeta | Botón | Nombre del archivo |
|---|---|---|
| `assets` | Agregar un nuevo recurso → Crear un recurso en blanco | `aurum.css` |
| `assets` | Agregar un nuevo recurso → Crear un recurso en blanco | `aurum.js` |
| `snippets` | Agregar un nuevo fragmento | `aurum-motion` |
| `sections` | Agregar una nueva sección | `aurum-hero` |
| `sections` | Agregar una nueva sección | `aurum-split` |
| `sections` | Agregar una nueva sección | `aurum-packs` |
| `sections` | Agregar una nueva sección | `aurum-products` |
| `sections` | Agregar una nueva sección | `aurum-banner` |

Al crear una sección, Shopify trae un texto de ejemplo: **borralo entero** y pegá el nuestro.

## 2. Activar el movimiento y la estrella
Abrí `layout/theme.liquid`, buscá `</body>` (casi al final) y pegá **justo antes**:

```liquid
{% render 'aurum-motion' %}
```

Guardá.

## 3. Subir las imágenes
**Contenido → Archivos → Subir archivos**, con lo que está en la carpeta `imagenes-para-subir`:
- `lipoil-cut.png` y `resaltador-cut.png`: los productos que salen del marco (fondo transparente).
- `mano.jpg` y `cinta.jpg`: las fotos de la píldora, la lista y el banner.

## 4. Crear las colecciones
**Productos → Colecciones → Crear colección → Automatizada:**
- **Novedades:** la etiqueta del producto es igual a `nuevo`.
- **Kits:** el tipo de producto es igual a `Kits`.

Los productos y kits del archivo `Aurum_productos_shopify.csv` ya traen esas etiquetas y ese tipo.

## 5. Armar la página de inicio
**Personalizar → Página de inicio → Agregar sección.** Agregá las secciones en este orden y elegí, en cada una, su **lugar en la cápsula bordó**:

| Orden | Sección | Lugar en la cápsula | Qué cargar |
|---|---|---|---|
| 1 | Aurum · Hero | Inicio | Arriba: `lipoil-cut.png` · Píldora: `mano.jpg` · Abajo: vacío |
| 2 | Aurum · Lista + foto | Medio | Foto: `cinta.jpg` · Botón: "Ver promos" con link `#promos` |
| 3 | Aurum · Selector de promos | Medio | Producto: el resaltador · Frasco: `resaltador-cut.png`. Las 4 promos ya vienen cargadas. |
| 4 | Aurum · Productos | Medio | Colección: Novedades · Diseño: Carrusel · Título: "Nuevo en Aurum" |
| 5 | Aurum · Productos | Medio | Colección: Kits · Diseño: Grilla · Título: "Armá tu kit" · Ancla: `kits` |
| 6 | Aurum · Banner | Final | Foto: `mano.jpg` · Abajo: `resaltador-cut.png` |

Ocultá o borrá las secciones viejas del tema que ya no uses (el banner de imagen, la colección destacada, etc.).

## 6. Colores del resto de la tienda
Para que la página del producto, el carrito y el resto hagan juego: **Personalizar → Configuración del tema → Colores:**
- **Fondo:** `#10020A` · **Texto:** `#FCE4E3`
- **Botón:** `#F9D4D3` · **Texto del botón:** `#3B0408`
- **Fondo secundario (tarjetas):** `#3B0408`

## 7. Probar antes de publicar
En **Vista previa**, en la compu y en el celular, revisá:
- [ ] La estrella baja y gira al scrollear.
- [ ] El lip oil entra por arriba y el resaltador sale por abajo.
- [ ] En el selector de promos, cada botón cambia el precio, y "Comprar" suma la cantidad correcta al carrito con el descuento aplicado.
- [ ] El carrusel de novedades se desliza y "Sumar" agrega el producto.
- [ ] Nada se corta en el celular.

Si todo está bien: **Temas → tu copia → Publicar.**


## 7. Carrusel de videos (Aurum · Videos)
1. **Editar código → sections → Agregar una nueva sección** → nombre `aurum-videos` → borrá el ejemplo y pegá el contenido de `sections/aurum-videos.liquid`. Guardá.
2. **Contenido → Archivos → Subir archivos:** subí los videos verticales (están en `contenido_semana/5_Videos_editados/finales/`).
3. **Personalizar → Página de inicio → Agregar sección → Aurum · Videos.** Arrastrala justo debajo de **Aurum · Selector de promos**. Lugar en la cápsula: **Medio**.
4. En cada bloque **Video** elegí el video, una etiqueta corta y el producto que aparece debajo:

| Video | Etiqueta | Producto |
|---|---|---|
| `Rutina_glow.mp4` | Rutina glow | Iluminador Corporal Aurum |
| `AD_Cinta.mp4` | Antes y después | Iluminador Corporal Aurum |
| `AD_Kit_Fiesta_Glow.mp4` | Kit Fiesta Glow | Kit Fiesta Glow |
| `FEED_Ultra_Glitter.mp4` | Ultra Glitter | Ultra Glitter |
| `FEED_Labios.mp4` | Labios | Lip Oil |
| `FEED_Unboxing.mp4` | Unboxing | (vacío) |

Los videos arrancan solos sin sonido cuando aparecen en pantalla; con un toque se escuchan (y se silencian los demás).
