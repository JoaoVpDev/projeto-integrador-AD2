from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Item
from .forms import ItemForm


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
    return render(
        request,
        "zooapp/perfil.html",
        {"user": request.user, "permissions": request.user.get_all_permissions()},
    )


# Listar itens
@login_required
@login_required
def listar_itens(request):
    itens = Item.objects.all().order_by("nome")  # Adicionado ordenação padrão
    return render(
        request,
        "zooapp/listar_itens.html",
        {"itens": itens, "can_add": request.user.has_perm("zooapp.add_item")},
    )


# Adicionar novo item
@login_required
@permission_required("zooapp.add_item", raise_exception=True)
def adicionar_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            novo_item = form.save()
            messages.success(
                request, f"Item '{novo_item.nome}' adicionado com sucesso!"
            )
            return redirect("listar_itens")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = ItemForm()

    return render(
        request, "zooapp/adicionar_item.html", {"form": form, "action": "Adicionar"}
    )


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
def excluir_item(
    request, item_id
):  # Mude de 'id' para 'item_id' para manter consistência
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        item.delete()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        return redirect("listar_itens")

    return render(request, "zooapp/confirmar_exclusao.html", {"item": item})
