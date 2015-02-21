import mymath
import xml.etree.ElementTree as ET
import math
import random

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

class EntityBase(object):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

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
    def __init__(self, health):
        self.name = "Hero"
        self.health = health
        self.equipment = {'Helmet', 'Chest', 'Legs', 'Foot', 'MainHand', 'OffHand', 'Consumable'}
        self.equipment['Trinkets'] = []

    def update(self):
        pass

    def render(self):
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
    def __init__(self, seed=-1):
        if seed == -1:
            self.seed = random.randint(1000, 9999)
        else:
            if isinstance(seed, int) and 1000 <= seed <= 9999:
                self.seed = seed
            else:
                raise TypeError("Seed needs to be an Integer from 1000 to 9999.")

    def generate(self):
        pass

class  Room(object):
    def __init__(self):
        pass

