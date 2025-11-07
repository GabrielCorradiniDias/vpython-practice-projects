from vpython import canvas, cone, cylinder, sphere, box, vector, color, rate, local_light, triangle, vertex
import random, math

# ---------------- Scene Setup ----------------
scene = canvas(title="Christmas Night Scene 🎄🌙✨",
               width=900, height=650, background=vector(0.02, 0.02, 0.05))

# ---------------- Tree Setup ----------------
tree_height = 12
tree_levels = 5
base_radius = 4

# Infinite snowy ground
ground = box(pos=vector(0, -tree_height/2 - 0.5, 0),
             size=vector(200, 0.1, 200),
             color=vector(0.9, 0.9, 1),
             shininess=0.8,
             emissive=False)

# Tree trunk
trunk = cylinder(pos=vector(0, -tree_height/2, 0),
                 axis=vector(0, tree_height/6, 0),
                 radius=0.5,
                 color=vector(0.55, 0.27, 0.07))

# Tree layers
for i in range(tree_levels):
    level_height = tree_height / (tree_levels + 1)
    level_radius = base_radius - (i * 0.7)
    level_y = -tree_height / 2 + trunk.axis.y + (i * (level_height * 0.8))
    cone(pos=vector(0, level_y, 0),
         axis=vector(0, level_height, 0),
         radius=level_radius,
         color=vector(0, 0.5 + i * 0.1, 0))

# ---------------- Ornaments ----------------
ornament_colors = [color.red, color.blue, color.cyan, color.magenta, color.orange, color.yellow, color.green]
ornaments = []

num_ornaments = 180
for i in range(num_ornaments):
    level = random.randint(0, tree_levels - 1)
    level_height = tree_height / (tree_levels + 1)
    y = -tree_height / 2 + trunk.axis.y + (level * (level_height * 0.8)) + random.uniform(-0.3, 0.3)
    if y > tree_height / 4:  # avoid star zone
        continue
    r = (base_radius - (level * 0.7)) * random.uniform(0.7, 0.95)
    theta = random.uniform(0, 2 * math.pi)
    x = r * math.cos(theta)
    z = r * math.sin(theta)
    ornaments.append(
        sphere(pos=vector(x, y, z),
               radius=random.uniform(0.12, 0.18),
               color=random.choice(ornament_colors),
               emissive=True)
    )

# ---------------- 3D Five-Point Star ----------------
def create_3d_star(pos, size=1.0, col=color.yellow):
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        radius = size if i % 2 == 0 else size * 0.4
        points.append(vector(radius * math.cos(angle), radius * math.sin(angle), 0))

    faces = []
    for i in range(10):
        p1 = points[i]
        p2 = points[(i + 1) % 10]
        tip_front = vector(0, 0, size / 2)
        tip_back = vector(0, 0, -size / 2)
        faces.append(triangle(vs=[
            vertex(pos=p1 + pos, color=col),
            vertex(pos=p2 + pos, color=col),
            vertex(pos=tip_front + pos, color=col)
        ]))
        faces.append(triangle(vs=[
            vertex(pos=p1 + pos, color=col),
            vertex(pos=p2 + pos, color=col),
            vertex(pos=tip_back + pos, color=col)
        ]))
    return faces

# Add the star
star_pos = vector(0, tree_height / 2.8 + 0.8, 0)
star = create_3d_star(star_pos, size=0.8, col=color.yellow)

# ---------------- Presents ----------------
def create_present(pos, size=vector(1, 0.6, 1), body_color=color.red):
    gift = box(pos=pos, size=size, color=body_color)
    ribbon_thickness = 0.08
    ribbon_color = vector(1, 0.84, 0)
    box(pos=pos, size=vector(ribbon_thickness, size.y + 0.01, size.z + 0.01), color=ribbon_color)
    box(pos=pos, size=vector(size.x + 0.01, size.y + 0.01, ribbon_thickness), color=ribbon_color)
    return gift

present_colors = [color.red, color.green]
for _ in range(6):
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(1.5, 3.5)
    x = radius * math.cos(angle)
    z = radius * math.sin(angle)
    pos = vector(x, -tree_height/2 + 0.3, z)
    present_color = random.choice(present_colors)
    size = vector(random.uniform(0.7, 1.2), random.uniform(0.5, 0.8), random.uniform(0.7, 1.2))
    create_present(pos, size, present_color)

# ---------------- Mountains ----------------
for i in range(-3, 4):
    height = random.uniform(6, 12)
    radius = random.uniform(10, 16)
    x_pos = i * 15 + random.uniform(-3, 3)
    z_pos = -40 + random.uniform(-5, 5)
    cone(pos=vector(x_pos, -tree_height/2 - 0.5, z_pos),
         axis=vector(0, height, 0),
         radius=radius,
         color=vector(0.6, 0.65, 0.7),
         opacity=0.9)

# ---------------- Moon ----------------
moon = sphere(pos=vector(15, 15, -60),
              radius=3,
              color=vector(1, 1, 0.9),
              emissive=True)

# ---------------- Stars in the sky ----------------
sky_stars = []
for _ in range(200):
    x = random.uniform(-100, 100)
    y = random.uniform(5, 40)
    z = random.uniform(-120, -40)
    sky_stars.append(sphere(pos=vector(x, y, z),
                            radius=random.uniform(0.05, 0.15),
                            color=color.white,
                            emissive=True))

# ---------------- Snowfall ----------------
snowflakes = [sphere(pos=vector(random.uniform(-10, 10),
                                random.uniform(0, 8),
                                random.uniform(-10, 10)),
                     radius=0.05,
                     color=color.white)
              for _ in range(200)]

# ---------------- Lighting ----------------
local_light(pos=vector(0, 5, 5), color=color.white)
local_light(pos=vector(0, 10, -10), color=vector(1, 1, 0.8))  # moonlight tone

# ---------------- Animation ----------------
angle = 0
while True:
    rate(60)
    angle += 0.02

    # Rotate star
    for f in star:
        for v in f.vs:
            v.pos = vector(
                (v.pos.x - star_pos.x) * math.cos(0.02) - (v.pos.z - star_pos.z) * math.sin(0.02) + star_pos.x,
                v.pos.y,
                (v.pos.x - star_pos.x) * math.sin(0.02) + (v.pos.z - star_pos.z) * math.cos(0.02) + star_pos.z
            )

    # Twinkle effect
    twinkle = 0.7 + 0.3 * math.sin(angle * 6)
    warm_shift = 0.1 * math.sin(angle * 3)
    star_color = vector(1, twinkle, 0.2 + warm_shift)
    for f in star:
        for v in f.vs:
            v.color = star_color

    # Gentle twinkling of random sky stars
    for s in random.sample(sky_stars, 8):
        s.radius = 0.05 + 0.05 * abs(math.sin(angle * random.uniform(3, 6)))

    # Snowfall
    for s in snowflakes:
        s.pos.y -= 0.05
        if s.pos.y < -tree_height/2:
            s.pos.y = random.uniform(5, 10)
            s.pos.x = random.uniform(-10, 10)
            s.pos.z = random.uniform(-10, 10)
