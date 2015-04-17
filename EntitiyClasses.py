import mymath
import xml.etree.ElementTree as ET
import pygame
import math
import random
from xmlweapons import *
from UtilFuncs import *

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
    def __init__(self, name, pos, velocity=mymath.Vector2(0, 0), physical=True, background=False):
        self.name = name
        self.pos = pos
        self.velocity = velocity
        self.physical = physical
        self.background = background

    def ai_player(self, player):
        pass

    def hit(self, x, k=mymath.Vector2(0, 0)):
        pass

    def update(self, dt):
        pass

class Projectile(EntityBase):
    def __init__(self, pos, velocity, height=1, damage=1):
        self.pos = pos.copy()
        self.velocity = velocity
        self.height = height
        self.isPiercing = False
        self.attack = damage

    def update(self, dt, entityList):
        self.pos += self.velocity * dt
        for e in entityList:
            if isinstance(e, Wall_Floor):
                if e.physical:
                    tmp = self.pos - e.pos
                    dist = tmp.Dot(tmp)
                    if dist < 16 ** 2:
                        return True
            else:
                tmp = self.pos - e.pos
                dist = tmp.Dot(tmp)
                if dist < 16**2:
                    self.damage(e)
                    return True
        return False

    def damage(self, other):
        other.hit(self.attack)

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

class particle(object):
    def __init__(self, pos, image, life, direction):
        self.pos = pos
        self.image = image
        self.life = life
        if direction == UP:
            self.rotation = 0
        elif direction == RIGHT:
            self.rotation = 90
        elif direction == LEFT:
            self.rotation = 180
        elif direction == DOWN:
            self.rotation = 270

    def update(self, dt):
        self.life -= dt
        if self.life < 0:
            return True
        return False

    def render(self, surface):
        tmp = pygame.transform.rotate(self.image, self.rotation)
        #surface.blit(tmp, (self.pos.x - tmp.get_width()/2, self.pos.y - tmp.get_height()/2))


class Player(EntityBase):
    def __init__(self, pos=mymath.Vector2(0, 0), health=100, debug=False):
        self.pos = pos
        self.name = "Hero"
        self.health = health
        self.speed = 0.4


        self.equipment = [-1, -1, -1, -1, -1, -1, [], []]
        self.direction = DOWN
        self.invincibility_period = 0
        self.attack_delay = 1000
        self.cur_delay = 0
        self.sub_entities = []
        self.particles = []


        self.tmp_key_list = []

        #if debug:
        self.equipment[EQUIP_WEAPON] = Weapon()
        self.equipment[EQUIP_WEAPON].getWeapon("Longsword")


    def update(self, dt, list_of_keys, list_of_entities):
        #equip_weight_sum = 0
        #for i in self.equipment:
        #    if not i == -1 and not isinstance(i, list):
        #        equip_weight_sum += i.weight / 10
        #self.speed = 0.4 - equip_weight_sum
        #if self.speed < 0.05:
        #    self.speed = 0.05





        if self.cur_delay > 0:
            self.cur_delay -= dt
        if self.cur_delay < 0:
            self.cur_delay = 0

        if self.invincibility_period > 0:
            self.invincibility_period -= dt
        if self.invincibility_period < 0:
            self.invincibility_period = 0

        for i in self.sub_entities:
            if i.update(dt, list_of_entities):
                self.sub_entities.remove(i)

        for i in self.particles:
            if i.update(dt):
                self.particles.remove(i)

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
            self.attemptMove(UP, list_of_entities, dt)
        if pygame.K_s in list_of_keys:
            self.attemptMove(DOWN, list_of_entities, dt)
        if pygame.K_a in list_of_keys:
            self.attemptMove(LEFT, list_of_entities, dt)
        if pygame.K_d in list_of_keys:
            self.attemptMove(RIGHT, list_of_entities, dt)

    def attemptMove(self, direction, list_of_entities, dt):
        new_position = self.pos + direction
        for e in list_of_entities:
            if e.physical:
                if isinstance(e, Wall_Floor):
                    tmp = new_position - e.pos
                    newDist = tmp.Dot(tmp)
                    tmp2 = self.pos - e.pos
                    oldDist = tmp2.Dot(tmp2)
                    if newDist < 20**2 and newDist < oldDist:
                        return False
                else:
                    tmp = new_position - e.pos
                    newDist = tmp.Dot(tmp)
                    tmp2 = self.pos - e.pos
                    oldDist = tmp2.Dot(tmp2)

                    if newDist < 40**2 and newDist < oldDist:
                        return False
        self.pos += direction * dt * self.speed
        return True


    def render(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 20)
        for i in self.sub_entities:
            i.render(surface)
        for i in self.particles:
            i.render(surface)


    def attack(self, list_of_entities):
        if isinstance(self.equipment[EQUIP_WEAPON], Weapon):
            self.cur_delay = self.attack_delay
            if self.equipment[EQUIP_WEAPON].weapon['wtype'] == 'Melee':
                for i in list_of_entities:
                    tmp = i.pos - self.pos
                    tmp = tmp.Dot(tmp)
                    if tmp < int(self.equipment[EQUIP_WEAPON].weapon['range'])** 2:
                        i.hit(self.equipment[EQUIP_WEAPON].weapon['damage'], self.direction * 20)
                self.particles.append(particle(self.pos + self.direction * 10, swipe, 500, self.direction))
            elif self.equipment[EQUIP_WEAPON].weapon['wtype'] == "Ranged":
                self.sub_entities.append(Projectile(self.pos, self.direction*self.equipment[EQUIP_WEAPON].weapon['velocity'], 1, self.equipment[EQUIP_WEAPON].weapon['damage']))
            elif self.equipment[EQUIP_WEAPON].weapon['wtype'] == "Spell":
                pass

    def hit(self, damage):
        self.health -= damage
        self.invincibility_period = 5



