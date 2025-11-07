from vpython import *
import math

# === Scene setup ===
scene = canvas(title="MEMS Toroidal Cavity Array", width=900, height=600)
scene.background = color.black
scene.lights = []  # remove default light for softer glow
distant_light(direction=vector(1,1,1), color=color.white)

# === Parameters ===
wafer_size = 6
wafer_thickness = 0.2
num_rings_x = 6
num_rings_y = 6
ring_spacing = 0.8
ring_radius = 0.3
tube_radius = 0.08
ring_color = vector(0.2, 0.7, 1.0)

# === Wafer substrate ===
wafer = box(
    pos=vector(0, -wafer_thickness / 2, 0),
    size=vector(wafer_size, wafer_thickness, wafer_size),
    color=vector(0.3, 0.3, 0.35),
    opacity=0.7
)

# === Transparent dome enclosure ===
dome = sphere(
    pos=vector(0, 0, 0),
    radius=wafer_size * 0.7,
    color=color.cyan,
    opacity=0.25
)

# === Toroidal array ===
rings = []
x_offset = -(num_rings_x - 1) * ring_spacing / 2
z_offset = -(num_rings_y - 1) * ring_spacing / 2

for i in range(num_rings_x):
    for j in range(num_rings_y):
        x = x_offset + i * ring_spacing
        z = z_offset + j * ring_spacing
        y = 0
        torus = ring(pos=vector(x, y, z),
                     axis=vector(0, 1, 0),
                     radius=ring_radius,
                     thickness=tube_radius,
                     color=ring_color,
                     emissive=True)  # makes it look self-lit
        rings.append(torus)

# === Glow effect ===
glow_spheres = []
for torus in rings:
    glow = sphere(pos=torus.pos, radius=0.05, color=color.cyan, emissive=True, opacity=0.5)
    glow_spheres.append(glow)

# === Animation ===
angle = 0
t = 0
while True:
    rate(60)
    angle += 0.01
    t += 0.05

    # rotate array
    for torus, glow in zip(rings, glow_spheres):
        torus.rotate(angle=0.01, axis=vector(0,1,0), origin=vector(0,0,0))
        glow.rotate(angle=0.01, axis=vector(0,1,0), origin=vector(0,0,0))

        # subtle pulsation in brightness
        intensity = 0.5 + 0.5 * math.sin(t + torus.pos.x + torus.pos.z)
        glow.color = vector(0.1, 0.8 * intensity, 1.0 * intensity)
