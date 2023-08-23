# from asgiref.sync import sync_to_async
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Room

# from django.views.generic import TemplateView

# from .tokenizator import create_token


def index(request):
    if request.method == "POST":
        name = request.POST.get("name", None)
        if name:
            room = Room.objects.create(name=name, host=request.user)
            print(room.pk)
            return HttpResponseRedirect(
                reverse("room", kwargs={"pk": room.pk})
            )
    # token = create_token(1)
    # print(token)
    return render(request, 'chat/index.html')


def room(request, pk):
    room: Room = get_object_or_404(Room, pk=pk)
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
