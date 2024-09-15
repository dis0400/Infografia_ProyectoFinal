import arcade
import random
import math

import arcade.color

class Boid:
    def __init__(self, x, y):
        self.position = [x, y]  
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.acceleration = [0, 0]
        self.max_speed = 4
        self.max_force = 0.1
        self.size = 10 
        self.perception_radius = 50  
        self.touched_triangle = False
        self.color = arcade.color.WHITE


    def distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def update(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.velocity = self.normalize(self.velocity)
        self.velocity = [self.velocity[0] * self.max_speed, self.velocity[1] * self.max_speed]
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.acceleration = [0, 0]

    def apply_force(self, force):
        self.acceleration[0] += force[0]
        self.acceleration[1] += force[1]

    def edges(self, width, height):
        if self.position[0] > width:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = width
        if self.position[1] > height:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = height

    def separation(self, boids):
        desired_separation = 25 
        steer = [0, 0]
        total = 0

        for other in boids:
            distance = self.distance(self.position, other.position)
            if self != other and distance > 0:
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
            return self.seek(center_of_mass) 
        return [0, 0]

    def seek(self, target):
        desired = [target[0] - self.position[0], target[1] - self.position[1]]
        desired = self.normalize(desired)
        desired = [desired[0] * self.max_speed, desired[1] * self.max_speed]
        steer = [desired[0] - self.velocity[0], desired[1] - self.velocity[1]]
        steer = self.normalize(steer)
        steer = [steer[0] * self.max_force, steer[1] * self.max_force]
        return steer

    def avoid_obstacles(self, obstacles, boids):
        steer = [0, 0]
        total = 0
        safe_distance = 80  
        max_avoid_force = 0.3
        rotation_force = 0.05  
        safe_distance_triangle = 20 
        boids_to_add = 1  
       

        for obstacle in obstacles:
            distance = self.distance(self.position, obstacle)
            if obstacle[2] == "triangle":
                if distance < safe_distance_triangle:
                    if not self.touched_triangle:  
                        new_boid = Boid(self.position[0] + random.randint(-10, 10), self.position[1] + random.randint(-10, 10))
                        boids.append(new_boid)
                        self.touched_triangle = True  
                        return [0, 0]  
                continue
            
            if distance < safe_distance:  
                diff = [self.position[0] - obstacle[0], self.position[1] - obstacle[1]]
                diff = self.normalize(diff)
                
                #  rodear obst
                if distance < 50:  
                    tangent = [-diff[1], diff[0]]  
                    steer[0] += tangent[0] * rotation_force
                    steer[1] += tangent[1] * rotation_force
                else:
                    diff = [diff[0] / (distance ** 2), diff[1] / (distance ** 2)]
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
                steer = [steer[0] * max_avoid_force, steer[1] * max_avoid_force]

        return steer

    def apply_behaviors(self, boids, obstacles, behavior_mode):
        obstacle_avoidance = [0, 0]
        
        if behavior_mode == "cohesion":
            cohesion_force = self.cohesion(boids)
            cohesion_force = [cohesion_force[0] * 1.0, cohesion_force[1] * 1.0]
            self.apply_force(cohesion_force)
        elif behavior_mode == "alignment":
            alignment_force = self.alignment(boids)
            alignment_force = [alignment_force[0] * 1.0, alignment_force[1] * 1.0]
            self.apply_force(alignment_force)
        elif behavior_mode == "separation":
            separation_force = self.separation(boids)
            separation_force = [separation_force[0] * 1.5, separation_force[1] * 1.5]
            self.apply_force(separation_force)
        else:
            separation_force = self.separation(boids)
            alignment_force = self.alignment(boids)
            cohesion_force = self.cohesion(boids)
            obstacle_avoidance = self.avoid_obstacles(obstacles, boids) 

            separation_force = [separation_force[0] * 1.5, separation_force[1] * 1.5]
            alignment_force = [alignment_force[0] * 1.0, alignment_force[1] * 1.0]
            cohesion_force = [cohesion_force[0] * 1.0, cohesion_force[1] * 1.0]
            obstacle_avoidance = [obstacle_avoidance[0] * 2.0, obstacle_avoidance[1] * 2.0]

            self.apply_force(separation_force)
            self.apply_force(alignment_force)
            self.apply_force(cohesion_force)
            self.apply_force(obstacle_avoidance)


    def draw(self):
        angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0]))
        arcade.draw_triangle_filled(
            self.position[0] + math.cos(math.radians(angle)) * self.size,
            self.position[1] + math.sin(math.radians(angle)) * self.size,
            self.position[0] + math.cos(math.radians(angle + 140)) * (self.size / 2),
            self.position[1] + math.sin(math.radians(angle + 140)) * (self.size / 2),
            self.position[0] + math.cos(math.radians(angle - 140)) * (self.size / 2),
            self.position[1] + math.sin(math.radians(angle - 140)) * (self.size / 2),
            self.color
        )

    def magnitude(self, vector):
        return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

    def normalize(self, vector):
        mag = self.magnitude(vector)
        if mag > 0:
            return [vector[0] / mag, vector[1] / mag]
        return vector
