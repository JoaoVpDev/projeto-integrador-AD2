from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("listar/", views.listar_itens, name="listar_itens"),
    path("editar/<int:id>/", views.editar_item, name="editar_item"),
    path("adicionar/", views.adicionar_item, name="adicionar_item"),
    path("excluir/<int:id>/", views.excluir_item, name="excluir_item"),
    path("login/", views.custom_login, name="login"),  # Alterado para usar sua view
    path("logout/", views.custom_logout, name="logout"),
    path("perfil/", views.perfil_view, name="perfil"),
]
