from PIL import Image, ImageDraw, ImageFilter
import math
import random
import os

# =========================
# SETTINGS
# =========================

WIDTH = 900
HEIGHT = 450
FRAMES = 30

OUTPUT_DIR = "vfx"

os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)


# =========================
# CREATE WEB FRAME
# =========================

def create_frame(frame_number):

    img = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    # Separate glow layer
    glow = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow)

    # Main layer
    draw = ImageDraw.Draw(img)

    # Web starts near left side
    start_x = 45
    start_y = HEIGHT // 2

    # Web grows forward
    progress = frame_number / (FRAMES - 1)

    max_length = 760
    length = max_length * progress

    # Shooting direction
    end_x = start_x + length
    end_y = start_y

    # =========================
    # SHOOTING CORE
    # =========================

    if progress > 0:

        # Soft energy glow
        glow_radius = int(12 + 10 * progress)

        glow_draw.ellipse(
            (
                start_x - glow_radius,
                start_y - glow_radius,
                start_x + glow_radius,
                start_y + glow_radius
            ),
            fill=(210, 235, 255, 130)
        )

        # Bright center
        draw.ellipse(
            (
                start_x - 4,
                start_y - 4,
                start_x + 4,
                start_y + 4
            ),
            fill=(235, 245, 255, 240)
        )

    # =========================
    # WEB STRANDS
    # =========================

    if length > 5:

        strand_count = 7

        for strand in range(strand_count):

            points = []

            # Different vertical offsets
            offset = (
                (strand - (strand_count - 1) / 2)
                * 10
            )

            for i in range(31):

                t = i / 30

                x = start_x + length * t

                # Taper towards the end
                wave_strength = (
                    4
                    * math.sin(t * 15 + strand)
                    * (1 - t)
                )

                y = (
                    start_y
                    + offset * t
                    + wave_strength
                )

                points.append((x, y))

            # Glow strand
            glow_draw.line(
                points,
                fill=(170, 220, 255, 100),
                width=7
            )

            # Main thin strand
            draw.line(
                points,
                fill=(225, 240, 255, 215),
                width=2
            )

    # =========================
    # WEB CROSS CONNECTIONS
    # =========================

    if length > 80:

        for ring in range(4):

            x = start_x + length * (
                0.25 + ring * 0.18
            )

            if x < end_x:

                radius = 10 + ring * 4

                # Curved-ish horizontal web connector
                top = start_y - radius
                bottom = start_y + radius

                draw.arc(
                    (
                        x - radius,
                        top,
                        x + radius,
                        bottom
                    ),
                    200,
                    340,
                    fill=(220, 238, 255, 170),
                    width=1
                )

    # =========================
    # TIP / END
    # =========================

    if length > 30:

        tip_size = 5

        glow_draw.ellipse(
            (
                end_x - 10,
                end_y - 10,
                end_x + 10,
                end_y + 10
            ),
            fill=(190, 225, 255, 80)
        )

        draw.ellipse(
            (
                end_x - tip_size,
                end_y - tip_size,
                end_x + tip_size,
                end_y + tip_size
            ),
            fill=(235, 245, 255, 210)
        )

    # =========================
    # MOTION GLOW
    # =========================

    glow = glow.filter(
        ImageFilter.GaussianBlur(9)
    )

    img = Image.alpha_composite(
        glow,
        img
    )

    # =========================
    # SAVE
    # =========================

    filename = os.path.join(
        OUTPUT_DIR,
        f"web_{frame_number:02d}.png"
    )

    img.save(filename)


# =========================
# GENERATE ALL FRAMES
# =========================

print("Creating new cinematic web VFX...")

for i in range(FRAMES):

    create_frame(i)

    print(
        f"Created web_{i:02d}.png"
    )

print()
print("DONE!")
print(f"{FRAMES} transparent web frames created.")
