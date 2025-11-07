from vpython import *
import random

# === METALLIC SUPPORT PLATES ADDED ====

# === Scene setup ===
scene = canvas(title='Vacuum Chamber Visualization',
               width=1000, height=700, background=color.black)

# === CHAMBER BODY ===
chamber_radius = 3
chamber_length = 8

chamber_body = cylinder(pos=vector(-chamber_length/2, 0, 0),
                        axis=vector(chamber_length, 0, 0),
                        radius=chamber_radius,
                        color=vector(0.2, 0.9, 1),
                        opacity=0.25)

cap_thickness = 0.2
cap_left = cylinder(pos=vector(-chamber_length/2 - cap_thickness/2, 0, 0),
                    axis=vector(cap_thickness, 0, 0),
                    radius=chamber_radius,
                    color=color.gray(0.6))
cap_right = cylinder(pos=vector(chamber_length/2 + cap_thickness/2, 0, 0),
                     axis=vector(cap_thickness, 0, 0),
                     radius=chamber_radius,
                     color=color.gray(0.6))

window = cylinder(pos=vector(chamber_length/2 + cap_thickness, 0, 0),
                  axis=vector(0.3, 0, 0),
                  radius=1,
                  color=color.cyan,
                  opacity=0.4)

# === BASE ===
base = box(pos=vector(0, -chamber_radius - 0.7, 0),
           size=vector(chamber_length * 1.3, 0.5, chamber_radius * 1.6),
           color=vector(0.1, 0.7, 0.3),
           shininess=0.8)

# === SUPPORT PLATES (metallic finish) ===
plate_thickness = 0.1
plate_height = chamber_radius * 0.9
plate_width = chamber_radius * 1.1
plate_y_pos = -chamber_radius / 2 - 0.7

# metallic color — slightly bluish silver
metal_color = vector(0.8, 0.85, 0.9)

plate_left = box(pos=vector(-chamber_length/2 + 0.15, plate_y_pos, 0),
                 size=vector(plate_thickness, plate_height, plate_width),
                 color=metal_color,
                 shininess=1.0,
                 emissive=False,
                 opacity=0.9)

plate_right = box(pos=vector(chamber_length/2 - 0.15, plate_y_pos, 0),
                  size=vector(plate_thickness, plate_height, plate_width),
                  color=metal_color,
                  shininess=1.0,
                  emissive=False,
                  opacity=0.9)

# === MEMS ARRAY ===
rings = []
rows, cols = 3, 3
ring_radius = 0.4
spacing = 1.2
x_offset = -(cols - 1) * spacing / 2
z_offset = -(rows - 1) * spacing / 2

for i in range(cols):
    for j in range(rows):
        x = x_offset + i * spacing
        z = z_offset + j * spacing
        torus = ring(pos=vector(x, 0, z),
                     axis=vector(1, 0, 0),
                     radius=ring_radius,
                     thickness=0.1,
                     color=color.red)
        rings.append(torus)

# === CONTAINMENT FIELD RING ===
containment_field = ring(
    pos=vector(chamber_length/2 + 0.7, 0, 0),
    axis=vector(1, 0, 0),
    radius=2.8,
    thickness=0.25,
    color=vector(0.3, 0.9, 1),
    opacity=0.25,
    emissive=True
)

# === PARTICLES ===
num_particles = 40
particles = []

for i in range(num_particles):
    x = random.uniform(-chamber_length/2.5, chamber_length/2.5)
    y = random.uniform(-chamber_radius*0.7, chamber_radius*0.7)
    z = random.uniform(-chamber_radius*0.7, chamber_radius*0.7)
    p = sphere(pos=vector(x, y, z),
               radius=0.08,
               color=vector(0.5, 0.8, 1),
               emissive=True,
               opacity=0.8)
    p.v = vector(random.uniform(-0.02, 0.02),
                 random.uniform(-0.02, 0.02),
                 random.uniform(-0.02, 0.02))
    particles.append(p)

# === CAMERA & LIGHTING ===
scene.camera.pos = vector(8, 2, 6)
scene.camera.axis = vector(-8, -2, -6)

# key lighting for metal reflection
distant_light(direction=vector(-1, -1, -1), color=vector(1, 1, 1))
distant_light(direction=vector(1, 0.5, 1), color=vector(0.7, 0.8, 1))

# === ANIMATION ===
theta = 0
while True:
    rate(60)
    theta += 0.02

    # Rotate MEMS rings
    for torus in rings:
        x, y, z = torus.pos.x, torus.pos.y, torus.pos.z
        torus.pos = vector(
            x * cos(0.02) - z * sin(0.02),
            y,
            x * sin(0.02) + z * cos(0.02)
        )

    # Pulsating lighting
    glow_intensity = 0.8 + 0.6 * sin(theta * 1.5)
    scene.lights = []
    local_light(pos=vector(0, 0, 0),
                color=vector(0.2, 0.6 + glow_intensity, 1))
    local_light(pos=vector(5, 3, 5),
                color=vector(1, 1, 0.8) * 0.6)
    local_light(pos=vector(-5, -3, -5),
                color=vector(0.3, 0.6, 1) * 0.7)

    # Chamber glow
    chamber_body.opacity = 0.25 + 0.05 * abs(sin(theta))
    chamber_body.color = vector(0.2, 0.9, 1)

    # Particle motion
    for p in particles:
        p.pos += p.v
        if abs(p.pos.x) > chamber_length/2.5:
            p.v.x *= -1
        if abs(p.pos.y) > chamber_radius*0.7:
            p.v.y *= -1
        if abs(p.pos.z) > chamber_radius*0.7:
            p.v.z *= -1
        p.color = vector(0.4 + 0.4 * sin(theta + p.pos.x),
                         0.7 + 0.3 * sin(theta * 1.5 + p.pos.z),
                         1)
