import pygame  # Importamos la librería para manejar gráficos y eventos del juego
import sys  # Importamos para manejar la salida del sistema y cerrar el juego
from personaje import Cubo  # Importamos la clase del jugador 1
from personaje2 import Cubo2  # Importamos la clase del jugador 2
from disparo import Disparo  # Importamos la clase que maneja los disparos

# Inicializar Pygame
pygame.init()

# Configuración básica de la ventana
ANCHO = 800  # Ancho de la ventana del juego
ALTO = 600  # Alto de la ventana del juego
COLOR_FONDO = (30, 30, 30)  # Color de fondo en formato RGB (gris oscuro)

# Crear la ventana de juego
ventana = pygame.display.set_mode([ANCHO, ALTO])  # Establece las dimensiones de la ventana
pygame.display.set_caption("Juego de 2 Jugadores con Vida y Disparos")  # Título de la ventana

# Inicializar los mandos (joysticks)
pygame.joystick.init()
mandos = []  # Lista para almacenar los mandos conectados
for i in range(pygame.joystick.get_count()):
    mando = pygame.joystick.Joystick(i)  # Detecta un mando conectado
    mando.init()  # Inicializa el mando
    mandos.append(mando)  # Agrega el mando a la lista

# Verificar que hay al menos dos mandos conectados
if len(mandos) < 2:
    print("Se necesitan al menos dos mandos.")  # Mensaje si no hay suficientes mandos
    pygame.quit()  # Cierra Pygame
    sys.exit()  # Finaliza el programa

# Fuente para texto en pantalla
fuente = pygame.font.Font(None, 74)  # Fuente para mensajes grandes
fuente_pequeña = pygame.font.Font(None, 36)  # Fuente para mensajes pequeños

def mostrar_mensaje(texto, color):
    """Dibuja un mensaje en el centro de la pantalla."""
    superficie_texto = fuente.render(texto, True, color)  # Genera el texto con la fuente y color
    rect_texto = superficie_texto.get_rect(center=(ANCHO // 2, ALTO // 2))  # Centra el texto en la pantalla
    ventana.blit(superficie_texto, rect_texto)  # Dibuja el texto en la ventana

def reiniciar_juego():
    """Reinicia las variables del juego."""
    global jugador1, jugador2, disparos_jugador1, disparos_jugador2, cooldown_jugador1, cooldown_jugador2, jugando, ganador
    jugador1 = Cubo(100, 100)  # Posición inicial del jugador 1
    jugador2 = Cubo2(600, 400)  # Posición inicial del jugador 2
    disparos_jugador1 = []  # Lista vacía para los disparos del jugador 1
    disparos_jugador2 = []  # Lista vacía para los disparos del jugador 2
    cooldown_jugador1 = 0  # Tiempo de espera entre disparos para el jugador 1
    cooldown_jugador2 = 0  # Tiempo de espera entre disparos para el jugador 2
    ganador = None  # Reinicia al ganador a None

# Inicializar variables del juego
reiniciar_juego()

# Variable principal del bucle de juego
jugando = True
while jugando:
    # Procesar eventos del juego
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Detectar si se cierra la ventana
            jugando = False

        # Reiniciar el juego si hay un ganador y se presiona Enter
        if ganador and evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            reiniciar_juego()

    # Reducir cooldowns (tiempo entre disparos)
    if cooldown_jugador1 > 0:
        cooldown_jugador1 -= 1
    if cooldown_jugador2 > 0:
        cooldown_jugador2 -= 1

    # Si hay un ganador, mostrar el mensaje y esperar reinicio
    if ganador:
        ventana.fill(COLOR_FONDO)  # Pintar la pantalla con el color de fondo
        mensaje = f"{ganador} Ganador"  # Texto que muestra el ganador
        color_ganador = (0, 0, 255) if ganador == "Azul" else (255, 0, 0)  # Azul si jugador 2, Rojo si jugador 1
        mostrar_mensaje(mensaje, color_ganador)  # Llama a la función para mostrar el mensaje
        mensaje_reiniciar = "Presiona Enter para volver a jugar"  # Instrucción para reiniciar
        superficie_reiniciar = fuente_pequeña.render(mensaje_reiniciar, True, (255, 255, 255))  # Renderiza el texto
        rect_reiniciar = superficie_reiniciar.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))  # Ubicación del texto
        ventana.blit(superficie_reiniciar, rect_reiniciar)  # Dibuja el mensaje en pantalla
        pygame.display.update()  # Actualiza la pantalla
        continue  # Salta el resto del bucle mientras hay un ganador

    # Movimiento del jugador 1 con el joystick
    movimiento_jugador1 = [0, 0]
    movimiento_jugador1[0] = int(mandos[0].get_axis(0) * 3)  # Movimiento horizontal (X)
    movimiento_jugador1[1] = int(mandos[0].get_axis(1) * 3)  # Movimiento vertical (Y)
    jugador1.mover(movimiento_jugador1, ANCHO, ALTO)

    # Movimiento del jugador 2 con el joystick
    movimiento_jugador2 = [0, 0]
    movimiento_jugador2[0] = int(mandos[1].get_axis(0) * 3)  # Movimiento horizontal (X)
    movimiento_jugador2[1] = int(mandos[1].get_axis(1) * 3)  # Movimiento vertical (Y)
    jugador2.mover(movimiento_jugador2, ANCHO, ALTO)

    # Detectar disparos con el botón RT (eje 5) y aplicar cooldown
    if mandos[0].get_axis(5) > 0.5 and cooldown_jugador1 == 0:
        disparos_jugador1.append(Disparo(jugador1.rect.right, jugador1.rect.centery, 1, (255, 0, 0), daño=5))
        cooldown_jugador1 = 20  # Cooldown entre disparos

    if mandos[1].get_axis(5) > 0.5 and cooldown_jugador2 == 0:
        disparos_jugador2.append(Disparo(jugador2.rect.left, jugador2.rect.centery, -1, (0, 0, 255), daño=5))
        cooldown_jugador2 = 20

    # Mover disparos y verificar colisiones
    for disparo in disparos_jugador1[:]:
        disparo.mover()
        if disparo.rect.left > ANCHO:  # Sale de la pantalla
            disparos_jugador1.remove(disparo)
        elif disparo.rect.colliderect(jugador2.rect):  # Impacta al jugador 2
            jugador2.reducir_vida(disparo.daño)
            disparos_jugador1.remove(disparo)

    for disparo in disparos_jugador2[:]:
        disparo.mover()
        if disparo.rect.right < 0:  # Sale de la pantalla
            disparos_jugador2.remove(disparo)
        elif disparo.rect.colliderect(jugador1.rect):  # Impacta al jugador 1
            jugador1.reducir_vida(disparo.daño)
            disparos_jugador2.remove(disparo)

    # Verificar si algún jugador perdió toda la vida
    if jugador1.vida <= 0:
        ganador = "Azul"
    elif jugador2.vida <= 0:
        ganador = "Rojo"

    # Dibujar todo en pantalla
    ventana.fill(COLOR_FONDO)  # Pintar el fondo
    jugador1.dibujar(ventana)  # Dibujar jugador 1
    jugador2.dibujar(ventana)  # Dibujar jugador 2

    # Dibujar disparos en pantalla
    for disparo in disparos_jugador1:
        disparo.dibujar(ventana)
    for disparo in disparos_jugador2:
        disparo.dibujar(ventana)

    pygame.display.update()  # Actualizar la pantalla con los nuevos gráficos

# Salir del juego
pygame.quit()  # Finaliza Pygame
sys.exit()  # Salida del script
