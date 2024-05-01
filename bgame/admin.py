from django.contrib import admin
from .models import Player, Items, Location, Enemy, CityLocation, Inventory, Totem, WiseElder

admin.site.register(Player)
admin.site.register(Items)
admin.site.register(Enemy)
admin.site.register(Location)
admin.site.register(CityLocation)
admin.site.register(Inventory)
admin.site.register(Totem)
admin.site.register(WiseElder)
