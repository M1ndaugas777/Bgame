from django.urls import path
from . import views

urlpatterns = [
    # Main urls
    path('', views.index, name='bgame'),
    path('main/', views.main, name='main'),
    # Urls for locations
    path('location/<str:location_name>/', views.location_detail, name='location_detail'),
    path('city_location/<str:location_name>/', views.city_location_detail, name='city_location_detail'),
    # Urls for enemies and combat
    path('enemy/<str:enemy_name>/<str:username>/', views.enemy_detail, name='enemy_detail'),
    path('attack_results/<str:username>/<str:enemy_name>/', views.attack_results, name='attack_results'),
    # Registration
    path('register/', views.register, name='register'),
    # Player info urls
    path('player_details/<str:username>', views.player_details, name='player_details'),
    path('allocate-points/', views.allocate_points, name='allocate_points'),
    path('inventory/<str:username>/', views.inventory, name='inventory'),
    # Urls for items
    path('items/<str:item_type>/', views.items_by_type, name='items_by_type'),
    path('healing_items/', views.healing_items, name='healing_items'),
    path('use_item/<int:item_id>/', views.use_item, name='use_item'),
    path('buy/<str:username>/<str:item_name>/<str:city_location_name>/', views.buy_item, name='buy_item'),
    path('sell/<str:username>/<str:item_name>/<str:city_location_name>/', views.sell_item, name='sell_item'),
    path('equip/<int:item_id>/', views.equip_item, {'action': 'equip'}, name='equip_item'),
    path('unequip/<int:item_id>/', views.equip_item, {'action': 'unequip'}, name='unequip_item'),
    # Urls for elder and totems
    path('totem/<str:totem_name>/', views.totem_detail, name='totem_detail'),
    path('elder/', views.elder_detail, name='elder_detail'),
    # Other urls
    path('about/', views.about, name='about'),
    path('frequent_questions/', views.frequent_questions, name='frequent_questions'),
    path('highscores/', views.highscores, name='highscores'),
]


