from django.urls import path, include
from .views import kundli_view, astrology_home, kundli_create_view, user_signup

urlpatterns = [
    path('', astrology_home, name='astrology_home'),
    path('kundli/new/', kundli_create_view, name='kundli_create'),
    path('kundli/<int:pk>/', kundli_view, name='kundli_north_indian'),
    path('api/', include('astrology.api.urls')),
    path('signup/', user_signup, name='signup'),
]