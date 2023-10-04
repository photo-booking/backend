# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.authtoken.models import Token

from users.models import User

from .models import Chat


def order_chat_room(request, order_id):
    # token = request.headers["Authorization"].split(" ")[1]
    try:
        #        token = "34b08f70efc45c0d36ec10248167521def93d05a"
        token = request.headers["Authorization"].split(" ")[
            1
        ]  # Получаем токен

        user = get_object_or_404(
            Token, key=token
        ).user  # Получаем пользователя по токену
        try:
            order = user.orders.get(pk=order_id)  # ищем заказ
        except Exception:
            return HttpResponseNotFound(content="Чат не найден")
        print(order.chat_id)
    except Exception:
        return HttpResponseForbidden(
            content="Пользователь не найден, передайте токен"
        )
    return render(request, 'chat/room.html', {'order': order})


def index(request):
    users = User.objects.all()
    if request.method == "POST":
        userpk = request.POST.get("user_pk", None)
        current_users = User.objects.get(pk=userpk)
        if current_users:
            if Chat.objects.filter(
                host=request.user, current_users=current_users
            ).exists():
                room = Chat.objects.get(
                    host=request.user, current_users=current_users
                )
                return redirect('chat:room', room.pk)
            else:
                room = Chat.objects.create(
                    host=request.user, name=(current_users.pk, request.user.pk)
                )
                room.current_users.add(current_users)
                return redirect('chat:room', room.pk)
    return render(request, 'chat/index.html', {'users': users})


def room(request, pk):
    room: Chat = get_object_or_404(Chat, pk=pk)
    return render(
        request,
        'chat/room.html',
        {
            "room": room,
        },
    )


def test(request):
    # token = create_token(1)
    # print(token)
    return render(request, 'chat/test.html')
