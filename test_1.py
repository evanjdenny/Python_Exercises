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

class WeaponType(Enum):
    SHORT_BLADE = 0
    LONG_BLADE = 1
    BLUNT_MELEE = 2
    BOW = 3
    CROSSBOW = 4
    GUN = 5

class WeaponLevel(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class Level:
    """Levels and experience."""
    def __init__(self):
        self.current_level = 1
        self.current_experience = 0
        self.experience = {
            1: 0,
            2: 240,
            3: 720,
            4: 2160,
            5: 6480
        }

    def add_exp(self, exp: int):
        """Add experience to Level.current_experience."""
        self.current_experience += exp

    def check_level(self):
        """Check if your experience is high enough to progress to
        the next level."""
        if self.current_experience >= self.experience[self.current_level + 1]:
            self.current_level += 1
            print('You leveled up! You are now level', self.current_level)

class Weapon:
    def __init__(self, name: str, weapon_type: WeaponType, level: WeaponLevel, min_dmg: int, max_dmg: int, equipable_classes: list):
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
        self.level = Level()
        self.experience_to_next_level = self.level.experience[self.level.current_level+1]
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
        """Print inventory to the screen in a easy-to-view way."""
        print(self.inventory[0:5])
        print(self.inventory[5:10])
        print(self.inventory[10:15])
        print(self.inventory[15:20])
        print(self.inventory[20:25])
        print(self.inventory[25:30])

    def __calc_exp_to_next_lvl(self):
        self.experience_to_next_level = self.level.experience[self.level.current_level+1]-self.level.current_experience

    def print_current_level(self):
        """Prints player's current level and the amount of experience until the next level."""
        print(self.name,'is currently level',str(self.level.current_level)+'.')
        print(self.experience_to_next_level,'experience to level',self.level.current_level+1)

    def check_level_up(self):
        """Check if player has enough experience to progress to the next level."""
        self.level.check_level()

    def check_alive(self):
        """Check if player is alive or not."""
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
            print(self.name,'killed',target.name+'.')
            self.level.add_exp(target.experience)
            self.__calc_exp_to_next_lvl()
            for item in target.inventory:
                if item != '':
                    self.add_inventory_item(item)
                    if self.__check_inventory_full():
                        pass # When game board is created, the item should
                        # be added to the ground inventory, which should allow
                        # the player to pick up from when standing on the tile.

    def attack(self, target):
        """Attack a target using the player's weapon."""
        if randint(0,100) > 25:
            target.health -= self.equipment['Weapon'].damage_attack()
            print(self.name,'dealt',str(self.equipment['Weapon'].last_damage),'damage to',target.name+'.')
        else:
            print(self.name,'missed',target.name+'!')
        self.__check_kill(target)
    
    def equip_weapon(self, weapon: Weapon):
        """Equip a weapon to the player."""
        self.equipment['Weapon'] = weapon

class Monster:
    """Monsters that give experience to the player upon being killed."""
    def __init__(self, name, monster_type, health, weapon: Weapon, hit_chance, experience):
        self.name = name
        self.monster_type = monster_type
        self.health = health
        self.alive = True
        self.weapon = weapon
        self.hit_chance = hit_chance
        self.inventory = []
        self.experience = experience

    def check_alive(self):
        if self.health > 0:
            self.alive = True
        else:
            self.alive = False

    def attack(self, target: Player):
        """Attack player."""
        self.check_alive()
        if self.alive:
            if randint(0,100)*self.hit_chance > target.dodge_chance:
                target.health -= self.weapon.damage_attack()
                print(self.name,'dealt',str(self.weapon.last_damage),'damage to',target.name+'.')
            else:
                print(self.name,'missed',target.name+'!')
            target.check_alive()

evan = Player('Evan Denny', PlayerClass.WARRIOR)
goblin_club = Weapon('Goblin Club', WeaponType.BLUNT_MELEE, WeaponLevel.ONE, 2, 5, [PlayerClass.WARRIOR, PlayerClass.RANGER])
goblin = Monster('Goblin', 'Creature', 20, goblin_club, 0.90, 5)
sword = Weapon('Sword', WeaponType.BLUNT_MELEE, WeaponLevel.ONE, 5, 10, [PlayerClass.WARRIOR, PlayerClass.RANGER])
evan.equipment['Weapon'] = sword
goblin2 = Monster('Goblin', 'Creature', 20, goblin_club, 0.90, 5)

while evan.alive and (goblin.health>0 or goblin2.health>0):
    if goblin.health <= 0:
        pass
    else:
        goblin.attack(evan)
        evan.attack(goblin)
    if goblin2.health <= 0:
        pass
    else:
        goblin2.attack(evan)
        evan.attack(goblin2)
    print(evan.health, goblin.health, goblin2.health)
if not evan.alive:
    print(evan.name,'died.')
evan.print_current_level()