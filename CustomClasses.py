
class EntityBase(object):
    def __init__(self, name):
        self.name = name


class ItemBase(object):
    def __init__(self, name):
        self.name = name


class Player(EntityBase):
    def __init__(self, health):
        self.name = "Hero"
        self.health = health


class Enemy(EntityBase):
    def __init__(self, name, health):
        self.name = name
        self.health = health


class Consumable(ItemBase):
    def __init__(self):
        pass


class Equipable(ItemBase):
    def __init__(self):
        pass