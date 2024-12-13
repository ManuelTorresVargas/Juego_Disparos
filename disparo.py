import pygame  # Importamos Pygame para usar sus funciones gráficas

class Disparo:
    def __init__(self, x, y, direccion, color, daño=10):
        """
        Inicializa un disparo con su posición, dirección, color, y daño.
        
        :param x: Posición inicial en el eje X del disparo.
        :param y: Posición inicial en el eje Y del disparo.
        :param direccion: Dirección del disparo (1 para derecha, -1 para izquierda).
        :param color: Color del disparo (en formato RGB).
        :param daño: Cantidad de daño que inflige el disparo (valor predeterminado 10).
        """
        self.x = x  # Posición en el eje X
        self.y = y  # Posición en el eje Y
        self.direccion = direccion  # Dirección del disparo (1 o -1)
        self.color = color  # Color del disparo
        self.velocidad = 10  # Velocidad del disparo (valor fijo)
        self.daño = daño  # Daño que el disparo causará
        self.rect = pygame.Rect(self.x, self.y, 10, 5)  # Rectángulo para representar el disparo (ancho: 10, alto: 5)

    def mover(self):
        """
        Mueve el disparo en la dirección especificada.
        """
        self.x += self.velocidad * self.direccion  # Actualiza la posición X según la dirección y velocidad
        self.rect.x = self.x  # Actualiza la posición del rectángulo asociado al disparo

    def dibujar(self, ventana):
        """
        Dibuja el disparo en la ventana del juego.
        
        :param ventana: Superficie de Pygame donde se dibuja el disparo.
        """
        pygame.draw.rect(ventana, self.color, self.rect)  # Dibuja el rectángulo con el color especificado
