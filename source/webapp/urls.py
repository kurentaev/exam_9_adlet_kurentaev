from django.urls import path
from webapp.views.photos import IndexView, PhotoView, AddPhotoView, EditPhotoView, DeletePhotoView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('gallery/', IndexView.as_view(), name='home'),
    path('gallery/photo/<int:pk>', PhotoView.as_view(), name='photo'),
    path('gallery/photo/add', AddPhotoView.as_view(), name='add_photo'),
    path('gallery/photo/<int:pk>/edit', EditPhotoView.as_view(), name='edit_photo'),
    path('gallery/photo/<int:pk>/delete', DeletePhotoView.as_view(), name='delete_photo'),
]
