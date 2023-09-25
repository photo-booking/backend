# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# from django.shortcuts import get_object_or_404, render
from django.shortcuts import render


def order_chat_room(request, order_id):
    try:
        # извлечь заказ с заданным id, к которому
        # присоединился текущий пользователь
        print(22222)
        print(request.user)
        print(request.user.orders.all())

        order = request.user.orders.get(id=order_id)
    except Exception:
        # пользователь не является студентом курса либо
        # курс не существует
        print(1111)
        print(request.user)
        return HttpResponseForbidden()
    return render(request, 'chat/room.html', {'order': order})
