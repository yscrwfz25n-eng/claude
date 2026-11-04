"""Voz en off, música de fondo y efectos para el video de Match.

La voz es voz-elevenlabs.mp3 (ElevenLabs, voz «Cande»), con el guion de GUION.md. La música y los
efectos se sintetizan acá (sin samples de terceros).
Mientras habla la voz, la música baja sola.

Uso:  python3 redes/video-match/audio.py  ->  match-preventa-con-audio.mp4 (video + audio)

Música: piano eléctrico suave sobre Dm9 – B♭maj7 – Fmaj7 – C, a 84 bpm, con bombo y hi-hat bajitos.
Efectos: «whoosh» cuando entra cada carta, un clic al dar vuelta la carta, crepitar de fuego en el
reto y un golpe al aparecer «PREVENTA». Los tiempos coinciden con generar.py.
"""
import os
import subprocess

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SR, DUR = 44100, 19.3
N = int(SR * DUR)
rng = np.random.default_rng(7)


def nota(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def epiano(f, dur, vel=0.25):
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * 2.2) * (1 - np.exp(-t * 300))
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 4) + 0.12 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 7)
    return vel * env * s


def pasabajos(x, corte):
    b, a = butter(2, corte / (SR / 2), "low")
    return lfilter(b, a, x)


def pasaaltos(x, corte):
    b, a = butter(2, corte / (SR / 2), "high")
    return lfilter(b, a, x)


def poner(pista, x, t0, gan=1.0):
    i = int(t0 * SR)
    j = min(N, i + len(x))
    if i < N:
        pista[i:j] += gan * x[: j - i]


def musica():
    pista = np.zeros(N)
    beat = 60 / 84
    compas = 4 * beat
    acordes = [[50, 53, 57, 60, 64], [46, 50, 53, 57, 62], [41, 48, 52, 57, 60], [48, 52, 55, 59, 62]]  # Dm9 Bbmaj7 Fmaj7 Cmaj7
    t0, k = 0.0, 0
    while t0 < DUR:
        ac = acordes[k % 4]
        for b in range(4):  # acorde arpegiado suave en cada tiempo
            tt = t0 + b * beat
            notas = ac if b == 0 else ac[1:]
            for i, m in enumerate(notas):
                poner(pista, epiano(nota(m + 12 if b % 2 and i > 2 else m), 1.6, 0.10 if b else 0.14), tt + i * 0.012)
            poner(pista, epiano(nota(ac[0] - 12), 2.0, 0.22), t0) if b == 0 else None  # bajo
            # bombo en 1 y 3, hi-hat en corcheas
            if b in (0, 2):
                tk = np.arange(int(SR * 0.25)) / SR
                poner(pista, 0.5 * np.sin(2 * np.pi * (55 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 14), tt)
            for h in (0, beat / 2):
                ruido = pasaaltos(rng.standard_normal(int(SR * 0.05)), 7000) * np.exp(-np.arange(int(SR * 0.05)) / SR * 90)
                poner(pista, 0.05 * ruido, tt + h)
        t0 += compas
        k += 1
    return pasabajos(pista, 9000)


def whoosh(dur=0.5):
    n = int(SR * dur)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    trozos = 20
    for i in range(trozos):  # barrido de filtro de grave a agudo
        a, b = i * n // trozos, (i + 1) * n // trozos
        out[a:b] = pasabajos(x, 400 + 5000 * (i / trozos) ** 2)[a:b]
    env = np.sin(np.pi * np.arange(n) / n) ** 2
    return 0.45 * out * env


def clic():
    n = int(SR * 0.04)
    return 0.4 * pasaaltos(rng.standard_normal(n), 2500) * np.exp(-np.arange(n) / SR * 120)


def fuego(dur):
    n = int(SR * dur)
    base = pasabajos(rng.standard_normal(n), 900) * 0.25  # rumor grave
    crep = np.zeros(n)
    for _ in range(int(dur * 45)):  # chasquidos al azar
        i = rng.integers(0, n - 600)
        largo = rng.integers(80, 500)
        crep[i:i + largo] += rng.uniform(.2, .7) * pasaaltos(rng.standard_normal(largo), 3000) * np.exp(-np.arange(largo) / largo * 6)
    env = np.minimum(1, np.arange(n) / (SR * 0.6)) * np.minimum(1, (n - np.arange(n)) / (SR * 0.3))
    return (base + crep) * env * 0.6


def golpe():
    t = np.arange(int(SR * 0.6)) / SR
    return 0.7 * np.sin(2 * np.pi * (45 + 120 * np.exp(-t * 25)) * t) * np.exp(-t * 6) + 0.15 * pasabajos(rng.standard_normal(len(t)), 3000) * np.exp(-t * 18)


VOZ_ELEVENLABS = os.path.join(AQUI, "voz-elevenlabs.mp3")  # voz «Cande», de ElevenLabs


def voz():
    """La voz completa de ElevenLabs desde el segundo 0 y una envolvente de «está hablando»."""
    wav = os.path.join(AQUI, "_voz.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VOZ_ELEVENLABS, "-ac", "1", "-ar", str(SR), wav], check=True)
    _, x = wavfile.read(wav)
    os.remove(wav)
    x = x.astype(float) / 32768
    pista = np.zeros(N)
    poner(pista, x, 0.0)
    k = int(SR * 0.25)
    nivel = np.convolve(np.abs(pista), np.ones(k) / k, mode="same")
    habla = np.clip(nivel / (0.3 * nivel.max()), 0, 1)
    return pista, habla


def main():
    v, habla = voz()
    m = musica() * 0.55 * (1 - 0.6 * habla)
    fx = np.zeros(N)
    for t0 in (0.8, 5.7, 8.7, 10.8, 14.7):  # tiempos del video ya estirado a la voz
        poner(fx, whoosh(), t0 - 0.1)
    poner(fx, clic(), 3.3)
    poner(fx, fuego(3.0), 8.95)
    poner(fx, golpe(), 14.85)
    v = v / np.max(np.abs(v))
    mezcla = 0.55 * (m + fx * (1 - 0.4 * habla)) / max(1e-9, np.max(np.abs(m + fx))) + 0.95 * v
    # fundido de entrada y de salida
    env = np.minimum(1, np.arange(N) / (SR * 0.5)) * np.minimum(1, (N - np.arange(N)) / (SR * 1.2))
    mezcla *= env
    mezcla = 0.89 * mezcla / np.max(np.abs(mezcla))
    estereo = np.stack([mezcla, mezcla], axis=1)
    wav = os.path.join(AQUI, "_audio.wav")
    wavfile.write(wav, SR, (estereo * 32767).astype(np.int16))
    video = os.path.join(AQUI, "match-preventa.mp4")
    salida = os.path.join(AQUI, "match-preventa-con-audio.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", salida], check=True)
    os.remove(wav)
    print("ok", os.path.basename(salida))


if __name__ == "__main__":
    main()
