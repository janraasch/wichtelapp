from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Event, UserDrawing, Wishlist


@login_required
def home(request):
    current_year = datetime.now().year
    user_drawing = UserDrawing.objects.filter(giver=request.user, drawing__year=current_year).first()
    if user_drawing:
        return _giftlist(user_drawing.receiver.wishlist, request)
    return _wishlist(request)

def _wishlist(request):
    wishlist = Wishlist.objects.get_or_create(user=request.user, defaults={"text": ""})[0]
    if request.method == "POST":
        wishlist.text = request.POST.get("text", "")
        wishlist.save()
        Event.objects.create(user=request.user, name="wishlist.saved")
        messages.success(request, "Wunschliste gespeichert!")
        return redirect("wichtel:home")
    Event.objects.create(user=request.user, name="wishlist.viewed")
    return render(request, "wichtel/wishlist.html", {"wishlist": wishlist})

def _giftlist(giftlist, request):
    Event.objects.create(user=request.user, name="giftlist.viewed")
    profile = giftlist.user.profile
    return render(request, "wichtel/giftlist.html", {
        "giftlist": giftlist,
        "code_name": profile.code_name,
        "address": profile.address,
    })
