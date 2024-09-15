import arcade
import random
import math
from arcade import csscolor
from boid import Boid

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Simulador de Boids con Arcade"

class FlockingSimulation(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.boids = []
        self.obstacles = []  
        self.current_shape = "circle"  
        self.colors  = [  # Lista de colores válidos
            arcade.color.RED,
            arcade.color.BLUE,
            arcade.color.GREEN,
            arcade.color.YELLOW,
            arcade.color.ORANGE,
            arcade.color.PURPLE,
            arcade.color.PINK,
            arcade.color.CYAN,
            arcade.color.MAGENTA,
        ]
        self.group_colors ={}
        self.global_speed_multiplier = 1  # Controlar la velocidad de los boids
        self.behavior_mode = "normal"
                
    def setup(self):
        self.boids = [Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(50)]
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.C:
            self.current_shape = "circle"
        elif key == arcade.key.S:
            self.current_shape = "square"
        elif key == arcade.key.T:
            self.current_shape = "triangle"
        elif key == arcade.key.KEY_1:
            self.global_speed_multiplier = 0.2  # Velocidad lenta
        elif key == arcade.key.KEY_2:
            self.global_speed_multiplier = 1  # Velocidad normal
        elif key == arcade.key.KEY_3:
            self.global_speed_multiplier = 3  # Velocidad rápida
        elif key == arcade.key.KEY_4:
            self.global_speed_multiplier = 0  # Pausar
        elif key == arcade.key.J:
            self.behavior_mode = "cohesion"
        elif key == arcade.key.L:
            self.behavior_mode = "alignment"
        elif key == arcade.key.I:
            self.behavior_mode = "separation"
        elif key == arcade.key.N:
            self.behavior_mode = "normal"  # Restaurar comportamiento original

    def on_draw(self):      
        arcade.start_render()
        for boid in self.boids:
            boid.draw()
      
        for obstacle in self.obstacles:
            if obstacle[2] == "circle":
                arcade.draw_circle_filled(obstacle[0], obstacle[1], 10, arcade.color.RED)
            elif obstacle[2] == "square":
                arcade.draw_rectangle_filled(obstacle[0], obstacle[1], 20, 20, arcade.color.RED)
            elif obstacle[2] == "triangle":
                arcade.draw_triangle_filled(
                    obstacle[0], obstacle[1] + 15,
                    obstacle[0] - 15, obstacle[1] - 15, 
                    obstacle[0] + 15, obstacle[1] - 15, 
                    arcade.color.BLUE
                )

    def on_mouse_press(self, x, y, button, modifiers):
        self.obstacles.append((x, y, self.current_shape))

    def update(self, delta_time):
        self.update_groups() 
        
        if self.global_speed_multiplier > 0:  # Solo actualizar los boids si el multiplicador es mayor a 0
            for boid in self.boids:
                boid.max_speed *= self.global_speed_multiplier  # Aplicar el multiplicador global de velocidad
                boid.edges(SCREEN_WIDTH, SCREEN_HEIGHT)
                boid.apply_behaviors(self.boids, self.obstacles, self.behavior_mode)
                boid.update()
                boid.max_speed /= self.global_speed_multiplier  # Restablecer la velocidad original para el próximo ciclo
                
    def update_groups(self):
        group_threshold = 50  # Distancia para considerar boids como parte del mismo grupo
        groups = []  # Lista para almacenar los grupos de boids
        visited = set()  # Conjunto para rastrear boids ya asignados a un grupo

        for boid in self.boids:
            if boid not in visited:
                # Crear un nuevo grupo para cada boid no visitado
                current_group = []
                stack = [boid]
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        current_group.append(current)
                        # Considerar vecinos como parte del mismo grupo si están dentro del umbral
                        for neighbor in self.boids:
                            if neighbor not in visited and self.distance(boid.position, neighbor.position) < group_threshold:
                                stack.append(neighbor)
                groups.append(current_group)

        # Asignar un color único a cada grupo
                # Asignar un color a cada grupo de forma consistente
        new_group_colors = {}  # Temporal para los nuevos grupos
        for group in groups:
            group_id = tuple(sorted(tuple(boid.position) for boid in group))  # Convertir las posiciones a tuplas y luego crear una tupla para la ID del grupo
            if group_id in self.group_colors:
                group_color = self.group_colors[group_id]  # Mantener el color si el grupo ya existía
            else:
                group_color = random.choice(self.colors)  # Asignar un color aleatorio si es un nuevo grupo
            new_group_colors[group_id] = group_color  # Guardar el color del grupo

            for boid in group:
                boid.color = group_color  # Asignar color al boid

        self.group_colors = new_group_colors  # Actualizar los colores de los grupos


    def distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)    

if __name__ == "__main__":
    window = FlockingSimulation(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
# forma de cambiar los paraetros, la velocidad, parametros mientras se ejecute, conectar de forma dinamica
#hacer mas visual, los boids que se formen cambiar de color, umbral de distancia para cabiar de color