import math

#ItemData will be organized like [Name, Image, Type, Range (could be 0 if melee), Special Modifier List]

class ItemBase(object):
    def __init__(self, itemData):
        self.name = itemData[0]
        self.image = itemData[1]
        self.type = itemData[2]
        self.range = itemData[3]
        self.specialModifier = itemData[4]
