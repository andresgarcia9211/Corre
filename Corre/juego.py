import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configuración de la ventana
SCREEN_ancho = 800
SCREEN_largo = 600
screen = pygame.display.set_mode((SCREEN_ancho, SCREEN_largo))
pygame.display.set_caption('Corre!!!')

# Fuente para el texto
font = pygame.font.SysFont(None, 40)


# Clase para el jugador
class Jugador:
    def __init__(self):
        self._color = None
        self._ancho = None
        self._largo = None
        self._x = None
        self._y = None
        self._velocidad = None

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def ancho(self):
        return self._ancho

    @ancho.setter
    def ancho(self, ancho):
        self._ancho = ancho

    @property
    def largo(self):
        return self._largo

    @largo.setter
    def largo(self, largo):
        self._largo = largo

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def velocidad(self):
        return self._velocidad

    @velocidad.setter
    def velocidad(self, velocidad):
        self._velocidad = velocidad

    def mover(self, keys):
        """Mueve el personaje en función de las teclas presionadas."""
        if keys[pygame.K_LEFT]:
            self.x -= self.velocidad  # moverr a la izquierda
        if keys[pygame.K_RIGHT]:
            self.x += self.velocidad  # moverr a la derecha
        if keys[pygame.K_UP]:
            self.y -= self.velocidad  # moverr hacia arriba
        if keys[pygame.K_DOWN]:
            self.y += self.velocidad  # moverr hacia abajo

        # Evitar que el jugador salga de la pantalla
        self.x = max(0, min(self.x, SCREEN_ancho - self.ancho))
        self.y = max(0, min(self.y, SCREEN_largo - self.largo))

    def dibujar(self, screen):
        """Dibuja el personaje en la pantalla."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.ancho, self.largo))


# Clase para los enemigos
class Enemigo(Jugador):
    def __init__(self):
        super().__init__()

    def mover(self, jugador):
        """Los enemigos se mueven hacia el jugador."""

        if self.x < jugador.x:
            self.x += self.velocidad
        elif self.x > jugador.x:
            self.x -= self.velocidad

        if self.y < jugador.y:
            self.y += self.velocidad
        elif self.y > jugador.y:
            self.y -= self.velocidad

    def dibujar(self, screen):
        """Dibuja el enemigo en la pantalla."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.ancho, self.largo))


# Función para mostrar texto en pantalla
def dibujar_text(text, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# Función para el menú principal
def menu_principal():
    """Muestra el menú principal y permite al jugador elegir una opción."""
    while True:
        screen.fill(BLACK)
        dibujar_text("Corre!!!", BLUE, SCREEN_ancho // 4, SCREEN_largo // 4 - 50)
        dibujar_text("Presiona 'S' para Jugar", WHITE, SCREEN_ancho // 4, SCREEN_largo // 4 + 50)
        dibujar_text("Presiona 'Q' para Salir", WHITE, SCREEN_ancho // 4, SCREEN_largo // 4 + 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            jugar()
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()


# Función principal del juego
def jugar():
    """Inicia el juego principal donde el jugador se mueve y enfrenta enemigos."""
    jugador = Jugador()
    jugador.color = GREEN
    jugador.ancho = 50
    jugador.largo = 50
    jugador.x = SCREEN_ancho // 2
    jugador.y = SCREEN_largo // 2
    jugador.velocidad = 5
    enemigos = []
    for _ in range(5):
        enemigo = Enemigo()
        enemigo.color = RED
        enemigo.ancho = 40
        enemigo.largo = 40
        enemigo.x = random.randint(0, SCREEN_ancho - 40)
        enemigo.y = random.randint(0, SCREEN_largo - 40)
        enemigo.velocidad = 2
        enemigos.append(enemigo)


    while True:
        screen.fill(BLACK)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # moverr al jugador
        keys = pygame.key.get_pressed()
        jugador.mover(keys)

        # moverr a los enemigos
        for enemigo in enemigos:
            enemigo.mover(jugador)

        # Verificar colisiones
        for enemigo in enemigos:
            if pygame.Rect(jugador.x, jugador.y, jugador.ancho, jugador.largo).colliderect(
                    pygame.Rect(enemigo.x, enemigo.y, enemigo.ancho, enemigo.largo)):
                dibujar_text("¡Has sido alcanzado!", RED, SCREEN_ancho // 3, SCREEN_largo // 2)
                pygame.display.flip()
                pygame.time.delay(1000)
                menu_principal()

        # Dibujar elementos en la pantalla
        jugador.dibujar(screen)
        for enemigo in enemigos:
            enemigo.dibujar(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)


# Ejecutar el juego
if __name__ == "__main__":
    menu_principal()
