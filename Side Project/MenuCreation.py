__author__ = 'William'
import MenuStuff

def getMainMenu():
    m = MenuStuff.MainMenu()
    m.GUI_Objects.append(MenuStuff.Button((0, 0, 200, 50), "Single Player"))
    m.GUI_Objects.append(MenuStuff.Button((0, 0, 200, 50), "Multiplayer Player"))
    m.GUI_Objects.append(MenuStuff.Button((0, 0, 200, 50), "Options"))
    m.GUI_Objects.append(MenuStuff.Button((0, 0, 200, 50), "Quit"))
    return m