from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect("articles:article_list")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Регистрация прошла успешно. Войдите в аккаунт.")
        return redirect("articles:article_list")
    return render(request, "users/register.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_panel_view(request):
    users = User.objects.all().order_by("-date_joined")
    return render(request, "users/admin_panel.html", {"users": users})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def toggle_ban_view(request, user_id: int):
    if request.method != "POST":
        return redirect("users:admin_panel")
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        messages.error(request, "Нельзя заблокировать самого себя.")
        return redirect("users:admin_panel")
    if target.is_superuser and not request.user.is_superuser:
        messages.error(request, "Нельзя заблокировать супер админа.")
        return redirect("users:admin_panel")
    target.is_banned = not target.is_banned
    target.save(update_fields=["is_banned"])
    action = "заблокирован" if target.is_banned else "разблокирован"
    messages.success(request, f"Пользователь {target.username} {action}.")
    return redirect("users:admin_panel")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def make_admin_view(request, user_id: int):
    if request.method != "POST":
        return redirect("users:admin_panel")
    target = get_object_or_404(User, pk=user_id)
    if target.is_superuser:
        messages.error(request, "Нельзя изменять права супер админа.")
        return redirect("users:admin_panel")
    
    if target.is_staff:
        target.is_staff = False
        messages.success(request, f"Пользователь {target.username} лишен прав админа.")
    else:
        target.is_staff = True
        messages.success(request, f"Пользователь {target.username} назначен админом.")
    
    target.save(update_fields=["is_staff"])
    return redirect("users:admin_panel")
