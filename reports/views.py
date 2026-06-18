from django.shortcuts import render
from billing.models import Invoice

def reports(request):

    invoices = Invoice.objects.all()

    total_sales = sum(
        invoice.total
        for invoice in invoices
    )

    total_invoices = invoices.count()

    sales_labels = []
    sales_data = []

    for invoice in invoices:

        item = invoice.invoiceitem_set.first()

        if item:

            sales_labels.append(
                item.product.name
        )

        sales_data.append(
            float(invoice.total)
        )
    context = {

        'invoices': invoices,

        'total_sales': total_sales,

        'total_invoices': total_invoices,

        'sales_labels': sales_labels,

        'sales_data': sales_data

    }
    return render(
        request,
        'reports/reports.html',
        context
    )