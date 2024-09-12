import arcade
import random
import math

class Boid:
    def __init__(self, x, y):
        self.position = [x, y]  # Usamos una lista para la posición [x, y]
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.acceleration = [0, 0]
        self.max_speed = 4
        self.max_force = 0.1
        self.size = 10  # Tamaño del triángulo
        self.perception_radius = 50  # Radio de percepción para los boids cercanos

    def distance(self, point1, point2):
        # Función para calcular la distancia entre dos puntos
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def update(self):
        # Actualiza la posición y la velocidad
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.velocity = self.normalize(self.velocity)
        self.velocity = [self.velocity[0] * self.max_speed, self.velocity[1] * self.max_speed]
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.acceleration = [0, 0]

    def apply_force(self, force):
        # Aplica una fuerza a la aceleración
        self.acceleration[0] += force[0]
        self.acceleration[1] += force[1]

    def edges(self, width, height):
        # Maneja los bordes de la pantalla
        if self.position[0] > width:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = width
        if self.position[1] > height:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = height

    def separation(self, boids):
        # Evita estar demasiado cerca de otros boids
        desired_separation = 25  # Distancia mínima entre boids
        steer = [0, 0]
        total = 0

        for other in boids:
            distance = self.distance(self.position, other.position)
            if self != other and distance < desired_separation:
                diff = [self.position[0] - other.position[0], self.position[1] - other.position[1]]
                diff = self.normalize(diff)
                diff = [diff[0] / distance, diff[1] / distance]
                steer[0] += diff[0]
                steer[1] += diff[1]
                total += 1

        if total > 0:
            steer[0] /= total
            steer[1] /= total

        if self.magnitude(steer) > 0:
            steer = self.normalize(steer)
            steer = [steer[0] * self.max_speed, steer[1] * self.max_speed]
            steer[0] -= self.velocity[0]
            steer[1] -= self.velocity[1]
            steer = self.normalize(steer)
            steer = [steer[0] * self.max_force, steer[1] * self.max_force]
        return steer

    def alignment(self, boids):
        # Ajusta la dirección para alinearse con los boids cercanos
        perception_radius = self.perception_radius
        avg_velocity = [0, 0]
        total = 0

        for other in boids:
            distance = self.distance(self.position, other.position)
            if self != other and distance < perception_radius:
                avg_velocity[0] += other.velocity[0]
                avg_velocity[1] += other.velocity[1]
                total += 1

        if total > 0:
            avg_velocity[0] /= total
            avg_velocity[1] /= total
            avg_velocity = self.normalize(avg_velocity)
            avg_velocity = [avg_velocity[0] * self.max_speed, avg_velocity[1] * self.max_speed]
            steer = [avg_velocity[0] - self.velocity[0], avg_velocity[1] - self.velocity[1]]
            steer = self.normalize(steer)
            steer = [steer[0] * self.max_force, steer[1] * self.max_force]
            return steer
        return [0, 0]

    def cohesion(self, boids):
        # Mueve el boid hacia el centro de masa de los boids cercanos
        perception_radius = self.perception_radius
        center_of_mass = [0, 0]
        total = 0

        for other in boids:
            distance = self.distance(self.position, other.position)
            if self != other and distance < perception_radius:
                center_of_mass[0] += other.position[0]
                center_of_mass[1] += other.position[1]
                total += 1

        if total > 0:
            center_of_mass[0] /= total
            center_of_mass[1] /= total
            return self.seek(center_of_mass)  # Moverse hacia el centro de masa
        return [0, 0]

    def seek(self, target):
        # Apunta hacia un objetivo
        desired = [target[0] - self.position[0], target[1] - self.position[1]]
        desired = self.normalize(desired)
        desired = [desired[0] * self.max_speed, desired[1] * self.max_speed]
        steer = [desired[0] - self.velocity[0], desired[1] - self.velocity[1]]
        steer = self.normalize(steer)
        steer = [steer[0] * self.max_force, steer[1] * self.max_force]
        return steer

    def avoid_obstacles(self, obstacles):
        # Evitar los obstáculos
        steer = [0, 0]
        total = 0
        safe_distance = 80  # Aumentar la distancia para empezar a evitar los obstáculos antes
        max_avoid_force = 0.5  # Incrementar la fuerza máxima de evitación

        for obstacle in obstacles:
            distance = self.distance(self.position, obstacle)
            if distance < safe_distance:  # Si está dentro del rango seguro
                diff = [self.position[0] - obstacle[0], self.position[1] - obstacle[1]]
                diff = self.normalize(diff)
                # Aplicar una fuerza inversamente proporcional a la distancia
                diff = [diff[0] / (distance ** 2), diff[1] / (distance ** 2)]
                steer[0] += diff[0]
                steer[1] += diff[1]
                total += 1

        if total > 0:
            steer[0] /= total
            steer[1] /= total

            # Asegurarse de que la magnitud de la fuerza sea adecuada
            if self.magnitude(steer) > 0:
                steer = self.normalize(steer)
                steer = [steer[0] * self.max_speed, steer[1] * self.max_speed]
                steer[0] -= self.velocity[0]
                steer[1] -= self.velocity[1]

                # Aumentar la fuerza de evasión de obstáculos
                steer = self.normalize(steer)
                steer = [steer[0] * max_avoid_force, steer[1] * max_avoid_force]

        return steer
    
    def apply_behaviors(self, boids, obstacles):
        # Aplica las reglas de flocking
        separation_force = self.separation(boids)
        alignment_force = self.alignment(boids)
        cohesion_force = self.cohesion(boids)
        obstacle_avoidance = self.avoid_obstacles(obstacles)  # Evitar los obstáculos

        # Ajusta los pesos de las fuerzas
        obstacle_avoidance = [obstacle_avoidance[0] * 3.0, obstacle_avoidance[1] * 3.0]  # Dar más peso a la evasión de obstáculos
        separation_force = [separation_force[0] * 1.5, separation_force[1] * 1.5]
        alignment_force = [alignment_force[0] * 1.0, alignment_force[1] * 1.0]
        cohesion_force = [cohesion_force[0] * 1.0, cohesion_force[1] * 1.0]

        # Aplica las fuerzas
        self.apply_force(obstacle_avoidance)  # Aplica la fuerza de evitar obstáculos primero
        self.apply_force(separation_force)
        self.apply_force(alignment_force)
        self.apply_force(cohesion_force)

    def draw(self):
        # Dibuja el boid como un triángulo en Arcade
        angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0]))
        arcade.draw_triangle_filled(
            self.position[0] + math.cos(math.radians(angle)) * self.size,
            self.position[1] + math.sin(math.radians(angle)) * self.size,
            self.position[0] + math.cos(math.radians(angle + 140)) * (self.size / 2),
            self.position[1] + math.sin(math.radians(angle + 140)) * (self.size / 2),
            self.position[0] + math.cos(math.radians(angle - 140)) * (self.size / 2),
            self.position[1] + math.sin(math.radians(angle - 140)) * (self.size / 2),
            arcade.color.WHITE
        )

    # Helper functions for vector math
    def magnitude(self, vector):
        return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

    def normalize(self, vector):
        mag = self.magnitude(vector)
        if mag > 0:
            return [vector[0] / mag, vector[1] / mag]
        return vector
