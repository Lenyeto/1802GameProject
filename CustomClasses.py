import mymath
import xml.etree.ElementTree as ET

ITEM_CONSUMABLE = 0
ITEM_EQUIPABLE = 1

NONE = 0

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
            pass

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