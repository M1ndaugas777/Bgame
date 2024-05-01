from .models import CityLocation, Enemy, Inventory, Location, Player, Totem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect


def index(request):
    return render(request, 'main.html')


@login_required
def main(request):
    player = request.user.player
    player_username = request.user.username
    player_level = player.level
    player_health = player.health
    player_strength = player.strength
    player_defense = player.defense
    player_experience = player.experience
    player_gold = player.gold_pieces
    player_attribute_points = player.attribute_points
    player_experience_threshold = player.experience_threshold
    player_maximum_health = player.maximum_health

    locations = Location.objects.all().order_by('id')

    city_locations = CityLocation.objects.all().order_by('id')

    totems = Totem.objects.all().filter(player=player)

    return render(request, 'main.html', {
        'player_username': player_username,
        'player_level': player_level,
        'player_health': player_health,
        'player_strength': player_strength,
        'player_defense': player_defense,
        'player_experience': player_experience,
        'player_gold': player_gold,
        'locations': locations,
        'player_attribute_points': player_attribute_points,
        'player_experience_threshold': player_experience_threshold,
        'player_maximum_health': player_maximum_health,
        'city_locations': city_locations,
        'totems': totems,

    })


@login_required
def location_detail(request, location_name):
    location = Location.objects.get(name=location_name)
    enemies_in_location = Enemy.objects.filter(location=location)

    return render(request, 'location_detail.html', {'location': location, 'enemies_in_location': enemies_in_location})


@login_required
def city_location_detail(request, location_name):
    player = request.user.player
    city_location = get_object_or_404(CityLocation, city_location_name=location_name)
    items_in_store = Inventory.objects.filter(player=player, item__store_location=city_location)
    item_quantity = [item.quantity for item in items_in_store]

    player_money = player.gold_pieces

    return render(request, 'city_location_detail.html', {
        'items_in_store': items_in_store,
        'city_location': city_location,
        'item_quantity': item_quantity,
        'player_money': player_money,
        'player': player,

    })


@login_required()
def enemy_detail(request, enemy_name, username):
    enemy = Enemy.objects.get(name=enemy_name)
    enemy_health = enemy.health
    player = get_object_or_404(Player, username__username=username)
    player_health = player.health
    location = enemy.location
    username = request.user.username

    enemy_images = {
        'Forest': {
            'Goblin': 'goblin.jpg',
            'Angry goblin': 'angry_goblin.jpg',
            'Hobgoblin': 'hobgoblin.jpg',
            'Wounded bear': 'wounded-bear.jpg',
            'Wolf': 'wolf.jpg',
            'Hobgoblin leader': 'hobgoblin-leader.jpg',
            'Ancient bear': 'ancient-bear.jpg',
        },
        'Evil forest': {
            'Undead goblin': 'undead-goblin.jpg',
            'Zombie': 'zombie.jpg',
            'Imp': 'imp.jpg',
            'Giant imp': 'giant-imp.jpg',
            'Ogre': 'ogre.jpg',
            'Witch': 'witch.jpg',
            'Lesser demon': 'lesser-demon.jpg'
        },
        'Cursed wastelands': {
            'Curse bearing imp': 'curse-bearing-imp.jpg',
            'Skeleton': 'skeleton.jpg',
            'Ancient witch': 'ancient-witch.jpg',
            'Angry survivor': 'angry-survivor.jpg',
            'Baby dragon': 'baby-dragon.jpg',
            'Mysterious stranger': 'mysterious-stranger.jpg',
            'Skeleton warrior': 'skeleton-warrior.jpg'
        },
        'Endless desert': {
            'Desert spider': 'desert-spider.jpg',
            'Lost wanderer': 'lost-wanderer.jpg',
            'Giant snake': 'giant-snake.jpg',
            'Shaman': 'shaman.jpg',
            'Genie': 'genie.jpg',
            'Giant scorpion': 'giant-scorpion.jpg',
            'Spirit of the desert': 'spirit-of-the-desert.jpg'
        },
        'Demon wastelands': {
            'Fire demon': 'fire-demon.jpg',
            'Water demon': 'water-demon.jpg',
            'Air demon': 'air-demon.jpg',
            'Earth demon': 'earth-demon.jpg',
            'Storm demon': 'storm-demon.jpg',
            'Elemental demon': 'elemental-demon.jpg',
            'Demon of the wastelands': 'demon-of-the-wastelands.jpg',
        },
        'Mountain of dragons': {
            'Fire dragon': 'fire-dragon.jpg',
            'Water dragon': 'water-dragon.jpg',
            'Air dragon': 'air-dragon.jpg',
            'Earth dragon': 'earth-dragon.jpg',
            'Dragon of darkness': 'dragon-of-darkness.jpg',
            'Dragon of light': 'dragon-of-light.jpg',
            'King dragon': 'king-dragon.jpg',
        },
        'Palace of demon lord B': {
            'Demon guardian': 'demon-guardian.jpg',
            'Demon priest': 'demon-priest.jpg',
            'Demon hellspawn': 'demon-hellspawn.jpg',
            'Ancient demon': 'ancient-demon.jpg',
            'Demon of war': 'demon-of-war.jpg',
            'Demon guardian of Lord B Throne': 'demon-guardian-of-lord-b-throne.jpg',
            'DEMON LORD B': 'demon-lord-b.jpg',
        }

    }

    return render(request, 'enemy_detail.html', {
        'enemy': enemy,
        'enemy_health': enemy_health,
        'player_health': player_health,
        'location': location,
        'username': username,
        'enemy_images': enemy_images,
    })


