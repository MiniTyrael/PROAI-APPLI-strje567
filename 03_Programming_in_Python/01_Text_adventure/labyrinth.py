# Class to create the player
class Player:
    def __init__(self, current_room, inventory):
        self.current_room = current_room
        self.inventory = inventory
    
    # Player actions
    def showInventory(self):
        return print(f"Your bag contains: {', '.join(self.inventory)}.")
    
    # def go(direction):
    #     return direction
    
    def addItem(self, item):
        self.inventory.append(item)


# Class to create items
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        

# Class to create rooms
class Room:
    def __init__(self, name, description, exits, item, accessItem=None):
        self.name = name
        self.description = description
        self.exits =  exits
        self.item = item
        self.accessItem = accessItem
    
    # Actions
    def explainRoom(self):
        return print(f'''{self.name}
{self.description}
{', '.join(self.exits)}''')
        

class Game:
    

                    
room1 = Room(name='Entrance',
             description='You leave a huge gate behind you and are in a small hallway with a door at the end, lit by candles on the wall and smushed paintings.',
             exits={'North': 'Main Hall','South': 'Exit'},
             item=None,accessItem=None)

room1.explainRoom()

listi= [1,23,3]
