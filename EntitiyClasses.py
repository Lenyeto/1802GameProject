import mymath
import xml.etree.ElementTree as ET
import pygame
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
    def __init__(self, name, pos, velocity=mymath.Vector2(0, 0)):
        self.name = name
        self.pos = pos
        self.velocity = velocity

    def ai_player(self, player):
        pass

class Projectile(EntityBase):
    def __init__(self, pos, velocity, height=1):
        self.pos = pos
        self.velocity = velocity
        self.height = height
        self.isPiercing = False
        self.attack = 5

    def update(self, dt, entityList):
        self.pos += self.velocity * dt
        for e in entityList:
            tmp = self.pos - e.pos
            dist = tmp.Dot(tmp)
            if dist < 16**2:
                self.damage(e)
                return True
        return False

    def damage(self, other):
        other.health -= self.attack

    def render(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 5)


class CosProjectile(Projectile):
    def __init__(self, pos, velocity, height=1):
        Projectile.__init__(self, pos, velocity, height)
        self.acum = 0

    def update(self, dt, entityList):
        self.acum += dt
        # FIX TO WORK DOWNWARDS
        self.velocity.y = math.cos(self.acum) * 100
        if Projectile.update(self, dt, entityList):
            return True

class FireFlyProj(Projectile):
    def __init__(self, pos, velocity, height=1):
        Projectile.__init__(self, pos, velocity, height)
        self.acum = 0

    def update(self, dt, entityList):
        self.acum += dt
        self.velocity.y = math.cos(self.acum) * 10
        self.velocity.x = math.sin(self.acum) * 10
        if Projectile.update(self, dt, entityList):
            return True


class TrackingProj(Projectile):
    def __init__(self, pos, velocity, height=1):
        Projectile.__init__(self, pos, velocity, height)
        self.acum = 0
        self.target = NONE
        self.speed = velocity.Dot(velocity) ** 0.5

    def update(self, dt, entityList):
        if self.target == NONE:
            distanceList = []
            distanceList2 = []
            for i in entityList:
                tmp = self.pos - i.pos
                dist = tmp.Dot(tmp)
                distanceList.append(dist)
                distanceList2.append(dist)
            distanceList.sort()
            tmp = distanceList2.index(distanceList[0])
            self.target = entityList[tmp]
        else:
            tmp = self.target.pos - self.pos
            tmp = tmp.getNormalized()
            tmp *= dt
            self.velocity += tmp
            self.velocity = self.velocity.getNormalized()
            self.velocity *= self.speed
        if Projectile.update(self, dt, entityList):
            return True

    def render(self, surface):
        Projectile.render(self, surface)



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
        self.sub_entities = []

        self.tmp_key_list = []

        if debug:
            self.equipment[EQUIP_WEAPON] = "Bow"


    def update(self, dt, list_of_keys, list_of_entities):
        if self.cur_delay > 0:
            self.cur_delay -= dt
        if self.cur_delay < 0:
            self.cur_delay = 0

        for i in self.sub_entities:
            if i.update(dt, list_of_entities):
                self.sub_entities.remove(i)

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
        for i in self.sub_entities:
            i.render(surface)


    def attack(self, list_of_entities):
        self.cur_delay = self.attack_delay
        if self.equipment[EQUIP_WEAPON] == "Sword":
            for i in list_of_entities:
                tmp = i.pos - self.pos
                tmp = tmp.Dot(tmp)
                if tmp < 64 ** 2:
                    i.hit(5, self.direction * 20)
        elif self.equipment[EQUIP_WEAPON] == "Bow":
            #self.sub_entities.append(TestProj(self.pos.copy(), self.direction.copy()))
            pass
        elif self.equipment[EQUIP_WEAPON] == "Spell":
            pass



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
        self.show_health = 0

    def hit(self, damage, knockback=mymath.Vector2(0, 0)):
        self.health -= damage
        self.pos += knockback
        self.show_health = 10

    def update(self, dt):
        if self.invincible > 0:
            self.invincible -= dt
        if self.invincible < 0:
            self.invincible = 0
        if self.show_health > 0:
            self.show_health -= dt
        if self.show_health < 0:
            self.show_health = 0
        if self.health <= 0:
            return True
        #self.velocity.x = math.cos(dt) * dt
        self.pos += self.velocity
        return False

    def render(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), (int(self.pos.x), int(self.pos.y)), 20)
        #if self.show_health > 0:
        tmpX = 40
        tmpX *= self.health / 100
        pygame.draw.rect(surface, (125, 125, 125), (int(self.pos.x) - tmpX/2, int(self.pos.y - 10) - 20, tmpX, 5))
