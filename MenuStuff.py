__author__ = 'William'


class GUI(object):
    def __init__(self):
        self.GUI_Objects = []

    def render(self, surface):
        pass

    def update(self, keys, mousePos):
        for i in self.GUI_Objects:
            if mousePos in i:
                i.use()


class MainMenu(GUI):
    def __init__(self):
        GUI.__init__(self)




class MultiplayerMenu(GUI):
    pass


class SingleplayerMenu(GUI):
    pass


class MenuObject(object):
    def __init__(self, rect, string):
        self.rect = rect
        self.string = string

    def render(self, surface):
        pass

    def __contains__(self, item):
        pass


class Button(MenuObject):
    pass


class TextField(MenuObject):
    pass
