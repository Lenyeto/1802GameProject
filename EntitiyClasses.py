import mymath
import xml.etree.ElementTree as ET
import pygame

ITEM_CONSUMABLE = 0
ITEM_EQUIPABLE = 1

EQUIP_HELM = 0
EQUIP_CHEST = 1
EQUIP_LEGS = 2
EQUIP_FOOT = 3
EQUIP_WEAPON = 4
EQUIP_OFFHAND = 5
EQUIP_CONSUMABLE = 6
EQUIP_TRINKET = 7

NONE = 0
CON_HEALTH = 1
CON_POWER = 2

DOWN = mymath.Vector2(0, 1)
UP = mymath.Vector2(0, -1)
RIGHT = mymath.Vector2(1, 0)
LEFT = mymath.Vector2(-1, 0)


class EntityBase(object):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def ai_player(self, player):
        pass


class Player(EntityBase):
    def __init__(self, pos=mymath.Vector2(0, 0), health=100, debug=False):
        self.pos = pos
        self.name = "Hero"
        self.health = health
        self.speed = 0.4
        self.equipment = [-1, -1, -1, -1, -1, -1, [], []]
        #self.equipment = {'Helmet', 'Chest', 'Legs', 'Foot', 'MainHand', 'OffHand', 'Consumable', 'Trinkets'}
        #self.equipment['Trinkets'] = []
        self.direction = DOWN
        self.invincibility_period = 0
        self.attack_delay = 1000
        self.cur_delay = 0

        self.tmp_key_list = []

        if debug:
            self.equipment[EQUIP_WEAPON] = "Sword"


    def update(self, dt, list_of_keys, list_of_entities):
        if self.cur_delay > 0:
            self.cur_delay -= dt
        if self.cur_delay < 0:
            self.cur_delay = 0

        if pygame.K_UP in list_of_keys:
            self.direction = UP
            if not pygame.K_UP in self.tmp_key_list:
                self.tmp_key_list.append(pygame.K_UP)
        if pygame.K_DOWN in list_of_keys:
            self.direction = DOWN
            if not pygame.K_DOWN in self.tmp_key_list:
                self.tmp_key_list.append(pygame.K_DOWN)
        if pygame.K_LEFT in list_of_keys:
            self.direction = LEFT
            if not pygame.K_LEFT in self.tmp_key_list:
                self.tmp_key_list.append(pygame.K_LEFT)
        if pygame.K_RIGHT in list_of_keys:
            self.direction = RIGHT
            if not pygame.K_RIGHT in self.tmp_key_list:
                self.tmp_key_list.append(pygame.K_RIGHT)

        if pygame.K_DOWN in list_of_keys or pygame.K_UP in list_of_keys or pygame.K_LEFT in list_of_keys or pygame.K_RIGHT in list_of_keys:
            if self.cur_delay == 0:
                self.attack(list_of_entities)

        if pygame.K_w in list_of_keys:
            self.pos += UP * dt * self.speed
        if pygame.K_s in list_of_keys:
            self.pos += DOWN * dt * self.speed
        if pygame.K_a in list_of_keys:
            self.pos += LEFT * dt * self.speed
        if pygame.K_d in list_of_keys:
            self.pos += RIGHT * dt * self.speed


    def render(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 20)

    def attack(self, list_of_entities):
        self.cur_delay = self.attack_delay
        if self.equipment[EQUIP_WEAPON] == "Sword":
            for i in list_of_entities:
                tmp = i.pos - self.pos
                tmp = tmp.Dot(tmp)
                if tmp < 32 ** 2:
                    i.hit(5, self.direction * 20)



class Enemy(EntityBase):
    def __init__(self, name, health):
        self.name = name
        self.health = health


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


class Dummy(EntityBase):
    def __init__(self, pos):
        EntityBase.__init__(self, "DUMMY", pos)
        self.health = 100
        self.invincible = 0

    def hit(self, damage, knockback=mymath.Vector2(0, 0)):
        self.health -= damage
        self.pos += knockback
        print("HIT")

    def update(self, dt):
        if self.invincible > 0:
            self.invincible -= dt
        if self.invincible < 0:
            self.invincible = 0

    def render(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), (int(self.pos.x), int(self.pos.y)), 20)
