import pygame  # Importamos Pygame para trabajar con gráficos y rectángulos

class Cubo2:
    def __init__(self, x, y):
        """
        Inicializa un cubo que representa al segundo jugador.
        
        :param x: Posición inicial en el eje X.
        :param y: Posición inicial en el eje Y.
        """
        self.x = x  # Posición en el eje X
        self.y = y  # Posición en el eje Y
        self.ancho = 50  # Ancho del cubo
        self.alto = 50  # Alto del cubo
        self.velosidad = 3  # Velocidad del cubo (puede ajustarse)
        self.color = (0, 0, 255)  # Color azul del cubo
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)  # Rectángulo que representa al cubo
        self.vida = 100  # Vida inicial del cubo

    def dibujar(self, ventana):
        """
        Dibuja el cubo y su barra de vida en la pantalla.
        
        :param ventana: Superficie de Pygame donde se dibuja el cubo.
        """
        pygame.draw.rect(ventana, self.color, self.rect)  # Dibuja el rectángulo del cubo

        # Dibuja la barra de vida encima del cubo
        largo_barra = 50  # Longitud de la barra de vida
        alto_barra = 5  # Altura de la barra de vida
        porcentaje_vida = max(0, self.vida) / 100  # Calcula el porcentaje de vida restante
        # Cambia el color de la barra según el nivel de vida
        barra_color = (0, 255, 0) if self.vida > 50 else (255, 165, 0) if self.vida > 25 else (255, 0, 0)
        # Dibuja la barra de vida llena
        pygame.draw.rect(ventana, barra_color, (self.x, self.y - 10, largo_barra * porcentaje_vida, alto_barra))
        # Dibuja el contorno de la barra de vida
        pygame.draw.rect(ventana, (255, 255, 255), (self.x, self.y - 10, largo_barra, alto_barra), 1)

    def mover(self, movimiento, ancho_pantalla, alto_pantalla):
        """
        Mueve el cubo dentro de los límites de la pantalla.
        
        :param movimiento: Lista [movimiento_x, movimiento_y] con los desplazamientos en cada eje.
        :param ancho_pantalla: Ancho de la pantalla para limitar movimientos.
        :param alto_pantalla: Alto de la pantalla para limitar movimientos.
        """
        # Actualiza la posición según el movimiento
        self.x += movimiento[0]
        self.y += movimiento[1]

        # Limita el movimiento del jugador 2 para que no cruce al lado izquierdo
        if self.x < ancho_pantalla // 2:  # Límite izquierdo para el jugador 2
            self.x = ancho_pantalla // 2
        if self.x + self.ancho > ancho_pantalla:  # Límite derecho
            self.x = ancho_pantalla - self.ancho
        if self.y < 0:  # Límite superior
            self.y = 0
        if self.y + self.alto > alto_pantalla:  # Límite inferior
            self.y = alto_pantalla - self.alto

        # Actualiza la posición del rectángulo asociado
        self.rect.x = self.x
        self.rect.y = self.y

    def reducir_vida(self, cantidad):
        """
        Reduce la vida del cubo.
        
        :param cantidad: Cantidad de vida a reducir.
        """
        self.vida -= cantidad  # Reduce la vida en la cantidad especificada
