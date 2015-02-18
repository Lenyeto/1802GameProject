#Matthew Asselin

import CustomClasses

def save():
    saveName = Player.name
    saveHealth = Player.health
    saveEquip = Player.equipment
    savePosition = Player.position

    with open("testsave.txt", 'w') as file:
        file.write("name = " + saveName + '\n')
        file.write("health = " + saveHealth + '\n')
        file.write("equip = " + saveEquip + '\n')
        file.write("pos = " + savePosition + '\n')
        file.close()

def load():
    with open("testsave.txt", 'r') as file:
        for line in file:
            line = line.strip()
            a = line.split("=")
            if len(a) == 2:
                a[0] = a[0].strip()
                a[1] = a[1].strip()
                if a[0] != '' and a[1] != '':
                    self.mydict[str(a[0])] = str(a[1])
            file.close()
        Player.name = mydict["name"]
        Player.health = mydict["health"]
        Player.equipment = mydict["equip"]
        Player.position = mydict["pos"]
