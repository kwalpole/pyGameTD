#Keegan Walpole
#Tower Defence Game

#imports
import pygame as pg
import json
from enemy import Enemy
from world import World
from trooper import Trooper
from button import Button
import constants as c


#initialize
pg.init()

#clock
clock = pg.time.Clock()

#game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("PyGame TD")

#game variables
placing_troops = False
selected_trooper = False

#load images
#map
map_image = pg.image.load("levels/level.png").convert_alpha()
#trooper spritesheets
trooper_spritesheets = []
for x in range(1, c.TROOPER_LEVELS + 1):
    trooper_sheet = pg.image.load(f'assets/images/troopers/trooper_{x}.png').convert_alpha()
    trooper_spritesheets.append(trooper_sheet)
#individual trooper image for cursor
cursor_trooper = pg.image.load('assets/images/troopers/trooper_solid.png').convert_alpha()
cursor_icon = pg.image.load('assets/images/troopers/cursor_trooper.png').convert_alpha()
#enemies
enemy_images = []
for x in range(1, c.ENEMY_LEVELS +1):
    enemy_image = pg.image.load(f'assets/images/enemy/enemy_{x}.png').convert_alpha()
    enemy_images.append(enemy_image)
#buttons
deploy_trooper_image = pg.image.load('assets/images/buttons/deploy_trooper.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
promote_trooper_image = pg.image.load('assets/images/buttons/promote_trooper.png').convert_alpha()

def create_trooper(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    #calculate sequential number of the tile
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    #check if tile is grass
    if world.tile_map[mouse_tile_num] == 1:
        #check that theres not another trooper there
        spaceFree = True
        for trooper in trooper_group:
            if (mouse_tile_x, mouse_tile_y) == (trooper.tile_x, trooper.tile_y):
                spaceFree = False
        if spaceFree == True:
            newTrooper = Trooper(trooper_spritesheets, mouse_tile_x, mouse_tile_y)
            trooper_group.add(newTrooper)

def select_trooper(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for trooper in trooper_group:
        if (mouse_tile_x, mouse_tile_y) == (trooper.tile_x, trooper.tile_y):
            return trooper

def clear_selection():
    for trooper in trooper_group:
        trooper.selected = False

#load json data for level
with open('levels/level.tmj') as file:
    world_data = json.load(file)


#create world
world = World(world_data, map_image)
world.process_data()

#create groups
enemy_group = pg.sprite.Group()
trooper_group = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

#create buttons
trooper_button = Button(c.SCREEN_WIDTH + 75, 120, deploy_trooper_image, True)
cancel_button = Button(c.SCREEN_WIDTH+ 75, 180, cancel_image, True)
promote_trooper_button = Button(c.SCREEN_WIDTH+ 75, 240, promote_trooper_image, True)

#game loop
running = True
while running:

    clock.tick(c.FPS)

    # UPDATES ###########################
    # update groups
    enemy_group.update()
    trooper_group.update(enemy_group)

    #highlight trooper
    if selected_trooper:
        selected_trooper.selected = True

    # DRAW #############################

    screen.fill("gray")

    #draw level
    world.draw(screen)

    #draw groups
    enemy_group.draw(screen)
    for trooper in trooper_group:
        trooper.draw(screen)

    #draw buttons
    #button for placing troops
    if trooper_button.draw(screen):
        placing_troops = True
    #if placing turrets, show cancel button
    if placing_troops == True:
        #change cursor image
        cursor_rect = cursor_icon.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0]<= c.SCREEN_WIDTH:
            screen.blit(cursor_icon, cursor_rect)

        if cancel_button.draw(screen):
            placing_troops = False
    #if trooper is selected show promote button
    if selected_trooper:
        #if trooper can be upgraded then show the upgrade button
        if selected_trooper.upgrade_level < c.TROOPER_LEVELS:
            if promote_trooper_button.draw(screen):
                selected_trooper.upgrade()

    #event handler
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #check if mouse is on level
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                #clear selected troopers
                selected_trooper = None
                clear_selection()
                if placing_troops == True:
                    create_trooper(mouse_pos)
                else:
                    selected_trooper = select_trooper(mouse_pos)
    #update display
    pg.display.flip()

pg.QUIT