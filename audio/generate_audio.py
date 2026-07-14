# -*- coding: utf-8 -*-
"""
Regenerates the narration clips in this folder using the Kokoro TTS model
(https://huggingface.co/hexgrad/Kokoro-82M), voice "af_heart" -- the same
voice used in Dragon's Pearl Chase, so narration sounds consistent across
both games.

Setup (one-time):
    pip install kokoro-onnx soundfile
    # download kokoro-v1.0.onnx and voices-v1.0.bin from the Kokoro-82M
    # HuggingFace repo into this folder (or point the paths below at them)
    brew install espeak-ng  # provides phonemization; see note below

Note on espeak-ng: the prebuilt espeakng-loader wheel ships a espeak-ng
build with a hardcoded (CI-runner) data path that doesn't exist on a normal
machine, causing phonemization to fail. This script points Kokoro at the
Homebrew-installed espeak-ng instead, which works correctly.

Run:
    python3 generate_audio.py
"""
import subprocess
from kokoro_onnx import Kokoro
from kokoro_onnx.config import EspeakConfig
import soundfile as sf

VOICE = "af_heart"
SPEED = 0.95

ESPEAK_CONFIG = EspeakConfig(
    lib_path="/opt/homebrew/opt/espeak-ng/lib/libespeak-ng.dylib",
    data_path="/opt/homebrew/opt/espeak-ng/share/espeak-ng-data",
)

STORIES = [
    ("meadow",
     "Once upon a time, in a meadow just past the garden gate, Princess Rosie met a unicorn named Buttercup. But something was wrong. All the colors in the meadow had disappeared! “Will you help me bring the colors back?” asked Buttercup. Rosie smiled and picked up her paintbrush."),
    ("mane",
     "Buttercup's mane and tail used to sparkle with every color of the rainbow. “Paint me bright and beautiful again!” said Buttercup, swishing her tail. Rosie chose her favorite colors and got to work."),
    ("bridge",
     "As soon as Buttercup's mane sparkled again, a magical bridge began to glow in the sky. “That's the Rainbow Bridge!” said Buttercup. “It only appears when there's enough color in the world. Let's paint it and cross together!”"),
    ("sky",
     "On the other side of the bridge, Rosie and Buttercup found a garden floating high on fluffy clouds. The sun smiled down, waiting for its warm colors. “This is where all the stars come out to play,” whispered Buttercup."),
    ("garden",
     "Next, they landed in a garden bursting with flowers and butterflies, all waiting for their colors too. Rosie painted every petal she could find, and the butterflies danced with joy."),
    ("castle",
     "At last, they reached the Crystal Castle at the top of the kingdom. When Rosie painted the very last color, the whole kingdom sparkled brighter than ever before! Buttercup bowed her head, and Rosie became the kingdom's very first Rainbow Princess. The End!"),
]

COLORS = [
    "Red", "Orange", "Yellow", "Green", "Teal", "Blue",
    "Purple", "Pink", "Brown", "Black", "White", "Gold",
]

k = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin", espeak_config=ESPEAK_CONFIG)


def render(slug, text):
    samples, sr = k.create(text, voice=VOICE, speed=SPEED, lang="en-us")
    wav_path = f"{slug}.wav"
    mp3_path = f"{slug}.mp3"
    sf.write(wav_path, samples, sr)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
         "-codec:a", "libmp3lame", "-b:a", "48k", "-ac", "1", mp3_path],
        check=True,
    )
    subprocess.run(["rm", wav_path], check=True)
    print(f"{slug}: {len(samples)/sr:.2f}s")


for slug, text in STORIES:
    render(slug, text)
for name in COLORS:
    render("color-" + name.lower(), name)
