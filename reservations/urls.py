from django.urls import path
from . import views

urlpatterns = [
    path('rezerve/<int:koltuk_id>/', views.koltuk_rezerve_et, name='koltuk_rezerve_et'),
    path('satin-al/<int:koltuk_id>/', views.satin_al, name='satin_al'),
]