from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return redirect('/dashboard/')

urlpatterns = [
    path('', home),

    path('admin/', admin.site.urls),

    path('dashboard/', include('dashboard.urls')),

    path('products/', include('products.urls')),

    path('customers/', include('customers.urls')),

    path('billing/', include('billing.urls')),
    path(
    'accounts/',
    include('accounts.urls')
),
    path(
    'reports/',
    include('reports.urls')
),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )