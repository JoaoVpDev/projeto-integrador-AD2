from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

# Lista simulada de itens (sem banco de dados)
ITENS_FAKE = [
    {
        "id": 1,
        "nome": "Tigre",
        "especime": "Panthera tigris",
        "data_coleta": "2023-10-05",
    },
    {
        "id": 2,
        "nome": "Pinguim",
        "especime": "Aptenodytes forsteri",
        "data_coleta": "2024-01-15",
    },
]


# Página inicial
def home(request):
    return render(request, "home.html")


# Login do usuário
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuário ou senha incorretos")

    return render(request, "registration/login.html")


# Logout do usuário
def logout(request):
    auth_logout(request)
    return redirect("login")


# Página de perfil do usuário
def perfil_view(request):
    return render(request, "perfil.html")


# Listar itens
def listar_itens(request):
    return render(request, "listar_itens.html", {"itens": ITENS_FAKE})


# Adicionar novo item
def adicionar_item(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        especime = request.POST.get("especime")
        data_coleta = request.POST.get("data_coleta")

        if nome and especime and data_coleta:
            novo_id = max(item["id"] for item in ITENS_FAKE) + 1 if ITENS_FAKE else 1
            ITENS_FAKE.append(
                {
                    "id": novo_id,
                    "nome": nome,
                    "especime": especime,
                    "data_coleta": data_coleta,
                }
            )
            return redirect("listar_itens")

    return render(request, "adicionar_item.html")


# Editar item existente
def editar_item(request, id):
    global ITENS_FAKE
    item = next((i for i in ITENS_FAKE if i["id"] == id), None)
    if not item:
        return HttpResponse("Item não encontrado", status=404)

    if request.method == "POST":
        item["nome"] = request.POST.get("nome")
        item["especime"] = request.POST.get("especime")
        item["data_coleta"] = request.POST.get("data_coleta")
        return redirect("listar_itens")

    return render(request, "editar_item_modal.html", {"item": item})


# Excluir item
def excluir_item(request, id):
    global ITENS_FAKE
    if request.method == "POST":
        ITENS_FAKE = [item for item in ITENS_FAKE if item["id"] != id]
        return redirect("listar_itens")
    return HttpResponse("Método não permitido", status=405)
