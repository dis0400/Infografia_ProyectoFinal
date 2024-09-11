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

    def setup(self):
        # Crear boids al iniciar
        self.boids = [Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(50)]

    def on_draw(self):
        # Renderizar la pantalla
        arcade.start_render()
        for boid in self.boids:
            boid.draw()

    def update(self, delta_time):
        # Actualizar cada boid y aplicar las reglas
        for boid in self.boids:
            boid.edges(SCREEN_WIDTH, SCREEN_HEIGHT)
            boid.apply_behaviors(self.boids)
            boid.update()

# Ejecutar el simulador
if __name__ == "__main__":
    window = FlockingSimulation(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
