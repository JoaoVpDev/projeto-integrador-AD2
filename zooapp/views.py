from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Item
from .forms import ItemForm

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
@login_required
def home(request):
    return render(request, "home.html")


# Login do usuário
def custom_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            next_url = request.POST.get("next", "home")

            # Validação segura da URL de redirecionamento
            if not url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                next_url = "home"

            return redirect(next_url)
        else:
            messages.error(request, "Credenciais inválidas")

    return render(
        request, "registration/login.html", {"next": request.GET.get("next", "")}
    )


# Logout do usuário
def custom_logout(request):
    auth_logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect("login")


# Página de perfil do usuário
def perfil_view(request):
    return render(request, "perfil.html")


# Listar itens
@login_required
def listar_itens(request):
    return render(request, "listar_itens.html", {"itens": ITENS_FAKE})


# Adicionar novo item
@login_required
@permission_required("zooapp.add_item", raise_exception=True)
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
@login_required
@permission_required("zooapp.change_item", raise_exception=True)
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
@login_required
@permission_required("zooapp.delete_item", raise_exception=True)
def excluir_item(request, id):
    global ITENS_FAKE
    if request.method == "POST":
        ITENS_FAKE = [item for item in ITENS_FAKE if item["id"] != id]
        return redirect("listar_itens")
    return HttpResponse("Método não permitido", status=405)
