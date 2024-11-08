from vpython import sphere, vector, color, rate, scene, random, mag, norm, pi, cylinder, sin, cos

# Set up the 3D scene
scene.title = "3D Molecular Simulation Inside a Red Blood Cell"
scene.width = 800
scene.height = 600

# Parameters for the red blood cell
rbc_radius = 25  # Radius of the red blood cell structure

# Parameters for the core structure
num_cores = 6  # Increased number of cores
core_radius = 2
nucleus_radius = 0.5  # Radius of the nucleus
orbit_radius = 5

# Parameters for particles
num_particles = 150  # Increased number of particles
particle_radius = 0.3
spring_constant = 0.1  # Strength of attraction to core
single_bond_distance = 1.5
double_bond_distance = 1.0
triple_bond_distance = 0.5

# Red blood cell (RBC) enclosure
rbc = sphere(pos=vector(0, 0, 0), radius=rbc_radius, color=color.red, opacity=0.3)

# Generate cores and nuclei in random positions within the red blood cell
cores = []
for i in range(num_cores):
    core_pos = vector((random() - 0.5) * rbc_radius * 0.8, (random() - 0.5) * rbc_radius * 0.8, (random() - 0.5) * rbc_radius * 0.8)
    core = sphere(pos=core_pos, radius=core_radius, color=color.white, opacity=0.8)
    nucleus = sphere(pos=core_pos, radius=nucleus_radius, color=color.black, opacity=1)
    cores.append((core, nucleus))

# Generate particles with random colors around the cores
particles = []
for i in range(num_particles):
    core_index = int(random() * num_cores)
    core, _ = cores[core_index]
    theta = random() * 2 * pi
    phi = random() * pi
    x = core.pos.x + orbit_radius * sin(phi) * cos(theta)
    y = core.pos.y + orbit_radius * sin(phi) * sin(theta)
    z = core.pos.z + orbit_radius * cos(phi)
    particle_color = color.red if random() < 0.33 else (color.green if random() < 0.5 else color.blue)
    particle = sphere(pos=vector(x, y, z), radius=particle_radius, color=particle_color)
    particle.velocity = vector(random() - 0.25, random() - 0.25, random() - 0.25)
    particles.append(particle)

# List to store bonds
bonds = []

# Free-roaming camera movement setup
camera_speed = 0.5
camera_rotation_speed = 0.02
scene.forward = vector(0, 0, -1)  # Initial direction camera faces



# Bind keys to movement functions
scene.bind('keydown', lambda evt: move_forward() if evt.key == 'w' else
                            move_backward() if evt.key == 's' else
                            move_left() if evt.key == 'a' else
                            move_right() if evt.key == 'd' else
                            move_up() if evt.key == 'q' else
                            move_down() if evt.key == 'e' else
                            rotate_left() if evt.key == 'left' else
                            rotate_right() if evt.key == 'right' else
                            rotate_up() if evt.key == 'up' else
                            rotate_down() if evt.key == 'down' else None)
       
# Animation loop with molecular dynamics
while True:
    rate(120)
    for bond in bonds:
        bond.visible = False
    bonds.clear()

    for particle in particles:
        closest_core = min(cores, key=lambda core_nuc: mag(core_nuc[0].pos - particle.pos))
        core = closest_core[0]
        to_core = core.pos - particle.pos
        distance_to_core = mag(to_core)
        force_to_core = spring_constant * (distance_to_core - orbit_radius) * norm(to_core)
        particle.velocity += force_to_core

        # Repulsion between particles and bonding visualization
        for other in particles:
            if other != particle:
                distance = mag(particle.pos - other.pos)
                if distance < triple_bond_distance:
                    bond1 = cylinder(pos=particle.pos, axis=other.pos - particle.pos, radius=0.05, color=color.blue, emissive=True)
                    bond2 = cylinder(pos=particle.pos + vector(0.1, 0, 0), axis=other.pos - (particle.pos + vector(0.1, 0, 0)), radius=0.05, color=color.blue, emissive=True)
                    bond3 = cylinder(pos=particle.pos - vector(0.1, 0, 0), axis=other.pos - (particle.pos - vector(0.1, 0, 0)), radius=0.05, color=color.blue, emissive=True)
                    bonds.extend([bond1, bond2, bond3])

                elif distance < double_bond_distance:
                    bond1 = cylinder(pos=particle.pos, axis=other.pos - particle.pos, radius=0.05, color=color.green, emissive=True)
                    bond2 = cylinder(pos=particle.pos + vector(0.1, 0, 0), axis=other.pos - (particle.pos + vector(0.1, 0, 0)), radius=0.05, color=color.green, emissive=True)
                    bonds.extend([bond1, bond2])

                elif distance < single_bond_distance:
                    bond = cylinder(pos=particle.pos, axis=other.pos - particle.pos, radius=0.05, color=color.red, emissive=True)
                    bonds.append(bond)

        # Update particle position using its velocity
        particle.pos += particle.velocity * 0.1

        # Constrain particles within the red blood cell
        if mag(particle.pos) > rbc_radius - particle_radius:
            particle.pos = rbc_radius * norm(particle.pos)
            particle.velocity *= -0.5






