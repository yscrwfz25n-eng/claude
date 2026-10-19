"""Interior completo del ÁLBUM DE VINOS (104 páginas A5 + 3 mm de sangrado).

Uso:  python3 vinos/generar_libro.py
  -> vinos/interior.html                  (generado)
  -> vinos/album-de-vinos-interior.pdf    para imprenta, con TrimBox/BleedBox en cada página
  -> vinos/interior-muestra.png           vista previa de algunas páginas

Orden: 1 «Este álbum es de» · 2-101 vinos N.º 01 a 100 · 102 «Los inolvidables» (top 5)
· 103 «Este álbum lo completó» (foto + fecha) · 104 colofón. 104 es múltiplo de 4 (pliegos).
La página de cada vino sale de pagina.html. En las páginas impares el lomo queda a la
izquierda; en las pares, a la derecha: el margen ancho siempre va del lado del lomo.
"""
import os
import random
import re
import subprocess
import tempfile

from PIL import Image

from generar_tapa import AQUI, pdf_de_imprenta

SALIDA = os.path.join(AQUI, "album-de-vinos-interior.pdf")
BOTELLAS = 100

base = open(os.path.join(AQUI, "pagina.html"), encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", base, re.S).group(1)
CSS = CSS.replace("html,body{margin:0;width:154mm;height:216mm;overflow:hidden;}", "html,body{margin:0;}")
CSS = CSS.replace("body{position:relative;background:#FBF8F3;", "body{")
CSS += """
  .pagina{position:relative;width:154mm;height:216mm;overflow:hidden;background:#FBF8F3;break-after:page;}
  .par .hoja{left:15mm;}
  .centro{position:absolute;left:19mm;width:120mm;text-align:center;}
  .par .centro{left:15mm;}
  .o.acento{position:relative;}
  .o.acento::after{content:"";position:absolute;background:currentColor;transform:skewX(-28deg);}
"""
cuerpo = base[base.index("<body>") + 6:base.index("</body>")]
# las definiciones de filtros van una sola vez al principio del documento
DEFS = re.search(r"<defs>(.*?)</defs>", cuerpo, re.S).group(1)
DEFS += """
    <filter id="prensa" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.45" numOctaves="3" seed="11" result="ruido"/>
      <feColorMatrix in="ruido" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -8 6.1" result="huecos"/>
      <feComposite in="SourceGraphic" in2="huecos" operator="in"/>
    </filter>"""
cuerpo = re.sub(r"<defs>.*?</defs>", "", cuerpo, flags=re.S)
_i = cuerpo.index('<g filter="url(#mano)"')
DIBUJOS = cuerpo[_i:cuerpo.index("</svg>", _i)]
HOJA = cuerpo[cuerpo.index('<div class="hoja">'):]

# esquinas posibles para el aro de copa: varía de página en página (a veces no hay)
AROS = [(-4, 222), (158, 222), (158, -6), (-4, -6), None, None]
CAPA = '<svg class="capa" viewBox="0 0 154 216" style="mix-blend-mode:multiply">{}</svg>'


def aro(rnd):
    pos = rnd.choice(AROS)
    if pos is None:
        return ""
    r = rnd.uniform(14, 18)
    return (f'<g filter="url(#acuarela)"><circle cx="{pos[0]}" cy="{pos[1]}" r="{r:.1f}" fill="none" '
            f'stroke="#7A1436" stroke-width="1.8" opacity=".16"/></g>')


def pagina(n_hoja, contenido, fondo=""):
    clase = "pagina par" if n_hoja % 2 == 0 else "pagina"
    return f'<div class="{clase}">{CAPA.format(fondo)}{contenido}</div>\n'


def titulo(texto, size, color="var(--tinta)"):
    """Bebas con las O como círculos (y la Ó con su tilde)."""
    o = size * 0.69
    borde = size * 0.11
    html = ""
    for ch in texto:
        if ch in "OÓ":
            extra = "acento" if ch == "Ó" else ""
            tilde = (f'<style>.t{int(size * 10)}::after{{left:{o * .38:.2f}mm;top:{-o * .32:.2f}mm;'
                     f'width:{o * .14:.2f}mm;height:{o * .24:.2f}mm;}}</style>') if extra else ""
            html += (f'{tilde}<span class="o {extra} t{int(size * 10)}" style="width:{o:.2f}mm;height:{o:.2f}mm;'
                     f'border-width:{borde:.2f}mm;margin:0 {size * .02:.2f}mm;"></span>')
        else:
            html += "&nbsp;" if ch == " " else ch
    return (f'<div class="bebas" style="font-size:{size}mm;color:{color};justify-content:center;'
            f'filter:url(#prensa);">{html}</div>')


GARABATO_COPA = ('<g transform="translate({x} {y}) rotate({r}) scale({s})"><path d="M0 0C0 13 4 19 9 19C14 19 18 13 18 0Z"/>'
                 '<path d="M9 19V31"/><path d="M3 32Q9 29.5 15 32"/><path d="M1 7Q9 9.5 17 7"/></g>')
GARABATO_SACACORCHOS = ('<g transform="translate({x} {y}) rotate({r}) scale({s})"><path d="M0 4Q12 -2 24 4"/><path d="M12 1.5V10"/>'
                        '<path d="M12 10q-3.5 1.6 0 3.2q3.5 1.6 0 3.2q-3.5 1.6 0 3.2q3.5 1.6 0 3.2"/></g>')


def mano(*partes):
    return ('<g filter="url(#mano)" fill="none" stroke="#7A1832" stroke-width=".7" stroke-linecap="round" '
            'stroke-linejoin="round">' + "".join(partes) + "</g>")


def linea_campo(etiqueta, ancho="80mm"):
    return (f'<div class="campo" style="width:{ancho};margin:0 auto;"><span class="et">{etiqueta}</span></div>')


def portadilla():
    contenido = f'''<div class="centro" style="top:58mm;">
      {titulo("ESTE ÁLBUM", 20)}{titulo("ES DE", 20)}
      <div style="height:16mm"></div>{linea_campo("nombre", "92mm")}
      <div style="height:9mm"></div>
      <div class="et">empezado el</div>
      <div style="font-size:5mm;letter-spacing:1.2mm;color:var(--linea);margin-top:1.5mm;">__ / __ / ____</div>
      <div class="manuscrita" style="font-size:9mm;margin-top:16mm;">cien botellas por delante</div>
    </div>'''
    fondo = aro(random.Random(1)) + mano(GARABATO_COPA.format(x=64, y=30, r=-10, s=.7),
                                         GARABATO_SACACORCHOS.format(x=80, y=32, r=24, s=.6))
    return contenido, fondo


def inolvidables():
    filas = ""
    for i in range(1, 6):
        filas += f'''<div style="display:grid;grid-template-columns:12mm 1fr 18mm;column-gap:3mm;align-items:end;height:19mm;">
          <div class="bebas" style="font-size:15mm;color:var(--vino);filter:url(#prensa);">{i}</div>
          <div class="campo"><span class="et">vino</span></div>
          <div class="campo"><span class="et">n.º</span></div>
        </div>'''
    contenido = f'''<div class="hoja" style="top:20mm;">{titulo("LOS INOLVIDABLES", 15, "var(--vino)")}
      <div class="manuscrita" style="font-size:7mm;text-align:center;margin-top:1mm;">los cinco que volverías a abrir</div>
      <div style="height:10mm"></div>{filas}
      <div class="seccion" style="margin-top:12mm;"><span class="et">el peor de todos (con cariño)</span>
      <div class="campo"></div></div></div>'''
    return contenido, aro(random.Random(2))


def completado():
    contenido = f'''<div class="centro" style="top:16mm;">
      {titulo("ESTE ÁLBUM", 15)}{titulo("LO COMPLETÓ", 15, "var(--vino)")}
      <div style="height:8mm"></div>{linea_campo("nombres", "100mm")}
      <div style="width:96mm;height:96mm;margin:9mm auto 0;border:.35mm dashed var(--linea);border-radius:2.5mm;
                  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1mm;">
        <span class="manuscrita" style="font-size:8mm;">pegá una foto acá</span>
        <span class="et">la de la última botella</span>
      </div>
      <div style="height:8mm"></div>
      <div class="et">terminado el</div>
      <div style="font-size:5mm;letter-spacing:1.2mm;color:var(--linea);margin-top:1.5mm;">__ / __ / ____</div>
      <div class="manuscrita" style="font-size:8.5mm;margin-top:6mm;">cien vinos después. ¡Salud!</div>
    </div>'''
    return contenido, aro(random.Random(3))


def colofon():
    contenido = '''<div class="centro" style="top:178mm;color:var(--tinta);">
      <svg viewBox="0 0 100 100" style="width:9mm;height:9mm;">
        <circle cx="50" cy="50" r="34" fill="none" stroke="#142A40" stroke-width="8"/>
        <line x1="50" y1="2" x2="50" y2="98" stroke="#142A40" stroke-width="8"/>
        <line x1="2" y1="50" x2="98" y2="50" stroke="#142A40" stroke-width="8"/>
        <circle cx="50" cy="50" r="11" fill="#1C82D9"/></svg>
      <div style="font-family:Marker;font-size:5.2mm;color:#142A40;margin-top:1mm;">Oficina Gráfica</div>
      <div class="et" style="margin-top:2mm;">diseñado e impreso por nosotros · @oficina.grafica_</div>
    </div>'''
    return contenido, ""


def vino(n, rnd):
    hoja = HOJA.replace("&nbsp;N.º 01", f"&nbsp;N.º {n:02d}" if n < 100 else "&nbsp;N.º 100")
    return hoja, aro(rnd) + DIBUJOS


def main():
    rnd = random.Random(42)
    paginas = [portadilla()] + [vino(n, rnd) for n in range(1, BOTELLAS + 1)] + [inolvidables(), completado(),
                                                                                  colofon()]
    html = ['<!doctype html><html lang="es"><head><meta charset="utf-8"><style>',
            "@font-face{font-family:Marker;src:url('../fuentes/PermanentMarker-Regular.ttf');}", CSS, "</style></head><body>",
            f'<svg width="0" height="0" style="position:absolute"><defs>{DEFS}</defs></svg>']
    html += [pagina(i + 1, c, f) for i, (c, f) in enumerate(paginas)]
    html.append("</body></html>")
    with open(os.path.join(AQUI, "interior.html"), "w", encoding="utf-8") as f:
        f.write("".join(html))
    pdf_de_imprenta("interior.html", SALIDA, "Álbum de vinos – interior")
    # vista previa: portadilla, dos vinos enfrentados y las páginas finales
    tmp = tempfile.mkdtemp()
    vistas = []
    for n in (1, 2, 3, 102, 103, 104):
        b = os.path.join(tmp, f"p{n}")
        subprocess.run(["pdftoppm", "-r", "60", "-png", "-singlefile", "-f", str(n), "-l", str(n), SALIDA, b], check=True)
        im = Image.open(b + ".png")
        s = round(3 / 25.4 * 60)
        vistas.append(im.crop((s, s, im.width - s, im.height - s)))
    w, h = vistas[0].size
    hoja = Image.new("RGB", (w * 3 + 40, h * 2 + 30), "#D9D0C2")
    for i, im in enumerate(vistas):
        hoja.paste(im, (10 + (i % 3) * (w + 10), 10 + (i // 3) * (h + 10)))
    hoja.save(os.path.join(AQUI, "interior-muestra.png"))
    print("ok interior-muestra.png")


if __name__ == "__main__":
    main()