@login_required
def attack_results(request, username, enemy_name):
    player = get_object_or_404(Player, username__username=username)
    enemy = get_object_or_404(Enemy, name=enemy_name)
    player_username = request.user.username

    attack_results = player.attack(enemy)
    location = enemy.location

    is_winner, enemy_experience, enemy_gold_pieces, player_damage_dealt, enemy_damage_dealt, level_up, player_health, enemy_health_remaining = attack_results

    enemy_images = {
        'Forest': {
            'Goblin': 'goblin.jpg',
            'Angry goblin': 'angry_goblin.jpg',
            'Hobgoblin': 'hobgoblin.jpg',
            'Wounded bear': 'wounded-bear.jpg',
            'Wolf': 'wolf.jpg',
            'Hobgoblin leader': 'hobgoblin-leader.jpg',
            'Ancient bear': 'ancient-bear.jpg',
        },
        'Evil forest': {
            'Undead goblin': 'undead-goblin.jpg',
            'Zombie': 'zombie.jpg',
            'Imp': 'imp.jpg',
            'Giant imp': 'giant-imp.jpg',
            'Ogre': 'ogre.jpg',
            'Witch': 'witch.jpg',
            'Lesser demon': 'lesser-demon.jpg'
        },
        'Cursed wastelands': {
            'Curse bearing imp': 'curse-bearing-imp.jpg',
            'Skeleton': 'skeleton.jpg',
            'Ancient witch': 'ancient-witch.jpg',
            'Angry survivor': 'angry-survivor.jpg',
            'Baby dragon': 'baby-dragon.jpg',
            'Mysterious stranger': 'mysterious-stranger.jpg',
            'Skeleton warrior': 'skeleton-warrior.jpg'
        },
        'Endless desert': {
            'Desert spider': 'desert-spider.jpg',
            'Lost wanderer': 'lost-wanderer.jpg',
            'Giant snake': 'giant-snake.jpg',
            'Shaman': 'shaman.jpg',
            'Genie': 'genie.jpg',
            'Giant scorpion': 'giant-scorpion.jpg',
            'Spirit of the desert': 'spirit-of-the-desert.jpg'
        },
        'Demon wastelands': {
            'Fire demon': 'fire-demon.jpg',
            'Water demon': 'water-demon.jpg',
            'Air demon': 'air-demon.jpg',
            'Earth demon': 'earth-demon.jpg',
            'Storm demon': 'storm-demon.jpg',
            'Elemental demon': 'elemental-demon.jpg',
            'Demon of the wastelands': 'demon-of-the-wastelands.jpg',
        },
        'Mountain of dragons': {
            'Fire dragon': 'fire-dragon.jpg',
            'Water dragon': 'water-dragon.jpg',
            'Air dragon': 'air-dragon.jpg',
            'Earth dragon': 'earth-dragon.jpg',
            'Dragon of darkness': 'dragon-of-darkness.jpg',
            'Dragon of light': 'dragon-of-light.jpg',
            'King dragon': 'king-dragon.jpg',
        },
        'Palace of demon lord B': {
            'Demon guardian': 'demon-guardian.jpg',
            'Demon priest': 'demon-priest.jpg',
            'Demon hellspawn': 'demon-hellspawn.jpg',
            'Ancient demon': 'ancient-demon.jpg',
            'Demon of war': 'demon-of-war.jpg',
            'Demon guardian of Lord B Throne': 'demon-guardian-of-lord-b-throne.jpg',
            'DEMON LORD B': 'demon-lord-b.jpg',
        }

    }

    context = {
        'player': player,
        'enemy': enemy,
        'player_username': player_username,
        'location': location,
        'is_winner': is_winner,
        'enemy_experience': enemy_experience,
        'enemy_gold_pieces': enemy_gold_pieces,
        'player_damage_dealt': player_damage_dealt,
        'enemy_damage_dealt': enemy_damage_dealt,
        'level_up': level_up,
        'player_health': player_health,
        'enemy_health_remaining': enemy_health_remaining,
        'enemy_images': enemy_images,

    }

    return render(request, 'attack_results.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:

                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:

                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


@login_required
def player_details(request, username):
    player = request.user.player
    username = player.username
    player_level = player.level
    player_health = player.health
    player_strength = player.strength
    player_defense = player.defense
    player_experience = player.experience
    player_gold = player.gold_pieces
    player_attribute_points = player.attribute_points
    player_experience_threshold = player.experience_threshold
    player_maximum_health = player.maximum_health

    return render(request, 'player_details.html', {
        'username': username,
        'player_level': player_level,
        'player_health': player_health,
        'player_strength': player_strength,
        'player_defense': player_defense,
        'player_experience': player_experience,
        'player_gold': player_gold,
        'player_attribute_points': player_attribute_points,
        'player_experience_threshold': player_experience_threshold,
        'player_maximum_health': player_maximum_health,

    })


@login_required
def allocate_points(request):
    if request.method == 'POST':
        player = request.user.player
        strength = int(request.POST.get('strength_points', 0))
        health = int(request.POST.get('health_points', 0))
        defense = int(request.POST.get('defense_points', 0))

        total_points = strength + health + defense

        if total_points <= player.attribute_points:
            player.strength += strength
            player.defense += defense
            player.maximum_health += health

            player.attribute_points -= total_points

            player.save()

        next_url = request.POST.get('next', '/')
        return redirect(next_url)
    else:
        return HttpResponse("Invalid request method")


@login_required
def inventory(request, username):
    player = request.user.player
    player_inventory = Inventory.objects.filter(player=player)

    return render(request, 'inventory.html', {
        'username': username,
        'player': player,
        'player_inventory': player_inventory,

    })


@login_required
def healing_items(request):
    player = request.user.player

    try:
        items = Inventory.objects.filter(player=player, item__item_type='Healing item')
    except Inventory.DoesNotExist:
        items = []

    return render(request, 'healing_items.html', {
        'items': items,
        'player': player,
        'player_username': request.user.username,
    })


@login_required
def use_item(request, item_id):
    try:
        inventory_item = Inventory.objects.get(pk=item_id)
        player = request.user.player
        inventory_item.use_item(player)
    except Inventory.DoesNotExist:
        return redirect('healing_items')

    return redirect('healing_items')


@login_required
def buy_item(request, username, item_name, city_location_name):
    if request.method == 'POST':
        player = get_object_or_404(Player, username__username=username)
        inventory = get_object_or_404(Inventory, player=player, item__item_name=item_name)
        buy_quantity = int(request.POST.get('buy_quantity', 0))
        if buy_quantity > 0:
            total_price = inventory.item.item_buy_price * buy_quantity
            if player.gold_pieces >= total_price:
                inventory.increase_quantity(buy_quantity)
                player.gold_pieces -= total_price
                player.save()
            else:
                pass
            return redirect('city_location_detail', location_name=city_location_name)
    return HttpResponse("Invalid request")


@login_required
def sell_item(request, username, item_name, city_location_name):
    if request.method == 'POST':
        player = get_object_or_404(Player, username__username=username)
        inventory = get_object_or_404(Inventory, player=player, item__item_name=item_name)
        sell_quantity = int(request.POST.get('sell_quantity', 0))
        if sell_quantity > 0 and inventory.quantity >= sell_quantity:
            total_price = inventory.item.item_sell_price * sell_quantity
            inventory.decrease_quantity(sell_quantity)
            player.gold_pieces += total_price
            player.save()
            return redirect('city_location_detail', location_name=city_location_name)
    return HttpResponse("Invalid request")


@login_required
def use_item(request, item_id):
    try:
        inventory_item = Inventory.objects.get(pk=item_id)
        player = request.user.player
        inventory_item.use_item(player)
    except Inventory.DoesNotExist:
        return redirect('healing_items')

    return redirect('healing_items')


@login_required
def equip_item(request, item_id, action):
    try:
        inventory_item = Inventory.objects.get(pk=item_id)
        player = request.user.player
        if action == 'equip':
            inventory_item.equip_item(player)
        elif action == 'unequip':
            inventory_item.unequip_item(player)
    except Inventory.DoesNotExist:
        return redirect('inventory')

    return redirect('items_by_type', item_type=inventory_item.item.item_type.capitalize())


@login_required
def items_by_type(request, item_type):
    player = request.user.player

    try:
        items = Inventory.objects.filter(player=player, item__item_type=item_type.capitalize())
    except Inventory.DoesNotExist:
        items = []

    template_name = item_type.lower() + '.html'

    return render(request, template_name, {'items': items, 'player_username': request.user.username})


@login_required
def totem_detail(request, totem_name):
    player = request.user.player
    totem = Totem.objects.get(player=player, totem_name=totem_name)

    if request.method == 'POST':
        if request.POST.get('action') == 'pray':
            totem.pray(player)

    player_maximum_health = player.maximum_health
    player_strength = player.strength
    player_defense = player.defense

    context = {
        'player': player,
        'totem': totem,
        'player_defense': player_defense,
        'player_maximum_health': player_maximum_health,
        'player_strength': player_strength,
    }

    return render(request, 'totem_detail.html', context)


@login_required
def elder_detail(request):
    player = request.user.player
    elder = player.wise_elder

    if request.method == 'POST':
        if request.POST.get('action') == 'pray':
            elder.pay(player)
            elder.save()

    elder_name = elder.name
    knowledge_price = elder.knowledge_price
    knowledge_acquired = elder.knowledge_acquired
    knowledge_message = elder.knowledge_messages[elder.variable] if elder.variable < len(
        elder.knowledge_messages) else None

    player_gold_pieces = player.gold_pieces

    unlocked_knowledge_messages = []
    for i in range(1, elder.variable + 1):
        unlocked_knowledge_messages.append(elder.knowledge_messages[i - 1])

    all_knowledge_acquired = elder.variable >= 8

    context = {
        'elder_name': elder_name,
        'knowledge_price': knowledge_price,
        'knowledge_acquired': knowledge_acquired,
        'knowledge_message': knowledge_message,
        'player_gold_pieces': player_gold_pieces,
        'unlocked_knowledge_messages': unlocked_knowledge_messages,
        'all_knowledge_acquired': all_knowledge_acquired,
    }

    return render(request, 'elder_detail.html', context)


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def frequent_questions(request):
    return render(request, 'frequent_questions.html')


@login_required
def highscores(request):
    players = Player.objects.order_by('-level')
    return render(request, 'highscores.html', {'players': players})
