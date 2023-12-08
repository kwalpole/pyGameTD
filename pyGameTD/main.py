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
game_over = False
game_outcome = 0 # -1 is a loss, 1 is a win
level_started = False
placing_troops = False
selected_trooper = False
last_enemy_spawn = pg.time.get_ticks()

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
begin_image = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
fast_forward_image = pg.image.load('assets/images/buttons/fast_forward.png').convert_alpha()


#load fonts for showing text
text_font = pg.font.SysFont("Cambria", 24, bold = True)
large_font = pg.font.SysFont("Cambria", 36)

#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_data():
    #draw panel
    pg.draw.rect(screen, "royalblue", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    pg.draw.rect(screen, "black", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 2)
    draw_text("HEALTH: " + str(world.health), text_font, "darkred", 0, 0)
    draw_text("CREDITS: " + str(world.money), text_font, "gold", 0, 30)
    draw_text("WAVE: " + str(world.level), text_font, "black", 0, 60)

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
            #deduct cost of turret
            world.money -= c.BUY_COST

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
world.process_enemies()

#create groups
enemy_group = pg.sprite.Group()
trooper_group = pg.sprite.Group()

#create buttons
trooper_button = Button(c.SCREEN_WIDTH + 75, 120, deploy_trooper_image, True)
cancel_button = Button(c.SCREEN_WIDTH+ 75, 180, cancel_image, True)
promote_trooper_button = Button(c.SCREEN_WIDTH+ 75, 180, promote_trooper_image, True)
begin_button = Button(c.SCREEN_WIDTH+ 75, 300, begin_image, True)
restart_button = Button(660, 360, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH+ 75, 300, fast_forward_image, False)

#game loop
running = True
while running:

    clock.tick(c.FPS)

    # UPDATES ###########################

    if game_over == False:
        #check if player has lost
        if world.health <= 0:
            game_over = True
            game_outcome = -1
        #check if player has won
        if world.level > c.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1

        # update groups
        enemy_group.update(world)
        trooper_group.update(enemy_group, world)

        #highlight trooper
        if selected_trooper:
            selected_trooper.selected = True

    # DRAW #############################

    #draw level
    world.draw(screen)

    #draw groups
    enemy_group.draw(screen)
    for trooper in trooper_group:
        trooper.draw(screen)

    display_data()

    if game_over == False:
        #check if level has started
        if level_started == False:
            if begin_button.draw(screen):
                level_started = True
        else:
            #fast forward option
            world.game_speed = 1
            if fast_forward_button.draw(screen):
                world.game_speed = 2
            #spawn enemies
            if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_level = int(world.enemy_list[world.spawned_enemies])
                    enemy = Enemy(world.waypoints, enemy_images, enemy_level)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()

        #check if level is over
        if world.check_level_complete() == True:
            world.money += c.LEVEL_COMPLETE_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemies()

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
            #display cost of placing trooper
            draw_text("COST: " + str(c.BUY_COST), large_font, "gold", c.SCREEN_WIDTH+ 75, 60)
            if cursor_pos[0]<= c.SCREEN_WIDTH:
                screen.blit(cursor_icon, cursor_rect)
            if cancel_button.draw(screen):
                placing_troops = False
        #if trooper is selected show promote button
        if selected_trooper:
            #show upgrade cost
            draw_text("COST: " + str(c.UPGRADE_COST), large_font, "gold", c.SCREEN_WIDTH + 75, 60)
            #if trooper can be upgraded then show the upgrade button
            if selected_trooper.upgrade_level < c.TROOPER_LEVELS:
                if promote_trooper_button.draw(screen):
                    if world.money >= c.UPGRADE_COST:
                        selected_trooper.upgrade()
                        world.money -= c.UPGRADE_COST
    else:
        if game_outcome == -1:
            pg.draw.rect(screen, "firebrick", (530, 250, 400, 200), border_radius=30)
            draw_text("GAME OVER", large_font, "black", 640, 300)
        elif game_outcome == 1:
            pg.draw.rect(screen, "steelblue", (530, 250, 400, 200), border_radius=30)
            draw_text("YOU WON!", large_font, "black", 645, 300)
        #restart level
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            placing_troops = False
            selected_trooper = None
            last_enemy_spawn = pg.time.get_ticks()
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemies()
            #empty groups
            enemy_group.empty()
            trooper_group.empty()

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
                    #check if they got enough dough for a trooper
                    if world.money >= c.BUY_COST:
                        create_trooper(mouse_pos)
                else:
                    selected_trooper = select_trooper(mouse_pos)
    #update display
    pg.display.flip()

pg.QUIT