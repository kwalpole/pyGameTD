#enemy class
import pygame as pg
from pygame.math import Vector2
from enemy_data import ENEMY_DATA
import constants as c
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, images, enemy_level):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.enemy_level = enemy_level
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA[self.enemy_level - 1].get("health")
        self.speed = ENEMY_DATA[self.enemy_level - 1].get("speed")
        self.angle = 0
        self.original_image = images[self.enemy_level - 1]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        #define target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            #enemy reached end of path
            self.kill()
            world.health -= 1
            world.missed_enemies += 1

        #distance to target calculations
        dist = self.movement.length()
        #check if distance is > speed
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1


    def rotate(self):
        #calc distance to next waypoint
        dist = self.target - self.pos
        #use dist to calc angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        #rotate image, update rect
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <=0:
            world.killed_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()

