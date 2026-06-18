from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from .forms import CustomerForm


def customer_list(request):

    customers = Customer.objects.all()

    search = request.GET.get('search')

    if search:
        customers = customers.filter(
            name__icontains=search
        )

    return render(
        request,
        'customers/customer_list.html',
        {
            'customers': customers
        }
    )


def add_customer(request):

    form = CustomerForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            'customer_list'
        )

    return render(
        request,
        'customers/add_customer.html',
        {
            'form': form
        }
    )


def edit_customer(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    form = CustomerForm(
        request.POST or None,
        instance=customer
    )

    if form.is_valid():

        form.save()

        return redirect(
            'customer_list'
        )

    return render(
        request,
        'customers/edit_customer.html',
        {
            'form': form
        }
    )
def customer_list(request):

    customers = Customer.objects.all()

    search = request.GET.get('search')

    if search:

        customers = customers.filter(
            name__icontains=search
        )

    return render(
        request,
        'customers/customer_list.html',
        {
            'customers': customers
        }
    )

def delete_customer(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    customer.delete()

    return redirect(
        'customer_list'
    )
    