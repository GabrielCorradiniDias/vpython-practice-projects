from vpython import *
import math

# Create the 3D scene
scene = canvas(title='Cone inside Box (orbit + bounce)', width=800, height=600)

# Transparent cyan cube
box(pos=vector(0,0,0), size=vector(4,4,4), color=color.cyan, opacity=0.3)

# Red cone
cone_obj = cone(pos=vector(1,0,0), axis=vector(0,1,0), radius=0.5, color=color.red)

# Animation variables
angle = 0
t = 0

while True:
    rate(60)
    angle += 0.03
    t += 0.05

    # Smaller orbit to stay within cube boundaries (max ~1.5 from center)
    x = 1.2 * math.sin(angle)
    z = 1.2 * math.cos(angle)

    # Gentle bounce within top/bottom faces
    y = 0.8 * math.sin(t)

    # Update position
    cone_obj.pos = vector(x, y, z)

    # Spin around its own axis
    cone_obj.rotate(angle=0.05, axis=vector(0,1,0))
