#Matthew Asselin

from xml.dom import minidom

class Equipment(object):
    def __init__(self):
        self.helmet = {}
        self.chest = {}
        self.legs = {}
        self.foot = {}
        self.primary = {}
        self.secondary = {}
        self.trinket = {}
        self.consume = {}

    def equipPrimary(self, itemname):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('primary')
        for s in itemlist:
            if (s.attributes['name'].value == itemname):
                self.primary['name'] = str(s.attributes['name'].value)
                self.primary['damage'] = int(s.attributes['damage'].value)
                self.primary['delay'] = int(s.attributes['delay'].value)
                self.primary['knockback'] = int(s.attributes['knockback'].value)
                self.primary['icon'] = str(s.attributes['icon'].value)
                self.primary['range'] = int(s.attributes['range'].value)
                self.primary['velocity'] = int(s.attributes['velocity'].value)
                self.primary['armor'] = int(s.attributes['armor'].value)
                returnval = self.primary
            else:
                returnval = None
        return self

    def equipSecondary(self, itemname):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('secondary')
        for s in itemlist:
            if (s.attributes['name'].value == itemname):
                self.secondary['name'] = str(s.attributes['name'].value)
                self.secondary['damage'] = int(s.attributes['damage'].value)
                self.secondary['delay'] = int(s.attributes['delay'].value)
                self.secondary['knockback'] = int(s.attributes['knockback'].value)
                self.secondary['icon'] = str(s.attributes['icon'].value)
                self.secondary['range'] = int(s.attributes['range'].value)
                self.secondary['velocity'] = int(s.attributes['velocity'].value)
                self.secondary['armor'] = int(s.attributes['armor'].value)
                returnval = self.secondary
            else:
                returnval = None
        return self

    def equipTwohand(self, itemname):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('twohand')
        for s in itemlist:
            if (s.attributes['name'].value == itemname):
                self.primary['name'] = str(s.attributes['name'].value)
                self.primary['damage'] = int(s.attributes['damage'].value)
                self.primary['delay'] = int(s.attributes['delay'].value)
                self.primary['knockback'] = int(s.attributes['knockback'].value)
                self.primary['icon'] = str(s.attributes['icon'].value)
                self.primary['range'] = int(s.attributes['range'].value)
                self.primary['velocity'] = int(s.attributes['velocity'].value)
                self.primary['armor'] = int(s.attributes['armor'].value)
                gear.equipSecondary("Twohand")
                returnval = self.primary
            else:
                returnval = None
        return self

    def equipHelmet(self, itemname):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('helmet')
        for s in itemlist:
            if (s.attributes['name'].value == itemname):
                self.helmet['name'] = str(s.attributes['name'].value)
                self.helmet['armor'] = int(s.attributes['armor'].value)
                self.helmet['weight'] = int(s.attributes['weight'].value)
                self.helmet['type'] = str(s.attributes['weight'].value)
                self.helmet['icon'] = str(s.attributes['weight'].value)
                self.helmet['attribute'] = str(s.attributes['attribute'].value)
                returnval = self.helmet
            else:
                returnval = None
        return self

    def equipChest(self, itemname):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('chest')
        for s in itemlist:
            if (s.attributes['name'].value == itemname):
                self.chest['name'] = str(s.attributes['name'].value)
                self.chest['armor'] = int(s.attributes['armor'].value)
                self.chest['weight'] = int(s.attributes['weight'].value)
                self.chest['type'] = str(s.attributes['weight'].value)
                self.chest['icon'] = str(s.attributes['weight'].value)
                self.chest['attribute'] = str(s.attributes['attribute'].value)
                returnval = self.chest
            else:
                returnval = None
        return self

    def equipLegs(self, itemname):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('legs')
        for s in itemlist:
            if (s.attributes['name'].value == itemname):
                self.legs['name'] = str(s.attributes['name'].value)
                self.legs['armor'] = int(s.attributes['armor'].value)
                self.legs['weight'] = int(s.attributes['weight'].value)
                self.legs['type'] = str(s.attributes['weight'].value)
                self.legs['icon'] = str(s.attributes['weight'].value)
                self.legs['attribute'] = str(s.attributes['attribute'].value)
                returnval = self.legs
            else:
                returnval = None
        return self

    def equipFoot(self, itemname):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('foot')
        for s in itemlist:
            if (s.attributes['name'].value == itemname):
                self.foot['name'] = str(s.attributes['name'].value)
                self.foot['armor'] = int(s.attributes['armor'].value)
                self.foot['weight'] = int(s.attributes['weight'].value)
                self.foot['type'] = str(s.attributes['weight'].value)
                self.foot['icon'] = str(s.attributes['weight'].value)
                self.foot['attribute'] = str(s.attributes['attribute'].value)
                returnval = self.foot
            else:
                returnval = None
        return self

    def equipTrinket(self, itemname):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('trinket')
        for s in itemlist:
            if (s.attributes['name'].value == itemname):
                self.trinket['name'] = str(s.attributes['name'].value)
                self.trinket['attribute'] = str(s.attributes['attribute'].value)
                self.trinket['value'] = int(s.attributes['value'].value)
                self.trinket['icon'] = str(s.attributes['icon'].value)
                returnval = self.trinket
            else:
                returnval = None
        return self

    def equipConsumable(self, itemname):
        xmldoc = minidom.parse('items.xml')
        itemlist = xmldoc.getElementsByTagName('consumable')
        for s in itemlist:
            if (s.attributes['name'].value == itemname):
                self.consume['name'] = str(s.attributes['name'].value)
                self.consume['attribute'] = str(s.attributes['attribute'].value)
                self.consume['value'] = int(s.attributes['value'].value)
                self.consume['icon'] = str(s.attributes['icon'].value)
                returnval = self.consume
            else:
                returnval = None
        return self


gear = Equipment()

gear.equipPrimary("Longsword")
gear.equipSecondary("Steel Shield")
gear.equipChest("Leather Jerkin")
gear.equipLegs("Leather Pantaloons")
gear.equipFoot("Leather Boots")
gear.equipHelmet("Leather Helmet")
gear.equipTrinket("Magic Wand")
gear.equipConsumable("Heal Potion")
