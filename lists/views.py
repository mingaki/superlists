from django.shortcuts import redirect, render

from .models import Item


def home_page(request):
    if request.method == "POST":
        text = request.POST.get("item_text", "")
        Item.objects.create(text=text)
        return redirect("/lists/the-only-list-in-the-world/")

    return render(request, "home.html")


def view_list(request):
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})
