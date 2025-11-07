# vacuum_chamber_improved.py
from vpython import *
import random, math

# === Scene setup ===
scene = canvas(title='Vacuum Chamber — improved',
               width=1000, height=700, background=color.black)

# === CHAMBER GEOMETRY ===
chamber_radius = 3
chamber_length = 8
chamber_center_y = 0        # keep chamber centered at y=0

chamber_body = cylinder(pos=vector(-chamber_length/2, chamber_center_y, 0),
                        axis=vector(chamber_length, 0, 0),
                        radius=chamber_radius,
                        color=vector(0.2, 0.9, 1),
                        opacity=0.25)

cap_thickness = 0.2
cap_left = cylinder(pos=vector(-chamber_length/2 - cap_thickness/2, chamber_center_y, 0),
                    axis=vector(cap_thickness, 0, 0),
                    radius=chamber_radius,
                    color=color.gray(0.6))
cap_right = cylinder(pos=vector(chamber_length/2 + cap_thickness/2, chamber_center_y, 0),
                     axis=vector(cap_thickness, 0, 0),
                     radius=chamber_radius,
                     color=color.gray(0.6))

window = cylinder(pos=vector(chamber_length/2 + cap_thickness, chamber_center_y, 0),
                  axis=vector(0.3, 0, 0),
                  radius=1,
                  color=color.cyan,
                  opacity=0.4)

# === BASE & SUPPORT PLATES (metallic) ===
base = box(pos=vector(0, -chamber_radius - 0.7, 0),
           size=vector(chamber_length * 1.3, 0.5, chamber_radius * 1.6),
           color=vector(0.1, 0.7, 0.3),
           shininess=0.8)

plate_thickness = 0.08
plate_height = chamber_radius * 0.9
plate_width = chamber_radius * 1.1
plate_y_pos = -chamber_radius / 2 - 0.7

metal_color = vector(0.82, 0.84, 0.87)   # bluish-silver

plate_left = box(pos=vector(-chamber_length/2 + 0.15, plate_y_pos, 0),
                 size=vector(plate_thickness, plate_height, plate_width),
                 color=metal_color,
                 shininess=1.0,
                 opacity=0.95)

plate_right = box(pos=vector(chamber_length/2 - 0.15, plate_y_pos, 0),
                  size=vector(plate_thickness, plate_height, plate_width),
                  color=metal_color,
                  shininess=1.0,
                  opacity=0.95)

# === MEMS ARRAY (unchanged) ===
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
        torus = ring(pos=vector(x, chamber_center_y, z),
                     axis=vector(1, 0, 0),
                     radius=ring_radius,
                     thickness=0.1,
                     color=color.red)
        rings.append(torus)

# label the array
label(pos=vector(0, chamber_center_y + 0.9, 0),
      text='MEMS Array', xoffset=0, yoffset=0, height=14, color=color.white, box=False)

# === OUTER CONTAINMENT RING (outside chamber, static) ===
outer_field = ring(pos=vector(chamber_length/2 + 0.7, chamber_center_y, 0),
                   axis=vector(1, 0, 0),
                   radius=2.8,
                   thickness=0.25,
                   color=vector(0.22, 0.9, 1),
                   opacity=0.25,
                   emissive=True)

label(pos=vector(chamber_length/2 + 1.4, chamber_center_y + 0.9, 0),
      text='Outer Field', height=12, box=False, color=color.white)

# === INNER CONTAINMENT RING (inside chamber, pulses out-of-phase) ===
inner_field = ring(pos=vector(0, chamber_center_y, 0),
                   axis=vector(1, 0, 0),
                   radius=chamber_radius - 0.5,   # smaller so it sits inside
                   thickness=0.18,
                   color=vector(1, 0.4, 0.9),     # slightly magenta tint
                   opacity=0.22,
                   emissive=True)

label(pos=vector(0, chamber_center_y + 1.1, -2.2),
      text='Inner Field', height=12, box=False, color=color.white)

# === SIMULATED SOLENOID COILS (rings as turns) ===
coil_turns = []
n_turns = 18
coil_radius = chamber_radius * 1.25
start_x = -chamber_length/2 + 0.3
end_x = chamber_length/2 - 0.3
for t in range(n_turns):
    tx = start_x + (end_x - start_x) * t / (n_turns - 1)
    turn = ring(pos=vector(tx, chamber_center_y, 0),
                axis=vector(1, 0, 0),
                radius=coil_radius,
                thickness=0.03,
                color=vector(0.6, 0.6, 0.65),
                opacity=0.9)
    coil_turns.append(turn)

label(pos=vector(0, chamber_center_y - (coil_radius + 0.6), 0),
      text='Drive coils (simulated turns)', height=10, box=False, color=color.white)

# === VACUUM PARTICLES (unchanged) ===
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

# === CAMERA & STATIC LIGHTS ===
scene.camera.pos = vector(8, 2, 6)
scene.camera.axis = vector(-8, -2, -6)
distant_light(direction=vector(-1, -1, -1), color=vector(1,1,1))
distant_light(direction=vector(1, 0.5, 1), color=vector(0.7,0.8,1))

# === ANIMATION LOOP: MEMS rotate, fields pulse (outer & inner out of phase), particles move ===
theta = 0
while True:
    rate(60)
    theta += 0.02

    # rotate MEMS rings
    for torus in rings:
        x, y, z = torus.pos.x, torus.pos.y, torus.pos.z
        torus.pos = vector(
            x * cos(0.02) - z * sin(0.02),
            y,
            x * sin(0.02) + z * cos(0.02)
        )

    # particle motion and shimmer
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

    # outer field pulse (synchronized)
    outer_intensity = 0.25 + 0.12 * (1 + sin(theta * 2))
    outer_color_shift = 0.9 + 0.15 * sin(theta * 1.3)
    outer_field.opacity = outer_intensity
    outer_field.color = vector(0.22, outer_color_shift, 1)

    # inner field pulses out of phase with outer (pi offset)
    inner_intensity = 0.22 + 0.12 * (1 + sin(theta * 2 + math.pi))
    inner_color_shift = 0.7 + 0.2 * sin(theta * 1.7 + math.pi/4)
    inner_field.opacity = inner_intensity
    inner_field.color = vector(inner_color_shift, 0.4, 0.9)

    # coils: very subtle phasing glow along coils to suggest current
    for i, turn in enumerate(coil_turns):
        turn.opacity = 0.6 + 0.15 * math.sin(theta * 2 + i * 0.3)
