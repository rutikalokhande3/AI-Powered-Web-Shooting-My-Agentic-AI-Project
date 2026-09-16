import wave
import math
import random
import struct

SAMPLE_RATE = 44100
DURATION = 0.9

filename = "web_shoot.wav"

samples = []

for i in range(int(SAMPLE_RATE * DURATION)):

    t = i / SAMPLE_RATE

    # Cinematic whoosh
    freq = 900 - (700 * t)

    whoosh = math.sin(2 * math.pi * freq * t)

    # Sharp web snap
    snap = math.sin(2 * math.pi * 1800 * t)

    # Low cinematic impact
    impact = math.sin(2 * math.pi * 90 * t)

    # Envelopes
    whoosh_env = max(0, 1 - t / 0.75)
    snap_env = math.exp(-35 * t)
    impact_env = math.exp(-10 * max(0, t - 0.05))

    # Small noise for realistic texture
    noise = random.uniform(-1, 1) * 0.08

    value = (
        whoosh * whoosh_env * 0.45
        + snap * snap_env * 0.35
        + impact * impact_env * 0.25
        + noise * whoosh_env
    )

    # Prevent clipping
    value = max(-1, min(1, value))

    samples.append(
        struct.pack(
            "<h",
            int(value * 32767)
        )
    )


with wave.open(filename, "wb") as wav:

    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SAMPLE_RATE)

    wav.writeframes(b"".join(samples))


print("web_shoot.wav created successfully!")