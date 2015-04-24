import random
import pygame
from mymath import *
from EntityClasses import *
import equipment



DEBUG = -1




class Floor(object):
    def __init__(self, surface, type=DEBUG):
        self.rooms = []
        self.type = type
        self.num_rooms = random.randint(6, 16)
        self.generate_floor()
        self.cur_room = self.rooms[0]
        self.create_doors()
        self.cur_room.generate_room(surface)



    def generate_floor(self):
        self.rooms.append(Room(self.type, Vector2(0, 0)))
        i = 0
        while i < self.num_rooms:
            cur_room = self.rooms[-1]
            rnd = random.randint(0, 3)
            if len(self.rooms) <= self.num_rooms:# - 3:
                print(len(self.rooms))
                if rnd == 0:
                    if self.check_if_full(Vector2(cur_room.position.x + 1, cur_room.position.y)) == False:
                        self.rooms.append(Room(self.type, Vector2(cur_room.position.x + 1, cur_room.position.y)))
                        i += 1
                elif rnd == 1:
                    if not self.check_if_full(Vector2(cur_room.position.x, cur_room.position.y + 1)):
                        self.rooms.append(Room(self.type, Vector2(cur_room.position.x, cur_room.position.y + 1)))
                        i += 1
                elif rnd == 2:
                    if not self.check_if_full(Vector2(cur_room.position.x - 1, cur_room.position.y)):
                        self.rooms.append(Room(self.type, Vector2(cur_room.position.x - 1, cur_room.position.y)))
                        i += 1
                else:
                    if not self.check_if_full(Vector2(cur_room.position.x, cur_room.position.y - 1)):
                        self.rooms.append(Room(self.type, Vector2(cur_room.position.x, cur_room.position.y - 1)))
                        i += 1
            #elif len(self.rooms) < self.num_rooms - 1:
            #    # Creates Item Rooms
            #    pass
            #elif len(self.rooms) < self.num_rooms:
            #    # Creates Boss Room
            #    pass

    def update(self, list_of_players, surface):
        move = self.cur_room.update(list_of_players)
        if not move == Vector2(0, 0):
            bool = self.check_if_full(self.cur_room.position + move)
            if bool:
                self.cur_room.entities = list()
                self.cur_room = self.get_room_at(self.cur_room.position + move)
                self.cur_room.generate_room(surface)
                for i in list_of_players:
                    if move == Vector2(-1, 0):
                        i.pos = Vector2(550, 320)
                    elif move == Vector2(0, 1):
                        i.pos = Vector2(320, 550)
                    elif move == Vector2(1, 0):
                        i.pos = Vector2(90, 320)
                    elif move == Vector2(0, -1):
                        i.pos = Vector2(320, 90)

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

    def check_if_full(self, pos):
        for i in self.rooms:
            if i.position == pos:
                return True
        return False

    def get_room_at(self, pos=Vector2(0, 0)):
        for i in self.rooms:
            if i.position == pos:
                return i


class Room(object):
    def __init__(self, type, position=Vector2(0, 0)):
        self.entities = []
        self.can_leave = False
        self.position = position
        self.doors = [False, False, False, False]
        self.door_pos = [Vector2(0, 0), Vector2(0, 0), Vector2(0,0), Vector2(0, 0)]
        self.empty = False

    def generate_room(self, surface, type=DEBUG):
        self.create_walls(surface, type)
        self.generate_entities(surface, type)

    def regenerate_room(self, surface, type=DEBUG):
        self.create_walls(surface, type)


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
        if self.doors[0]:
            self.entities.append(Wall_Floor("Door", Vector2(surface.get_width() - 32, surface.get_height()/2 - 16), path + "EastDoor.png"))
            self.door_pos[0] = Vector2(surface.get_width() - 16, surface.get_height()/2 - 16)
        if self.doors[1]:
            self.entities.append(Wall_Floor("Door", Vector2(surface.get_width()/2 - 16, 0), path + "NorthDoor.png"))
            self.door_pos[1] = Vector2(surface.get_width()/2 - 16, 16)
        if self.doors[2]:
            self.entities.append(Wall_Floor("Door", Vector2(0, surface.get_height()/2 - 16), path + "WestDoor.png"))
            self.door_pos[2] = Vector2(16, surface.get_height()/2 - 16)
        if self.doors[3]:
            self.entities.append(Wall_Floor("Door", Vector2(surface.get_width()/2 - 16, surface.get_height() - 32), path + "SouthDoor.png"))
            self.door_pos[3] = Vector2(surface.get_width()/2 - 16, surface.get_height() - 16)

    def generate_entities(self, surface, type):
        self.entities.append(Dummy(mymath.Vector2(200, 200)))
        self.entities.append(WeaponStand(equipment.Equipment().equipPrimary("Short Bow"), mymath.Vector2(50, 50)))

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
                for j in range(len(self.door_pos)):
                    tmp = i.pos - self.door_pos[j]
                    dist = tmp.Dot(tmp)
                    if self.doors[j] and dist < 48 ** 2:
                        if j == 2:
                            return Vector2(-1, 0)
                        elif j == 0:
                            return Vector2(1, 0)
                        elif j == 1:
                            return Vector2(0, 1)
                        elif j == 3:
                            return Vector2(0, -1)
            return Vector2(0, 0)
        return Vector2(0, 0)