class Enemy(EntityBase):
    def __init__(self, name, health):
        self.name = name
        self.health = health


class ItemStand(EntityBase):
    def __init__(self, item, pos):
        EntityBase.__init__(self, "", pos)

        self.item = item

        self.cool_down = 10

    def pick_up(self, player):

        self.cool_down = 1000

    def update(self, dt, players=[]):
        if self.cool_down == 0:
            for p in players:
                dist_vect = p.pos - self.pos
                dist = dist_vect.Dot(dist_vect)
                if dist < 50**2:
                    self.pick_up(p)
        else:
            self.cool_down -= dt
            if self.cool_down < 0:
                self.cool_down = 0

    def render(self, surface):
        pygame.draw.rect(surface, (125, 125, 125), (int(self.pos.x-20), int(self.pos.y+20), 40, 20))
        if not self.item == -1:
            pygame.draw.circle(surface, (self.cool_down/1000 * 255, 225, 225), (int(self.pos.x), int(self.pos.y)), 15)


class WeaponStand(ItemStand):
    def __init__(self, weapon, pos):
        ItemStand.__init__(self, weapon, pos)

    def pick_up(self, player):
        if isinstance(player.equipment[EQUIP_WEAPON], Weapon):
            if not self.item == -1:
                tmp = self.item
                self.item = player.equipment[EQUIP_WEAPON]
                player.equipment[EQUIP_WEAPON] = tmp
        else:
            player.equipment[EQUIP_WEAPON] = self.item
            self.item = -1
        self.cool_down = 1000

    def render(self, surface):
        pygame.draw.rect(surface, (self.cool_down/1000 * 255, 225, 225), (int(self.pos.x-20), int(self.pos.y + 20), 40, 20))
        tmpImage = pygame.image.load(self.item.weapon['graphic'])
        surface.blit(tmpImage, (int(self.pos.x - tmpImage.get_width()/2), int(self.pos.y - tmpImage.get_height()/2)))



class Dummy(EntityBase):
    def __init__(self, pos):
        EntityBase.__init__(self, "ENEMY", pos)
        self.health = 100
        self.invincible = 0
        self.show_health = 0
        self.speed = 0.01
        self.target = None

    def hit(self, damage, knockback=mymath.Vector2(0, 0)):
        self.health -= damage
        self.pos += knockback
        self.show_health = 10

    def attemptMove(self, direction, players, dt):
        new_position = self.pos + direction
        for e in players:
            tmp = new_position - e.pos
            if tmp.Dot(tmp) < 40**2:
                return False
        self.pos += direction * dt * self.speed
        return True

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

    def AI(self, players, dt):
        if self.target == None:
            if len(players) > 1:
                distList = []
                distList2 = players.copy()
                for p in players:
                    tmp = self.pos - p.pos
                    dist = tmp.Dot(tmp)
                    distList.append(dist)
                distList.sort()
                distList2.index(distList[0])
            else:
                self.target = players[0]
        else:
            dir = (self.target.pos - self.pos).getNormalized()
            self.attemptMove(dir, players, dt)


class Wall_Floor(EntityBase):
    def __init__(self, name, pos, texture, physical=True, background=True):
        EntityBase.__init__(self, name, pos, mymath.Vector2(0, 0), physical, background)
        self.texture = pygame.transform.scale(pygame.image.load(texture), (32, 32))

    def render(self, surface):
        surface.blit(self.texture, (self.pos.x, self.pos.y))