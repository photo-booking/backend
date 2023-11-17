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
    except Exception:
        return HttpResponseForbidden(
            content="Пользователь не найден, передайте токен"
        )
    return render(request, 'chat/room.html', {'order': order})


def index(request):
    users = User.objects.all()
    token = request.headers.get('Authorization').split(" ")[1]
    user = get_object_or_404(Token, key=token).user
    if request.method == "POST":
        userpk = request.POST.get("user_pk", None)
        current_users = User.objects.get(pk=userpk)
        if current_users:
            if Chat.objects.filter(
                host=user.pk, current_users=current_users
            ).exists():
                room = Chat.objects.get(
                    host=user.pk, current_users=current_users
                )
                return redirect('chat:room', room.pk)
            elif Chat.objects.filter(
                host=current_users, current_users=user.pk
            ).exists():
                print(777)
                room = Chat.objects.get(
                    host=current_users, current_users=user.pk
                )
                print(888)
                print(print(room))
                return redirect('chat:room', room.pk)
            else:
                room = Chat.objects.create(
                    host=user, name=(current_users.pk, user.pk)
                )
                room.current_users.add(current_users)
                return redirect('chat:room', room.pk)
    return render(
        request,
        'chat/index.html',
        {
            'users': users,
        },
    )


def room(request, pk):
    room: Chat = get_object_or_404(Chat, pk=pk)
    return render(
        request,
        'chat/room.html',
        {
            "user": room.host,
            "room": room,
            "current_user": room.current_users.all()[0],
        },
    )


def test(request):
    # token = create_token(1)
    # print(token)
    return render(request, 'chat/test.html')
