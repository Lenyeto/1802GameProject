import random
import pygame
from mymath import *
from EntitiyClasses import *
import xmlweapons



DEBUG = -1




class Floor(object):
    def __init__(self, surface, type=DEBUG):
        self.rooms = []
        self.type = type
        self.num_rooms = random.randint(6, 16)
        self.generate_floor()
        self.cur_room = self.rooms[0]
        self.cur_room.generate_room(surface)
        self.create_doors()


    def generate_floor(self):
        self.rooms.append(Room(self.type, Vector2(0, 0)))
        for i in range(self.num_rooms):
            cur_room = self.rooms[-1]
            ಠ_ಠ = random.randint(0, 3)
            if len(self.rooms) < self.num_rooms:# - 3:
                if ಠ_ಠ == 0:
                    if not self.check_if_full(Vector2(cur_room.position.x + 1, cur_room.position.y)):
                        self.rooms.append(Room(self.type, Vector2(cur_room.position.x + 1, cur_room.position.y)))
                elif ಠ_ಠ == 1:
                    if not self.check_if_full(Vector2(cur_room.position.x, cur_room.position.y + 1)):
                        self.rooms.append(Room(self.type, Vector2(cur_room.position.x, cur_room.position.y + 1)))
                elif ಠ_ಠ == 2:
                    if not self.check_if_full(Vector2(cur_room.position.x - 1, cur_room.position.y)):
                        self.rooms.append(Room(self.type, Vector2(cur_room.position.x - 1, cur_room.position.y)))
                else:
                    if not self.check_if_full(Vector2(cur_room.position.x, cur_room.position.y - 1)):
                        self.rooms.append(Room(self.type, Vector2(cur_room.position.x, cur_room.position.y - 1)))
            #elif len(self.rooms) < self.num_rooms - 1:
            #    # Creates Item Rooms
            #    pass
            #elif len(self.rooms) < self.num_rooms:
            #    # Creates Boss Room
            #    pass

    def update(self, list_of_players, surface):
        move = self.cur_room.update(list_of_players)
        if not move == Vector2(0, 0):
            bool, room = self.check_if_full(self.cur_room.position + move)
            if bool:
                self.cur_room = room
                self.cur_room.generate_room(surface)

    def create_doors(self):
        for i in self.rooms:
            if self.check_if_full(Vector2(i.position.x + 1, i.position.y)):
                i.doors[0] = True
            if self.check_if_full(Vector2(i.position.x, i.position.y + 1)):
                i.doors[1] = True
            if self.check_if_full(Vector2(i.position.x - 1, i.position.y)):
                i.doors[2] = True
            if self.check_if_full(Vector2(i.position.x, i.position.y - 1)):
                i.doors[3] = True

    def check_if_full(self, pos=Vector2(0, 0)):
        for i in self.rooms:
            if i.position == pos:
                return True, i
        return False, NONE

class Room(object):
    def __init__(self, type, position=Vector2(0, 0)):
        self.entities = []
        self.can_leave = False
        self.position = position
        self.doors = [False, False, False, False]

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

    def update(self, list_of_players):
        if not self.can_leave:
            num_of_enemies = 0
            for i in self.entities:
                if i.name == "ENEMY":
                    num_of_enemies += 1
            if num_of_enemies > 0:
                self.can_leave = False
            else:
                self.can_leave = True
        else:
            for i in list_of_players:
                if i.pos.x < 32 and self.doors[2]:
                    return Vector2(-1, 0)
                if i.pos.x > 608 and self.doors[0]:
                    return Vector2(1, 0)
                if i.pos.y < 32 and self.doors[1]:
                    return Vector2(0, -1)
                if i.pos.y > 608 and self.doors[3]:
                    return Vector2(0, 1)
            return Vector2(0, 0)
        return Vector2(0, 0)
