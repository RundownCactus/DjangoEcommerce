from django.shortcuts import render, get_object_or_404
from django.db.models.query import QuerySet
from .models import Item, Order, OrderItem, OrderUpdate
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def Tracker(request):
    return render(request, "Tracker.html")


def product(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product.html", context)


def checkout(request):
    context = {
        'items': Item.objects.all()
    }
    if request.method == "POST":
        update = OrderUpdate(order_id=Order.order_id, update_desc="")
    return render(request, "checkout-page.html")


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"


class SearchHomeView(ListView):
    model = Item.objects.filter()
    paginate_by = 10
    template_name = "home-page.html"


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You Do Not Have An Active Order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def home(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home-page.html", context)


def search(request):
    query = request.GET.get('search')
    context = {
        # filter(title=query)
        'items': Item.objects.filter(title__icontains=query)
    }
    return render(request, "Search-page.html", context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The item quanitity was updated.")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)

    else:
        ord_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ord_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            messages.info(request, "This item was removed to your cart.")
            order.items.remove(order_item)
            return redirect("core:product", slug=slug)

        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "No Active Order.")
        return redirect("core:products", slug=slug)
    return redirect("core:products", slug=slug)
