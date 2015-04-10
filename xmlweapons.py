from xml.dom import minidom

class Weapon(object):
    def __init__(self):
        self.weapon = {}

    def __str__(self):
        returnval = str(self.weapon['name']) + str(self.weapon['damage']) + str(self.weapon['delay']) + str(self.weapon['knockback']) + str(self.weapon['graphic']) + str(self.weapon['type']) + str(self.weapon['range']) + str(self.weapon['velocity'])
        return returnval

    def getWeapon(self, weapon):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('item')
        for s in itemlist:
            if (s.attributes['name'].value == weapon):
                self.weapon['name'] = str(s.attributes['name'].value)
                self.weapon['damage'] = int(s.attributes['damage'].value)
                self.weapon['delay'] = int(s.attributes['delay'].value)
                self.weapon['knockback'] = int(s.attributes['knockback'].value)
                self.weapon['graphic'] = str(s.attributes['graphic'].value)
                self.weapon['type'] = str(s.attributes['type'].value)
                self.weapon['range'] = int(s.attributes['range'].value)
                self.weapon['velocity'] = int(s.attributes['velocity'].value)
                self.weapon['wtype'] = str(s.attributes['wtype'].value)

        return self

#pweapon = Weapon()

#pweapon.getWeapon("Longsword")
#pweapon.getWeapon("Dagger")
#print(pweapon.weapon['damage'])
