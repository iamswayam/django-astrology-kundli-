from django.urls import path
from .views import KundliDetailsListCreateAPIView, KundliDetailsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('kundli/', KundliDetailsListCreateAPIView.as_view(), name='kundli-list-create'),
    path('kundli/<int:pk>/', KundliDetailsRetrieveUpdateDestroyAPIView.as_view(), name='kundli-detail'),
]