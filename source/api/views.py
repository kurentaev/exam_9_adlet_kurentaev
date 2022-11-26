from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Photo, FavouritePhotos


class AddFavouriteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=request.data.get('photo', False))
        user = get_object_or_404(get_user_model(), pk=request.data.get('user', False))
        for favourite in FavouritePhotos.objects.all():
            if favourite.photo.pk == int(request.data.get('photo', False)) and \
                    favourite.user.pk == int(request.data.get('user', False)):
                FavouritePhotos.objects.filter(photo=photo, user=user).delete()
                return Response({'answer': 'Added to favourite'})
        FavouritePhotos.objects.create(photo=photo, user=user)
        return Response({'answer': 'Deleted from favourite'})


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')
