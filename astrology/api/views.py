from rest_framework import generics
from ..models import KundliDetails
from .serializers import KundliDetailsSerializer

class KundliDetailsListCreateAPIView(generics.ListCreateAPIView):
    queryset = KundliDetails.objects.all()
    serializer_class = KundliDetailsSerializer

class KundliDetailsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KundliDetails.objects.all()
    serializer_class = KundliDetailsSerializer