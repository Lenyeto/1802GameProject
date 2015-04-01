import mymath
import xml.etree.ElementTree as ET
import math
import random
import pygame

ITEM_CONSUMABLE = 0
ITEM_EQUIPABLE = 1

EQUIP_HELM = 0
EQUIP_CHEST = 1
EQUIP_LEGS = 2
EQUIP_FOOT = 3
EQUIP_WEAPON = 4
EQUIP_OFFHAND = 5
EQUIP_TRINKET = 6

NONE = 0
CON_HEALTH = 1
CON_POWER = 2

DOWN = 1
RIGHT = 2
UP = 3
LEFT = 4

vUp = mymath.Vector2(0, -1)
vDown = mymath.Vector2(0, 1)
vRight = mymath.Vector2(1, 0)
vLeft = mymath.Vector2(-1, 0)

H1_SWORD = 0
H1_MACE = 1
H1_AXE = 2
H2_SWORD = 3
H2_MACE = 4
H2_AXE = 5
BOW = 6

NORMAL = 0
LOOT = 1
BOSS = 2
START = 3

class EntityBase(object):
    def __init__(self, name, pos, vel=mymath.Vector2(0, 0)):
        self.name = name
        self.pos = pos
        self.vel = vel
        self.acc = mymath.Vector2(0, 0)

    def ai_player(self, player):
        pass


class ItemBase(object):
    def __init__(self, name, file):
        self.name = name
        self.stats = self.get_data(self, file)

    def use(self, player):
        pass

    def get_data(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        return True #PLACE HOLDER


class Player(EntityBase):
    def __init__(self, health, pos):
        EntityBase.__init__(self, "Hero", pos)
        self.health = health
        self.equipment = {'Helmet', 'Chest', 'Legs', 'Foot', 'MainHand', 'OffHand', 'Consumable'}
        self.equipment['Trinkets'] = []
        self.aim = NONE
        self.past_list_of_keys = []

    def attack(self):
        if self.equipment['MainHand'].type == H1_SWORD:
            pass

    def update(self, dt, list_of_keys):
        self.pos += self.vel * dt
        self.control(list_of_keys, dt)

    def control(self, list_of_keys, dt):
        if pygame.K_w in list_of_keys:
            self.acc += vUp * dt
        if pygame.K_s in list_of_keys:
            self.acc += vDown * dt
        if pygame.K_d in list_of_keys:
            self.acc += vRight * dt
        if pygame.K_a in list_of_keys:
            self.acc += vLeft * dt

        if pygame.K_LEFT in list_of_keys:
            self.aim = LEFT
        if pygame.K_RIGHT in list_of_keys:
            self.aim = RIGHT
        if pygame.K_UP in list_of_keys:
            self.aim = UP
        if pygame.K_DOWN in list_of_keys:
            self.aim = DOWN

        self.past_list_of_keys = list(list_of_keys)

    def render(self, surface):
        pass


class Enemy(EntityBase):
    def __init__(self, name, health):
        self.name = name
        self.health = health


class Consumable(ItemBase):
    def __init__(self):
        pass


class Equipable(ItemBase):
    def __init__(self, name, type, file):
        ItemBase.__init__(name, file)
        self.type = type


class ItemStand(EntityBase):
    def __init__(self, item, pos, param):
        EntityBase.__init__(self, "", pos)
        if isinstance(item, Consumable):
            self.type = ITEM_CONSUMABLE
        elif isinstance(item, Equipable):
            self.type = ITEM_EQUIPABLE
        else:
            raise TypeError("This can only hold items.")

        if self.type == ITEM_CONSUMABLE:
            self.potable = param
        else:
            self.equipable = param[1]
            self.item = Equipable(param[0], param[1], param[3])

        self.cool_down = 10

    def pick_up(self, player):
        if self.type == ITEM_CONSUMABLE:
            if player.equipment['Consumable'] == NONE:
                player.equipment['Consumable'] = self.potable
                self.potable = NONE
            else:
                tmp = player.equipment['Consumable']
                player.equipment['Consumable'] = self.potable
                self.potable = tmp
        self.cool_down = 10

    def update(self, dt, players=[]):
        if self.cool_down == 0:
            for p in players:
                dist_vect = p.pos - self.pos
                dist = dist_vect.length()
                if dist < 5:
                    self.pick_up(p)
        else:
            self.cool_down -= dt
            if self.cool_down < 0:
                self.cool_down = 0


class Floor(object):
    def __init__(self, num_rooms=-1, seed=-1):
        if seed == -1:
            self.seed = random.randint(1000, 9999)
        else:
            if isinstance(seed, int) and 1000 <= seed <= 9999:
                self.seed = seed
            else:
                raise TypeError("Seed needs to be an Integer from 1000 to 9999.")

        random.seed(self.seed)

        if num_rooms == -1:
            self.num_rooms = random.randint(5, 15)

        self.left, right, up, down = False

        self.rooms = []

    def generate(self):
        self.rooms.append(Room(START, (0, 0)))
        for i in self.num_rooms:
            cur_room = self.rooms[-1]
            #Check Rooms Around The Current Room
            self.left, right, up, down = False
            for r in self.rooms:
                if r.pos[0] == cur_room.pos[0] + 1:
                    self.right = True
                if r.pos[0] == cur_room.pos[0] - 1:
                    self.left = True
                if r.pos[1] == cur_room.pos[1] + 1:
                    self.up = True
                if r.pos[1] == cur_room.pos[1] - 1:
                    self.down = True
            if self.right and self.left and self.up and self.down:
                if len(self.rooms) == self.num_rooms:
                    pass
                else:
                    break


class Room(object):
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos
        if self.type == NORMAL:
            pass
        elif self.type == LOOT:
            pass
        elif self.type == BOSS:
            pass
        elif self.type == START:
            pass




