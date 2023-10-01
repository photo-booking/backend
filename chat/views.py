# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken.models import Token

# from django.shortcuts import render
# from users.models import User


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
