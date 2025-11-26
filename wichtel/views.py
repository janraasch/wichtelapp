from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Event, Wishlist


@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user,
        defaults={'text': ''}
    )
    if request.method == 'POST':
        wishlist.text = request.POST.get('text', '')
        wishlist.save()
        Event.objects.create(user=request.user, name='wishlist.saved')
        messages.success(request, 'Wunschliste gespeichert!')
        return redirect('wichtel:wishlist')
    Event.objects.create(user=request.user, name='wishlist.viewed')
    return render(request, 'wichtel/wishlist.html', {'wishlist': wishlist})
