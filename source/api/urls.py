from django.urls import path
from api.views import get_token_view, AddFavouriteView

urlpatterns = [
    path('token/', get_token_view, name='token'),
    path('add_favourite/', AddFavouriteView.as_view(), name='add_favourite'),
]
