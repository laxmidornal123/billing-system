from django.shortcuts import render
from django.shortcuts import redirect
from decimal import Decimal
from customers.models import Customer
from products.models import Product

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Invoice, InvoiceItem
import random

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from django.db.models import Q
from .models import Invoice, InvoiceItem

def invoice_list(request):

    invoices = Invoice.objects.all()

    search = request.GET.get('search')
    date = request.GET.get('date')

    if search:

        invoices = invoices.filter(
            Q(invoice_no__icontains=search) |
            Q(customer__name__icontains=search)
        )

    if date:

        invoices = invoices.filter(
            created_at__date=date
        )

    return render(
        request,
        'billing/invoice_list.html',
        {
            'invoices': invoices
        }
    )
def create_invoice(request):

    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == "POST":

        customer_id = request.POST.get("customer")
        product_id = request.POST.get("product")
        quantity = int(request.POST.get("quantity"))

        customer = Customer.objects.get(id=customer_id)
        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity
        gst = subtotal * Decimal('0.18')
        total = subtotal + gst

        invoice = Invoice.objects.create(
            invoice_no=f"INV{random.randint(1000,9999)}",
            customer=customer,
            subtotal=subtotal,
            gst=gst,
            total=total
        )

        InvoiceItem.objects.create(
            invoice=invoice,
            product=product,
            quantity=quantity,
            price=product.price,
            total=subtotal
        )

        product.stock -= quantity
        product.save()

        return redirect("invoice_list")

    return render(
        request,
        "billing/create_invoice.html",
        {
            "customers": customers,
            "products": products
        }
    )
def download_invoice(request, id):

    invoice = Invoice.objects.get(id=id)

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="{invoice.invoice_no}.pdf"'
    )

    p = canvas.Canvas(
        response,
        pagesize=A4
    )

    width, height = A4

    # Header
    p.setFillColor(colors.darkblue)
    p.rect(
        0,
        height - 80,
        width,
        80,
        fill=1
    )

    p.setFillColor(colors.white)

    p.setFont(
        "Helvetica-Bold",
        24
    )

    p.drawString(
        50,
        height - 50,
        "BILLING PRO"
    )

    # Invoice Title
    p.setFillColor(colors.black)

    p.setFont(
        "Helvetica-Bold",
        18
    )

    p.drawString(
        50,
        height - 120,
        "INVOICE"
    )

    p.setFont(
        "Helvetica",
        12
    )

    p.drawString(
        50,
        height - 160,
        f"Invoice No: {invoice.invoice_no}"
    )

    p.drawString(
        50,
        height - 185,
        f"Customer: {invoice.customer.name}"
    )

    p.drawString(
        50,
        height - 210,
        f"Date: {invoice.created_at.strftime('%d-%m-%Y')}"
    )

    p.drawString(
        50,
        height - 260,
        f"Subtotal: Rs. {invoice.subtotal}"
    )

    p.drawString(
        50,
        height - 290,
        f"GST (18%): Rs. {invoice.gst}"
    )

    p.setFont(
        "Helvetica-Bold",
        14
    )

    p.drawString(
        50,
        height - 330,
        f"Grand Total: Rs. {invoice.total}"
    )

    # Footer
    p.setFont(
        "Helvetica",
        10
    )

    p.drawString(
        50,
        50,
        "Thank you for shopping with Billing Pro"
    )

    p.save()

    return response
def print_invoice(request, id):

    invoice = Invoice.objects.get(
        id=id
    )

    return render(
        request,
        'billing/print_invoice.html',
        {
            'invoice': invoice
        }
    )
def export_invoices(request):

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Invoices"

    sheet.append([
        "Invoice No",
        "Customer",
        "Subtotal",
        "GST",
        "Total",
        "Date"
    ])

    invoices = Invoice.objects.all()

    for invoice in invoices:

        sheet.append([
            invoice.invoice_no,
            invoice.customer.name,
            float(invoice.subtotal),
            float(invoice.gst),
            float(invoice.total),
            invoice.created_at.strftime('%d-%m-%Y')
        ])

    response = HttpResponse(
        content_type=
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=invoices.xlsx'

    workbook.save(response)

    return response

def invoice_detail(request, id):

    invoice = Invoice.objects.get(id=id)

    items = InvoiceItem.objects.filter(
        invoice=invoice
    )

    return render(
        request,
        'billing/invoice_detail.html',
        {
            'invoice': invoice,
            'items': items
        }
    )