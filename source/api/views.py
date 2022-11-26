from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Photo, FavouritePhotos
# from webapp.models import Respond, Vacancies, Resumes
# from accounts.models import Account


class AddFavouriteView(APIView):
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




#
# class EditAccountView(APIView):
#     def post(self, request, *args, **kwargs):
#         if request.data.get('username', False) == '':
#             return JsonResponse({'error': 'Поле логина пустое'}, status=400)
#         if request.data.get('name', False) == '':
#             return JsonResponse({'error': 'Поле имени пустое'}, status=400)
#         if request.data.get('lastname', False) == '':
#             return JsonResponse({'error': 'Поле фамилии пустое'}, status=400)
#         if request.data.get('email', False) == '':
#             return JsonResponse({'error': 'Поле почты пустое'}, status=400)
#         if request.data.get('phone', False) == '':
#             return JsonResponse({'error': 'Поле номера пустое'}, status=400)
#         for account in Account.objects.all():
#             if self.request.user.username == request.data.get('username', False):
#                 pass
#             elif account.username == request.data.get('username', False):
#                 return JsonResponse({'error': 'Такое имя уже есть'}, status=400)
#             if self.request.user.email == request.data.get('email', False):
#                 pass
#             elif account.email == request.data.get('email', False):
#                 return JsonResponse({'error': 'Такая почта уже есть'}, status=400)
#         Account.objects.filter(pk=self.request.user.pk).update(username=request.data.get('username', False),
#                                                                email=request.data.get('email', False),
#                                                                first_name=request.data.get('name', False),
#                                                                last_name=request.data.get('lastname', False),
#                                                                phone=request.data.get('phone', False),
#                                                                avatar=request.data.get('avatar', False)
#                                                                )
#         print(Account.objects.filter(pk=self.request.user.pk))
#         return JsonResponse({'answer': 'Данные успешно обновлены'})


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')
