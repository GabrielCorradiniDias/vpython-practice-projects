from vpython import *
import math

scene = canvas(title='UFO inside Box', width=800, height=600)

# Transparent cube box
box(pos=vector(0,0,0), size=vector(4,4,4), color=color.cyan, opacity=0.3)

# === UFO MODEL ===
# Local offsets (relative to UFO center)
ufo_center = vector(0, 0, 0)

# Saucer base
saucer = ellipsoid(pos=ufo_center, length=1.8, height=0.4, width=1.8, color=color.gray(0.5))

# Dome on top (offset from center)
dome_offset = vector(0, 0.35, 0)
dome = sphere(pos=ufo_center + dome_offset, radius=0.4, color=color.green, opacity=0.7)

# Rim lights (around saucer edge)
lights = []
num_lights = 8
for i in range(num_lights):
    angle = 2 * math.pi * i / num_lights
    offset = vector(0.9 * math.cos(angle), -0.1, 0.9 * math.sin(angle))
    light = sphere(pos=ufo_center + offset, radius=0.08, color=color.red)
    lights.append((light, offset))

# Group all UFO parts
ufo_parts = [saucer, dome] + [l for l, _ in lights]

# === ANIMATION ===
angle = 0
t = 0

while True:
    rate(60)
    angle += 0.03
    t += 0.05

    # Orbit + bounce inside box
    x = 1.2 * math.sin(angle)
    z = 1.2 * math.cos(angle)
    y = 0.8 * math.sin(t)
    ufo_pos = vector(x, y, z)

    # Rotation around Y-axis (UFO spins in place)
    rotation_angle = angle * 1.5
    cos_r = math.cos(rotation_angle)
    sin_r = math.sin(rotation_angle)

    # Update saucer position (center)
    saucer.pos = ufo_pos

    # Update dome (fixed offset rotated around center)
    rotated_dome_offset = vector(
        cos_r * dome_offset.x + sin_r * dome_offset.z,
        dome_offset.y,
        -sin_r * dome_offset.x + cos_r * dome_offset.z
    )
    dome.pos = ufo_pos + rotated_dome_offset

    # Update lights around rim (rotating with the saucer)
    for light, offset in lights:
        rotated_offset = vector(
            cos_r * offset.x + sin_r * offset.z,
            offset.y,
            -sin_r * offset.x + cos_r * offset.z
        )
        light.pos = ufo_pos + rotated_offset

    # Light color pulse effect
    for i, (light, _) in enumerate(lights):
        hue = (math.sin(t * 2 + i) + 1) / 2
        light.color = vector(1 - hue, hue, 0)
