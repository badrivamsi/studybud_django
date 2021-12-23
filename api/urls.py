from django.urls import path
from .views import getRooms, getRoutes, getRoom

urlpatterns = [
    path('', getRoutes, name='api'),
    path('rooms/', getRooms, name='api-rooms'),
    path('rooms/<str:pk>', getRoom, name='api-room')
]