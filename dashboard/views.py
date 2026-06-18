from django.shortcuts import render
from django.db.models import Sum

from products.models import Product
from customers.models import Customer
from billing.models import Invoice, InvoiceItem

def dashboard(request):

    total_products = Product.objects.count()

    total_customers = Customer.objects.count()

    total_invoices = Invoice.objects.count()

    total_sales = sum(
        invoice.total
        for invoice in Invoice.objects.all()
    )

    total_bills = Invoice.objects.count()

    recent_invoices = Invoice.objects.order_by(
        '-created_at'
    )[:3]

    low_stock_products = Product.objects.filter(
        stock__lt=5
    )

    sales_labels = []
    sales_data = []
    pie_labels = sales_labels
    pie_data = sales_data
    items = (
        InvoiceItem.objects
        .values('product__name')
        .annotate(total_qty=Sum('quantity'))
    )

    for item in items:

        sales_labels.append(
            item['product__name']
        )

        sales_data.append(
            item['total_qty']
        )
        top_product = "N/A"

        if sales_data:

            max_qty = max(sales_data)

            index = sales_data.index(max_qty)

            top_product = sales_labels[index]
            low_stock_count = Product.objects.filter(
    stock__lt=5
).count()
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_invoices': total_invoices,
        'total_sales': total_sales,
        'low_stock_products': low_stock_products,
        'sales_labels': sales_labels,
        'sales_data': sales_data,
        'total_bills': total_bills,
        'recent_invoices': recent_invoices,
        'top_product': top_product,
        'pie_labels': pie_labels,
'pie_data': pie_data,
    }
    
    print("Labels =", sales_labels)
    print("Data =", sales_data)

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )
