from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('index', views.index, name='index'),
    path('ping/', views.ping, name='ping'),
    path('ospf/neighboors/', views.show_ospf, name='ospf_neighboors'),
    path('ospf/set/', views.set_ospf, name='set_ospf'),
    path('ospf/remove/', views.remove_ospf, name='remove_ospf'),
    path('rip/database/', views.show_rip, name='rip_database'),
    path('rip/set/', views.set_rip, name='set_rip'),
    path('rip/remove/', views.remove_rip, name='remove_rip'),
    path('routing/pc/', views.show_pc_routes, name='pc_route_table'),
    path('routing/router/', views.show_router_routes, name='router_route_table'),
    path('setip/pc/',views.set_ip_pc,name="set_ip_for_pc"),
    path('setip/router/',views.set_ip_router,name="set_ip_for_router"),
    path('dhcp/set/',views.set_dhcp,name="set_dhcp"),
    path('dhcp/binding/',views.get_dhcp_binding,name="get_dhcp_binding"),
    path('dhcp/remove/',views.remove_dhcp,name="remove_dhcp"),
]