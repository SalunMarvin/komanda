from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Category, Product, Ticket, Quantity
from rest_framework.response import Response
from .forms import AddTicketForm
from .serializers import ProductSerializer
from rest_framework import viewsets, permissions, generics
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import django_filters


@login_required(login_url='/admin/login/')
def index(request):
    tickets = Ticket.objects.all().order_by('number').filter(isFinished=False)

    context = {'tickets': tickets, }

    return render(request, 'index.html', context)


@login_required(login_url='/admin/login/')
def add(request):
    if request.method == 'POST':
        form = AddTicketForm(request.POST)

        if form.is_valid():
            ticketFromDB = Ticket.objects.filter(slug=slugify(form.cleaned_data['ticket_name'])).exists()
            if ticketFromDB:
                return HttpResponseRedirect('/invalid/ticket/')
            else:
                ticket = Ticket(
                    name=form.cleaned_data['ticket_name'], number=form.cleaned_data['ticket_number'])
                ticket.save()
            return HttpResponseRedirect('/ticket/' + str(ticket.slug))

    tickets = Ticket.objects.all().order_by('number').filter(isFinished=False)

    context = {'tickets': tickets,
               'form': AddTicketForm()}

    return render(request, 'add.html', context)


@login_required(login_url='/admin/login/')
def get_ticket_by_slug(request, slug):
    ticket = Ticket.objects.filter(slug=slug)[0]

    leftToPay = (ticket.finalPrice or 0)

    context = {'ticket': ticket,
               'leftToPay': leftToPay}

    return render(request, "ticket.html", context)


@login_required(login_url='/admin/login/')
def add_product_to_ticket(request, ticket, product):
    product = Product.objects.filter(id=product)[0]

    ticket = Ticket.objects.filter(slug=ticket)[0]

    if Quantity.objects.filter(ticket=ticket, product=product).exists():
        quantity = Quantity.objects.filter(ticket=ticket, product=product)[0]
        quantity.quantity += 1
        quantity.save()
    else:
        quantity = Quantity.objects.create(ticket=ticket, product=product, quantity=1)
        quantity.save()

    ticket.finalPrice = (ticket.finalPrice or 0) + product.price

    ticket.save()

    context = {'ticket': ticket}

    return HttpResponseRedirect('/ticket/' + str(ticket.slug))


@login_required(login_url='/admin/login/')
def remove_product_from_ticket(request, ticket, product):
    product = Product.objects.filter(id=product)[0]

    ticket = Ticket.objects.filter(slug=ticket)[0]

    if Quantity.objects.filter(ticket=ticket, product=product).exists():
        quantity = Quantity.objects.filter(ticket=ticket, product=product)[0]
        if quantity.quantity > 1:
            quantity.quantity -= 1
            quantity.save()
        else:
            quantity.delete()    

    ticket.finalPrice = (ticket.finalPrice or 0) - (product.price or 0)

    ticket.save()

    context = {'ticket': ticket}

    return HttpResponseRedirect('/ticket/' + str(ticket.slug))


@login_required(login_url='/admin/login/')
def pay_product_from_ticket(request, ticket, product):
    product = Product.objects.filter(id=product)[0]

    ticket = Ticket.objects.filter(slug=ticket)[0]

    ticket.finalPrice = (ticket.finalPrice or 0) - (Decimal(product.price) or 0)
    ticket.partialPaid = (ticket.partialPaid or 0) + product.price

    ticket.save()

    context = {'ticket': ticket}

    return HttpResponseRedirect('/ticket/' + str(ticket.slug))


@login_required(login_url='/admin/login/')
def close_ticket_by_slug(request, slug):
    ticket = Ticket.objects.filter(slug=slug)[0]

    ticket.delete()

    return HttpResponseRedirect('/')


@login_required(login_url='/admin/login/')
def add_product_without_price_to_ticket(request, ticket, product, price):
    product = Product.objects.filter(id=product)[0]

    ticket = Ticket.objects.filter(slug=ticket)[0]

    if Quantity.objects.filter(ticket=ticket, product=product).exists():
        quantity = Quantity.objects.filter(ticket=ticket, product=product)[0]
        quantity.quantity += 1
        quantity.save()
    else:
        quantity = Quantity.objects.create(ticket=ticket, product=product, quantity=1)
        quantity.save()
    
    ticket.finalPrice = (ticket.finalPrice or 0) + (Decimal(price) or 0)

    ticket.save()

    context = {'ticket': ticket}

    return HttpResponseRedirect('/ticket/' + str(ticket.slug))


@login_required(login_url='/admin/login/')
def give_discount_to_ticket(request, ticket, price):
    ticket = Ticket.objects.filter(slug=ticket)[0]

    ticket.finalPrice = (ticket.finalPrice or 0) - (Decimal(price) or 0)

    ticket.save()

    context = {'ticket': ticket}

    return HttpResponseRedirect('/ticket/' + str(ticket.slug))


def show_invalid_page(request):
    return render(request, 'invalid.html')


def get_ticket_by_slug_to_user(request, slug):
    ticket = Ticket.objects.filter(slug=slug)[0]

    leftToPay = (ticket.finalPrice or 0)

    context = {'ticket': ticket,
               'leftToPay': leftToPay}

    return render(request, "user.html", context)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data, "status": "Produtos encontrados com sucesso"})


class ProductSearch(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_name = self.kwargs['name']
        return Product.objects.filter(name__icontains=product_name)