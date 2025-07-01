from django.urls import path
from .views import kundli_view, astrology_home

urlpatterns = [
    path('', astrology_home, name='astrology_home'),
    path('kundli/<int:pk>/', kundli_view, name='kundli_north_indian'),
]