# OPINÓLOGOS

> Todos opinan. Pocos convencen.

Juego de cartas de debate para adolescentes y adultos (14+), de 4 a 8 jugadores, para jugar en familia o con amigos.

**No gana quien tiene razón: gana quien hace cambiar de opinión a los demás.** Todos votan A FAVOR o EN CONTRA al mismo tiempo y debaten todos contra todos. El primero que logra que alguien cambie de opinión se lleva la carta del tema. Gana quien junta 5.

- 📖 [Reglamento completo](REGLAMENTO.md)
- 🖨️ [Cartas imprimibles (PDF)](opinologos-imprimible.pdf): 110 cartas en 26 hojas A4

## Para mandar a la imprenta

[`opinologos-muestra-imprenta.pdf`](opinologos-muestra-imprenta.pdf) tiene el juego completo en un solo archivo: 26 páginas de cartas (frente y dorso intercalados) y 4 páginas de reglamento. Se genera con:

```bash
python3 generar_pdf.py && python3 generar_reglamento.py
```

## Cómo imprimir en casa

1. Imprimí `opinologos-imprimible.pdf` en A4, **doble faz, girando por el borde largo** y al **100 %** (sin "ajustar a página").
2. Si tu impresora no imprime doble faz, imprimí las hojas impares (frentes) y las pares (dorsos) por separado, y pegalas espalda con espalda.
3. Cortá siguiendo las marcas de corte. Cada carta mide 63 × 88 mm, el tamaño estándar de las cartas de póker.
4. Lo ideal es papel de 200 a 300 g o cartulina. Otra opción: imprimir en papel común y meter cada carta en un folio de 63,5 × 88 junto con una carta vieja como respaldo.

## Diseño

Estilo C · Minimal: fondo blanco, un color por nivel (azul calentamiento, naranja picante, rojo profundo) y violeta para las cartas de Acción. Tipografía [Poppins](fuentes/OFL-Poppins.txt) (licencia OFL, libre para imprimir y vender). Las maquetas de los otros estilos están en `estilos/`.

## Editar el contenido

Todos los textos de las cartas están en [`contenido.py`](contenido.py). Después de cambiarlos, regenerá el PDF:

```bash
pip install reportlab
python3 generar_pdf.py
```

**Regla de oro para escribir temas:** en una mesa típica, el voto inicial debería quedar cerca de 50/50. Si un tema arranca 6 a 0, no genera debate y conviene reemplazarlo.
