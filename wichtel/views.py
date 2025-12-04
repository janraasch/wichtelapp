from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Event, UserDrawing, Wishlist


@login_required
def home(request):
    current_year = datetime.now().year
    user_drawing = UserDrawing.objects.filter(giver=request.user, drawing__year=current_year).first()
    if user_drawing and user_drawing.receiver.wishlist and user_drawing.receiver.wishlist.text:
        return giftlist(user_drawing.receiver.wishlist, request)
    return wishlist(request)


def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, defaults={"text": ""})
    if request.method == "POST":
        wishlist.text = request.POST.get("text", "")
        wishlist.save()
        Event.objects.create(user=request.user, name="wishlist.saved")
        messages.success(request, "Wunschliste gespeichert!")
        return redirect("wichtel:wishlist")
    Event.objects.create(user=request.user, name="wishlist.viewed")
    return render(request, "wichtel/wishlist.html", {"wishlist": wishlist})


def giftlist(giftlist, request):
    address = giftlist.user.profile.address
    return render(request, "wichtel/giftlist.html", {"giftlist": giftlist, "address": address})
