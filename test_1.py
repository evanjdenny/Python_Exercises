from math import pi

class Circle:
    def __init__(self, radius: int | float):
        self.geometry = 'Circle'
        self.set_radius(radius)
        self.print_stats()

    def get_radius(self):
        """Returns self.__radius"""
        return self.__radius

    def set_radius(self, radius: int | float):
        """Sets the value of self.__radius"""
        self.__radius = radius
        self.__calculate_circumference()
        self.__calculate_area()

    def __calculate_circumference(self):
        self.circumference = 2*pi*self.__radius

    def __calculate_area(self):
        self.area = pi*(self.__radius*self.__radius)

    def print_stats(self):
        print('Geometry:',self.geometry)
        print('Radius:',self.__radius)
        print('Circumference:',round(self.circumference,3))
        print('Area:',round(self.area,3))

from enum import Enum
from random import randint

class Weapon:
    def __init__(self, name: str, weapon_type, level: int, min_dmg: int, max_dmg: int, equipable_classes: list):
        self.name = name
        self.weapon_type = weapon_type
        self.level = level
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.last_damage = 0
        self.equipable_classes = equipable_classes

    def __attack(self):
        return randint(self.min_dmg, self.max_dmg)
    
    def damage_attack(self):
        self.last_damage = self.__attack()
        return self.last_damage

class PlayerClass(Enum):
    WARRIOR = 0
    RANGER = 1

class Player:
    def __init__(self, name, _class: PlayerClass):
        self.name = name
        self.player_class = _class
        self.level = 1
        self.health = 100
        self.mana = 100
        self.dodge_chance = 40
        self.equipment = {
            'Weapon': None,
            'Offhand': None,
            'Helmet': None,
            'Chest': None,
            'Right Forearm': None,
            'Left Forearm': None,
            'Gloves': None,
            'Legs': None,
            'Feet': None,
            'Ring 1': None,
            'Ring 2': None,
            'Necklace': None
        }
        self.alive = True
        self.inventory = []
        inventory_spaces = 30
        while inventory_spaces > 0:
            self.inventory.append('')
            inventory_spaces -= 1
        del inventory_spaces

    def view_inventory(self):
        print(self.inventory[0:5])
        print(self.inventory[5:10])
        print(self.inventory[10:15])
        print(self.inventory[15:20])
        print(self.inventory[20:25])
        print(self.inventory[25:30])

    def __check_alive(self):
        if self.health > 0:
            self.alive = True
        elif self.health <= 0:
            self.alive = False
        return self.alive

    def add_inventory_item(self, item: object):
        """Add an item to your inventory."""
        inv_space = 0
        while inv_space < 30:
            for content in self.inventory:
                if content == '':
                    self.inventory[inv_space] = item
                    return
                inv_space += 1
        print('No space in inventory!')

    def remove_inventory_item(self, item: object):
        """Remove the first occurence of an item from your inventory."""
        self.inventory[self.inventory.index(item)] = ''
    
    def __check_inventory_full(self):
        space = 0
        for item in self.inventory:
            if item == '':
                space += 1
        if space == 0:
            return True
        else:
            return False
    
    def __check_kill(self, target):
        if target.health <= 0:
            for item in target.inventory:
                if item != '':
                    self.add_inventory_item(item)
                    if self.__check_inventory_full():
                        pass # When game board is created, the item should
                        # be added to the ground inventory, which should allow
                        # the player to pick up from when standing on the tile.

    def attack(self, target):
        if randint(0,100) > 10:
            target.health -= self.equipment['Weapon'].damage_attack()
            print(self.name,'dealt',str(self.equipment['Weapon'].last_damage),'damage to',target.name+'.')
        else:
            print(self.name,'missed',target.name+'!')
    
    def equip_weapon(self, weapon: Weapon):
        self.equipment['Weapon'] = weapon

class Monster:
    def __init__(self, name, monster_type, health, weapon: Weapon, hit_chance):
        self.name = name
        self.monster_type = monster_type
        self.health = health
        self.weapon = weapon
        self.hit_chance = hit_chance
        self.inventory = []

    def attack(self, target: Player):
        """Attack player."""
        if randint(0,100)*self.hit_chance > target.dodge_chance:
            target.health -= self.weapon.damage_attack()
            print(self.name,'dealt',str(self.weapon.last_damage),'damage to',target.name+'.')
        else:
            print(self.name,'missed',target.name+'!')

evan = Player('Evan Denny', PlayerClass.WARRIOR)
goblin_club = Weapon('Goblin Club', 'Blunt', 1, 2, 5, [PlayerClass.WARRIOR, PlayerClass.RANGER])
goblin = Monster('Goblin', 'Creature', 20, goblin_club, 0.65)
sword = Weapon('Sword', 'Blade', 1, 5, 10, [PlayerClass.WARRIOR, PlayerClass.RANGER])
evan.equipment['Weapon'] = sword
goblin2 = Monster('Goblin', 'Creature', 20, goblin_club, 0.65)

while evan.alive:
    if goblin.health <= 0:
        del goblin
    else:
        evan.attack(goblin)
    if goblin2.health <= 0:
        del goblin2
    else:
        evan.attack(goblin2)
    goblin.attack(evan)
    goblin2.attack(evan)
    print(evan.health, goblin.health, goblin2.health)
if not evan.alive:
    print('Evan died.')
