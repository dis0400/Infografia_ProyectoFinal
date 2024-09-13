import arcade
import random
from boid import Boid

# Configuramos la ventana de Arcade
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Simulador de Boids con Arcade"

class FlockingSimulation(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.boids = []
        self.obstacles = []  # Lista para almacenar los obstáculos
        self.current_shape = "circle"  # Inicialmente los obstáculos serán círculos


    def setup(self):
        # Crear boids al iniciar
        self.boids = [Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(50)]
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.C:
            self.current_shape = "circle"
        elif key == arcade.key.S:
            self.current_shape = "square"

    def on_draw(self):
        # Renderizar la pantalla
        arcade.start_render()
        for boid in self.boids:
            boid.draw()
        # Dibujar los obstáculos
        for obstacle in self.obstacles:
            arcade.draw_circle_filled(obstacle[0], obstacle[1], 10, arcade.color.RED)  # Ajuste del tamaño del obstáculo
            for obstacle in self.obstacles:
                if obstacle[2] == "circle":
                    arcade.draw_circle_filled(obstacle[0], obstacle[1], 10, arcade.color.RED)
                elif obstacle[2] == "square":
                    arcade.draw_rectangle_filled(obstacle[0], obstacle[1], 20, 20, arcade.color.RED)


    def on_mouse_press(self, x, y, button, modifiers):
        # Crear un obstáculo en la posición del clic
        self.obstacles.append((x, y,  self.current_shape))


    def update(self, delta_time):
        # Actualizar cada boid y aplicar las reglas
        for boid in self.boids:
            boid.edges(SCREEN_WIDTH, SCREEN_HEIGHT)
            boid.apply_behaviors(self.boids, self.obstacles)  # Pasar los obstáculos a los boids
            boid.update()
            


# Ejecutar el simulador
if __name__ == "__main__":
    window = FlockingSimulation(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
