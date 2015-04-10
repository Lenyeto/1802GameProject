import random
import pygame
from mymath import *
from EntitiyClasses import *
import xmlweapons



DEBUG = -1




class Floor(object):
    pass


class Room(object):
    def __init__(self, type, piece="NONE"):
        self.entities = []

    def generate_room(self, surface, type=DEBUG):
        self.create_walls(surface, type)
        self.generate_entities(surface, type)

    def create_walls(self, surface, type=DEBUG):
        for i in range(int(surface.get_width()/32)):
            for k in range(int(surface.get_height()/32)):
                if type == DEBUG:
                    path = "Assets/Graphics/Room/"
                if i == 0 and k == 0:
                    self.entities.append(Wall_Floor("Wall", Vector2(0, 0), path+"NorthWestWall.png"))
                elif i == surface.get_width()/32 - 1 and k == surface.get_height()/32 - 1:
                    self.entities.append(Wall_Floor("Wall", Vector2(surface.get_width() - 32, surface.get_height() - 32), path+"SouthEastWall.png"))
                elif 0 < i < surface.get_width()/32 - 1 and 0 < k < surface.get_height()/32 - 1:
                    self.entities.append(Wall_Floor("Floor", Vector2(i * 32, k * 32), path+"StoneFloor1.png", False))
                elif k == surface.get_height()/32 - 1 and i == 0:
                    self.entities.append(Wall_Floor("Wall", Vector2(i * 32, k * 32), path+"SouthWestWall.png"))
                elif i == surface.get_width()/32 - 1 and k == 0:
                    self.entities.append(Wall_Floor("Wall", Vector2(i * 32, k * 32), path+"NorthEastWall.png"))
                else:
                    if i == 0 and not k == 0 and not k == surface.get_height()/32 - 1:
                        self.entities.append(Wall_Floor("Wall", Vector2(i * 32, k * 32), path+"WestWall.png"))
                    if not i == 0 and k == 0 and not i == surface.get_width()/32 - 1:
                        self.entities.append(Wall_Floor("Wall", Vector2(i * 32, k * 32), path+"NorthWall.png"))
                    if i == surface.get_width()/32 -1 and not k == 0 and not k == surface.get_height()/32 -1:
                        self.entities.append(Wall_Floor("Wall", Vector2(i * 32, k * 32), path+"EastWall.png"))
                    if k == surface.get_height()/32 -1 and not i == 0 and not i == surface.get_width()/32 - 1:
                        self.entities.append(Wall_Floor("Wall", Vector2(i * 32, k * 32), path+"SouthWall.png"))

    def generate_entities(self, surface, type):
        self.entities.append(Dummy(mymath.Vector2(200, 200)))
        self.entities.append(WeaponStand(xmlweapons.Weapon().getWeapon("Short Bow"), mymath.Vector2(50, 50)))

    def render(self, surface):
        for e in self.entities:
            e.render(surface)