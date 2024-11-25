# Class to create items
class Item:
    def __init__(self, name, description):
        self.__name = name
        self.__description = description
        
    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description


# Class to create rooms
class Room:
    def __init__(self, name, description, exits, item=None, access_item=None):
        self.__name = name
        self.__description = description
        self.__exits = exits
        self.__item = item
        self.__access_item = access_item

    # Properties
    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def exits(self):
        return self.__exits.keys(), self.__exits.values()

    @property
    def item(self):
        if self.__item is not None:
            return self.__item
        else:
            return 'Nothing to loot here.'

    @property
    def access_item(self):
        return self.__access_item

    # Methods
    def can_access(self, player):
        if self.__access_item in player.inventory:
            return True
        else:
            return False

    def describe(self):
        return f'''{self.name}
{self.description}
Exits:
    {', \n\t'.join(f"{key} : {val}" for key, val in self.__exits.items())}
Item: {self.item}'''


# Class to create the player
class Player:
    def __init__(self, current_room, inventory):
        self.__current_room = current_room
        self.__inventory = inventory

    # Player actions
    def add_to_inventory(self, item):
        self.__inventory.append(item)

    def has_item(self, item_name):
        if item_name in self.__inventory:
            return True
        else:
            return False

    def show_inventory(self):
        return ', '.join(self.__inventory)


# Class to create the game
class Game:
    def __init__(self) -> None:
        pass

                    
room1 = Room(name='Entrance',
             description='You leave a huge gate behind you and are in a small hallway with a door at the end, lit by candles on the wall and smushed paintings.',
             exits={'North': 'Main Hall','South': 'Exit'},
             item='Maindoorkey',
             access_item=None)

room2 = Room(name='Main Hall',
                description='You enter a huge hall with a high ceiling and a large chandelier hanging from it. The room is filled with old furniture and a large fireplace.',
                exits={'South': 'Entrance', 'East': 'Kitchen'},
                item=None,
                access_item='Maindoorkey')

print(room1.describe())