# Proyecto final Infografía
Este proyecto fue desarrollado por la estudiante de Ingeniería de Sistemas Computacionales, Alexia Marin.

Este proyecto presenta una **Simulación de Boids con Arcade** que utiliza el algoritmo de Flocking. El simulador implementa los tres principios básicos del algoritmo: separación, alineación y cohesión, y permite visualizar cómo los boids interactúan en un espacio definido. Además, el simulador incluye obstáculos con los que los boids pueden interactuar.

## Requisitos Previos

- Python 3.x instalado.
- Instalar las dependencias necesarias (Arcade) utilizando pip.

## Instalación

1. Clona el repositorio desde GitHub:

   ```
   git clone https://github.com/tu_usuario/tu_repositorio.git
   ```

2. Cambia al directorio del proyecto:
  ```
  cd tu_repositorio
  ```
3. Instala las dependencias necesarias:

  ```
  pip install arcade
  ```
# Uso
Inicia el simulador ejecutando 
```
python main.py
```
Para **interactuar** con la simulaci[on utiliza las siguientes teclas:
- Tecla 1: Los boids se mueven lentamente.
- Tecla 2: Los boids se mueven a velocidad normal.
- Tecla 3: Los boids se mueven rápidamente.
- Tecla 4: Pausa la simulación.
- Tecla C: Añadir un obstáculo circular.
- Tecla S: Añadir un obstáculo cuadrado.
- Tecla T: Añadir un obstáculo triangular.
- Tecla J: Los boids se agrupan solo siguiendo la regla de cohesión.
- Tecla L: Los boids se alinean únicamente.
- Tecla I: Los boids siguen solo la regla de separación.
- Tecla N: Los boids vuelven a comportarse normalmente.

# Estructura del proyecto
```
📦Simulador_Boids
 ┣ 📜README.md
 ┣ 📜main.py
 ┗ 📜boid.py
```
