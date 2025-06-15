from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("listar/", views.listar_itens, name="listar_itens"),
    path("editar/<int:item_id>/", views.editar_item, name="editar_item"),
    path("adicionar/", views.adicionar_item, name="adicionar_item"),
    path("excluir/<int:item_id>/", views.excluir_item, name="excluir_item"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("perfil/", views.perfil_view, name="perfil"),
]
