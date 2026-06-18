from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.invoice_list,
        name='invoice_list'
    ),

    path(
        'create/',
        views.create_invoice,
        name='create_invoice'
    ),
    path(
    'download/<int:id>/',
    views.download_invoice,
    name='download_invoice'
),
    path(
    'print/<int:id>/',
    views.print_invoice,
    name='print_invoice'
),
    path(
    'export/',
    views.export_invoices,
    name='export_invoices'
),
    path(
    'invoice/<int:id>/',
    views.invoice_detail,
    name='invoice_detail'
),

]