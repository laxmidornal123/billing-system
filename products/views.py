from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Product
from .forms import ProductForm


def product_list(request):

    products = Product.objects.all()

    search = request.GET.get('search')

    if search:

        products = products.filter(
            name__icontains=search
        )

    return render(
        request,
        'products/product_list.html',
        {
            'products': products
        }
    )
def add_product(request):

    form = ProductForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            'product_list'
        )

    return render(
        request,
        'products/add_product.html',
        {
            'form': form
        }
    )


def edit_product(request,id):

    product = get_object_or_404(
        Product,
        id=id
    )

    form = ProductForm(
        request.POST or None,
        instance=product
    )

    if form.is_valid():

        form.save()

        return redirect(
            'product_list'
        )

    return render(
        request,
        'products/edit_product.html',
        {
            'form': form
        }
    )


def delete_product(request,id):

    product = get_object_or_404(
        Product,
        id=id
    )

    product.delete()

    return redirect(
        'product_list'
    )