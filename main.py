import pygame
import sys
import random
import time

pygame.init()


WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Save Water")


image = pygame.image.load('player.png')  
image = pygame.transform.scale(image, (50, 50))  

player = image.get_rect()

options_green = ["mala1.png", "mala2.png", "mala3.png"]
options_red = ["buena1.png", "buena2.png", "buena3.png"]

green_image = pygame.image.load(options_green[random.randint(0, 2)])  
red_image = pygame.image.load(options_red[random.randint(0, 2)])  

green_image = pygame.transform.scale(green_image, (70, 70))  #
red_image = pygame.transform.scale(red_image, (70, 70))  

# Velocidad de movimiento
vel = 2

# Puntos
puntos = 0

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

good_objects = []
bad_objects = []
how_objects = 10

GOOD_COLLISION = pygame.USEREVENT + 1
BAD_COLLISION = pygame.USEREVENT + 2

def create_object():
    x = random.randint(0, WIDTH - 100)  
    y = random.randint(0, HEIGHT - 100)  
    rect = pygame.Rect(x, y, 50, 50) 
    rect = pygame.Rect(x, y, 50, 50)  
    return rect

def check_collisions(good_objects, bad_objects, player):
    toRemove_good = []
    toRemove_bad = []

    for i in range(len(good_objects)):
        if good_objects[i].colliderect(player):
            toRemove_good.append(i)
    for i in range(len(bad_objects)):
        if bad_objects[i].colliderect(player):
            toRemove_bad.append(i)

    for i in reversed(toRemove_good):
        del good_objects[i]
        print(len(good_objects))
    for i in reversed(toRemove_bad):
        del bad_objects[i]

    for collision_index in toRemove_good:
        pygame.event.post(pygame.event.Event(GOOD_COLLISION, collision=collision_index))
    for collision_index in toRemove_bad:
        pygame.event.post(pygame.event.Event(BAD_COLLISION, collision=collision_index))

def create_objects():        
    x = how_objects / 10
    for _ in range(how_objects):
        obj = create_object()
        good_objects.append(obj)

    for _ in range(int(x)):
        obj = create_object()
        bad_objects.append(obj)

def resume(value):
    global how_objects
    global puntos
    if value == True:
        #print("juego ganado")
        #print(f"Nivel {how_objects / 10} completo")
        pygame.display.update()
        how_objects += 10
        puntos = 0
        create_objects()

    elif value == False:
        fuente = pygame.font.Font(None, 40)
        message_loss = fuente.render("VUELVE A INTENTARLO MÁS TARDE", 1, (255, 255, 255))
        win.blit(message_loss, (200, 300))

create_objects()
fuente = pygame.font.Font(None, 20)

mensaje = fuente.render(f"Puntos {str(puntos)}", 1, (255, 255, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == GOOD_COLLISION:
            collision_index = event.collision
            
            #print(f"Colisión con el objeto {collision_index}")
            puntos += 1
            mensaje = fuente.render(f"Puntos: {str(puntos)}", 1, (255, 255, 255))

        if event.type == BAD_COLLISION:
            collision_index = event.collision
            #print(f"Colisión con el objeto {collision_index}")
            puntos += -1
            mensaje = fuente.render(f"Puntos: {str(puntos)}", 1, (255, 255, 255))

    check_collisions(good_objects, bad_objects, player)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= vel
    if keys[pygame.K_RIGHT]:
        player.x += vel
    if keys[pygame.K_UP]:
        player.y -= vel
    if keys[pygame.K_DOWN]:
        player.y += vel

    win.fill((0, 0, 0))

    if puntos < how_objects and len(good_objects) == 0:
        #print("goood objects len: " + str(len(good_objects)))
        #print("cant.objectos: " + str(how_objects))
        #print("cant. puntos: " + str(puntos))
        mensaje = fuente.render(f"Puntos: {str(puntos)}", 1, (255, 255, 255))
        mensaje = fuente.render("", 1, (255, 255, 255))
        resume(False)

    elif puntos == how_objects and len(good_objects) == 0:
        #print("good_objets len: " + str(len(good_objects)))
        #print("cant.objetos: " + str(how_objects))
        #print("cant. puntos: " + str(puntos))
        mensaje = fuente.render(f"Puntos: {str(puntos)}", 1, (255, 255, 255))
        x = how_objects / 10
        fuente2 = pygame.font.Font(None, 30)
        mensaje = fuente2.render(f"NIVEL {x} COMPLETADO", 1, (255, 255, 255))
        resume(True)

    win.blit(image, player)

    for obj in good_objects:
        win.blit(green_image, obj.topleft)

    for obj in bad_objects:
        win.blit(red_image, obj.topleft)

    win.blit(mensaje, (15, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
