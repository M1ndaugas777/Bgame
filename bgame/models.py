import math
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint


class Enemy(models.Model):
    name = models.CharField('Name', max_length=100, default='None')
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    level = models.IntegerField('Level', default=1)
    health = models.IntegerField('Health', default=5)
    strength = models.IntegerField('Stength', default=1)
    defense = models.IntegerField('Defense', default=0)
    experience = models.IntegerField('Experience', default=20)
    minimum_gold_pieces = models.IntegerField('Minimum_gold_pieces', default=7)
    maximum_gold_pieces = models.IntegerField('Maximum_gold_pieces', default=20)

    def __str__(self):
        return (f'{self.name}: LWL{self.level}, HP{self.health}, STR{self.strength}, DEF{self.defense}, '
                f'XP{self.experience}, GPmin{self.minimum_gold_pieces}, GPmax{self.maximum_gold_pieces}')


class Player(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField('Level', default=1)
    health = models.IntegerField('Health', default=10)
    strength = models.IntegerField('Stength', default=1)
    defense = models.IntegerField('Defense', default=1)
    experience = models.IntegerField('Experience', default=0)
    gold_pieces = models.IntegerField('GoldPieces', default=100)
    attribute_points = models.IntegerField('Attribute points', default=3)
    experience_threshold = models.FloatField('Experience Threshold', default=100)
    maximum_health = models.IntegerField('Current health', default=10)

    is_weapon_equiped = models.BooleanField('Weapon equiped', default=False)
    is_helmet_equiped = models.BooleanField('Helmet equiped', default=False)
    is_chest_armour_equiped = models.BooleanField('Armour equiped', default=False)
    is_leg_armour_equiped = models.BooleanField('Leg armour equiped', default=False)
    is_boots_equiped = models.BooleanField('Boots equiped', default=False)
    is_gloves_equiped = models.BooleanField('Gloves equiped', default=False)
    is_shield_equiped = models.BooleanField('Weapon equiped', default=False)
    is_ring_equiped = models.BooleanField('Ring equiped', default=False)
    is_pet_equiped = models.BooleanField('Pet equiped', default=False)

    def attack(self, enemy):

        player_health = self.health
        base_player_damage = self.strength
        player_defense = self.defense

        enemy_health = enemy.health
        base_enemy_damage = enemy.strength
        enemy_defense = enemy.defense

        player_damage_dealt = 0
        enemy_damage_dealt = 0

        level_up = False
        is_winner = False

        while player_health > 0 and enemy_health > 0:

            player_damage = randint(0, base_player_damage)
            enemy_damage = randint(0, base_enemy_damage)

            enemy_actual_damage = enemy_damage - player_defense
            if enemy_actual_damage < 1:
                enemy_actual_damage = 1

            player_actual_damage = player_damage - enemy_defense
            if player_actual_damage < 1:
                player_actual_damage = 1

            player_damage_dealt += player_actual_damage
            enemy_health -= player_actual_damage
            if enemy_health <= 0:
                break

            player_health -= enemy_actual_damage
            enemy_damage_dealt += enemy_actual_damage

        gold_gained = randint(enemy.minimum_gold_pieces, enemy.maximum_gold_pieces)

        if enemy_health <= 0:
            is_winner = True
            player_damage_taken = enemy_damage_dealt
            player_damage_dealt = player_damage_dealt

            self.experience += enemy.experience

            self.gold_pieces += gold_gained

            if self.experience >= self.experience_threshold:
                self.level += 1
                self.experience = 0
                if self.experience_threshold > 50000:
                    self.experience_threshold = math.ceil(self.experience_threshold * 1.01)
                else:
                    self.experience_threshold = math.ceil(self.experience_threshold * 1.05)
                self.attribute_points += 3
                level_up = True
                self.health = self.maximum_health
                self.save()
            else:
                level_up = False
                self.health -= player_damage_taken
                self.save()

        if player_health <= 0:
            is_winner = False
            self.health = 1
            self.save()
        enemy_health_remaining = enemy.health - player_damage_dealt

        return is_winner, enemy.experience, gold_gained, player_damage_dealt, enemy_damage_dealt, level_up, self.health, enemy_health_remaining

    def __str__(self):
        return f' {self.username} {self.level} {self.health} {self.strength} {self.defense} {self.experience} {self.attribute_points} {self.experience_threshold} {self.maximum_health}'

    @receiver(post_save, sender=User)
    def create_player(sender, instance, created, **kwargs):
        if created:
            player = Player.objects.create(username=instance)

            totem_names = ['Totem of strength', 'Totem of defense', 'Totem of health']
            for totem_name in totem_names:
                Totem.objects.create(player=player, totem_name=totem_name)

            WiseElder.objects.create(player=player)
            items = Items.objects.all()
            for item in items:
                quantity = 0
                if item.item_name == 'Bread':
                    quantity = 5
                if item.item_name == 'Rusty sword':
                    quantity = 1

                Inventory.objects.create(player=player, item=item, quantity=quantity)

    @receiver(post_save, sender=User)
    def save_player(sender, instance, **kwargs):
        instance.player.save()


class CityLocation(models.Model):
    city_location_name = models.CharField('Location', max_length=100, )

    def __str__(self):
        return f'{self.city_location_name}'


class Items(models.Model):
    item_name = models.CharField('Item name', max_length=100, default='nothing')
    item_type = models.CharField('Item type', max_length=100, default='nothing')

    healing_power = models.IntegerField('Healing power', default=4, null=True, blank=True)
    strength_modifier = models.IntegerField('Strenght bonus', default=0)
    defense_modifier = models.IntegerField('Defense bonus', default=0)
    health_modifier = models.IntegerField('Health modifier', default=0)

    item_buy_price = models.IntegerField('Buy price', default=50)
    item_sell_price = models.IntegerField('Sell price', default=50)

    store_location = models.ForeignKey('CityLocation', on_delete=models.CASCADE, blank=True, null=True)
    owners = models.ManyToManyField(Player, through='Inventory')

    def __str__(self):
        return f' {self.item_name} {self.item_type}'


class Inventory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantity', null=True, blank=True)

    def increase_quantity(self, amount=1):
        self.quantity += amount
        self.save()

    def decrease_quantity(self, amount=1):
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()

    def use_item(self, player):
        if self.item.item_type == 'Healing item' and self.quantity > 0:
            player.health += self.item.healing_power
            player.maximum_health += self.item.health_modifier

            if player.health > player.maximum_health:
                player.health = player.maximum_health
            player.save()
            self.quantity -= 1
            self.save()

            return f'{player.health} {player.maximum_health} '

    def equip_item(self, player):
        if self.quantity <= 0:
            return

        if self.item.item_type == 'Weapon' and not player.is_weapon_equiped:
            player.is_weapon_equiped = True
        elif self.item.item_type == 'Helmet' and not player.is_helmet_equiped:
            player.is_helmet_equiped = True
        elif self.item.item_type == 'Chest' and not player.is_chest_armour_equiped:
            player.is_chest_armour_equiped = True
        elif self.item.item_type == 'Leg armour' and not player.is_leg_armour_equiped:
            player.is_leg_armour_equiped = True
        elif self.item.item_type == 'Boots' and not player.is_boots_equiped:
            player.is_boots_equiped = True
        elif self.item.item_type == 'Gloves' and not player.is_gloves_equiped:
            player.is_gloves_equiped = True
        elif self.item.item_type == 'Shield' and not player.is_shield_equiped:
            player.is_shield_equiped = True
        elif self.item.item_type == 'Ring' and not player.is_ring_equiped:
            player.is_ring_equiped = True
        elif self.item.item_type == 'Pet' and not player.is_pet_equiped:
            player.is_pet_equiped = True

        player.strength += self.item.strength_modifier
        player.defense += self.item.defense_modifier
        player.maximum_health += self.item.health_modifier
        player.health += self.item.health_modifier
        player.save()
        self.save()

    def unequip_item(self, player):
        if self.quantity <= 0:
            return

        if self.item.item_type == 'Weapon' and player.is_weapon_equiped:
            player.is_weapon_equiped = False
        elif self.item.item_type == 'Helmet' and player.is_helmet_equiped:
            player.is_helmet_equiped = False
        elif self.item.item_type == 'Chest' and player.is_chest_armour_equiped:
            player.is_chest_armour_equiped = False
        elif self.item.item_type == 'Leg' and player.is_leg_armour_equiped:
            player.is_leg_armour_equiped = False
        elif self.item.item_type == 'Boots' and player.is_boots_equiped:
            player.is_boots_equiped = False
        elif self.item.item_type == 'Gloves' and player.is_gloves_equiped:
            player.is_gloves_equiped = False
        elif self.item.item_type == 'Shield' and player.is_shield_equiped:
            player.is_shield_equiped = False
        elif self.item.item_type == 'Ring' and player.is_ring_equiped:
            player.is_ring_equiped = False
        elif self.item.item_type == 'Pet' and player.is_pet_equiped:
            player.is_pet_equiped = False

        player.strength -= self.item.strength_modifier
        player.defense -= self.item.defense_modifier
        player.maximum_health -= self.item.health_modifier
        player.health -= self.item.health_modifier
        player.save()
        self.save()

    def __str__(self):
        return f'{self.player.username} - {self.item.item_name}: {self.quantity} '


class Location(models.Model):
    name = models.CharField('Location', max_length=100, )

    def __str__(self):
        return f'{self.name} '


class Totem(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    totem_name = models.CharField('Totem', max_length=100, )
    strength_prayer_price = models.IntegerField('Pray strength', default=100)
    defense_prayer_price = models.IntegerField('Pray defense', default=100)
    health_prayer_price = models.IntegerField('Pray health', default=100)

    def pray(self, player):
        if self.totem_name == 'Totem of strength' and player.gold_pieces >= self.strength_prayer_price:
            player.gold_pieces -= self.strength_prayer_price
            player.strength += 1
            player.save()
            self.strength_prayer_price = self.strength_prayer_price * 2
            self.save()

        elif self.totem_name == 'Totem of defense' and player.gold_pieces >= self.defense_prayer_price:
            player.gold_pieces -= self.defense_prayer_price
            player.defense += 1
            player.save()
            self.defense_prayer_price = self.defense_prayer_price * 2
            self.save()

        elif self.totem_name == 'Totem of health' and player.gold_pieces >= self.health_prayer_price:
            player.gold_pieces -= self.health_prayer_price
            player.maximum_health += 1
            player.health += 1
            player.save()
            self.health_prayer_price = self.health_prayer_price * 2
            self.save()

    def __str__(self):
        return f'{self.totem_name}'


class WiseElder(models.Model):
    name = models.CharField('Elder', max_length=100, default='WiseElder')
    knowledge_price = models.IntegerField('Price', default=100)
    variable = models.IntegerField('Variable', default=0)
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='wise_elder', blank=True, null=True)

    knowledge_1_unlocked = models.BooleanField(default=False)
    knowledge_2_unlocked = models.BooleanField(default=False)
    knowledge_3_unlocked = models.BooleanField(default=False)
    knowledge_4_unlocked = models.BooleanField(default=False)
    knowledge_5_unlocked = models.BooleanField(default=False)
    knowledge_6_unlocked = models.BooleanField(default=False)
    knowledge_7_unlocked = models.BooleanField(default=False)

    knowledge_messages = [
        '1. If you want to fullfill your destiny, consider your health as a priority.',
        '2. The price of aquiring power from three ancient tokens doubles each time you pray.',
        "3. If you want to aquire wealth, consider doing a lot of low effort task's, instead of a few high effort ones.",
        "4. If you desire power not money, in that case doing a few difficult task's is more rewarding than alot of"
        " easy ones.",
        '5. Who knows if my vision was correct, only you can prove it.',
        '6. I see you are persistant on your quest, you might want to consider obtaining powerfull pets and rings,'
        ' as they will enhance your abilities the most.'
        '7. If you really want to stand a change againts Demon lord B, you should consider obtaining items from another'
        ' dimension.',
        '8. There is nothing more i can tell you Best of luck warrior!'
    ]

    def pay(self, player):
        if player.gold_pieces >= self.knowledge_price:
            setattr(self, f'knowledge_{self.variable + 1}_unlocked', True)
            player.gold_pieces -= self.knowledge_price
            self.variable += 1
            self.knowledge_price *= 5
            self.save()
            player.save()

    @property
    def knowledge_acquired(self):
        return getattr(self, f'knowledge_{self.variable}_unlocked', False)

    def __str__(self):
        return f'{self.name} {self.knowledge_price} {self.knowledge_acquired}'
