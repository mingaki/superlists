from django.shortcuts import redirect, render

from .models import Item, List


def home_page(request):
    return render(request, "home.html")


def view_list(request, list_id):
    items = Item.objects.filter(list__id=list_id)
    return render(request, "list.html", {"items": items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")
