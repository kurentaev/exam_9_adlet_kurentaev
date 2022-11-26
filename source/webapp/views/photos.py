from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import Photo, FavouritePhotos
from webapp.forms.photo import PhotoForm


class IndexView(ListView):
    template_name = 'photo/photos.html'
    model = Photo
    context_object_name = 'photos'


class PhotoView(DetailView):
    template_name = 'photo/photo.html'
    model = Photo
    context_object_name = 'photo'


class AddPhotoView(LoginRequiredMixin, CreateView):
    template_name = 'photo/add_photo.html'
    model = Photo
    form_class = PhotoForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=self.request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.author = request.user
            photo.save()
            return redirect('index')
        context = {}
        context['form'] = form
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('photo', kwargs={'pk': self.object.pk})


class EditPhotoView(PermissionRequiredMixin, UpdateView):
    template_name = 'photo/add_photo.html'
    model = Photo
    form_class = PhotoForm
    permission_required = 'webapp.change_photo'

    def get_success_url(self):
        return reverse('photo', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user \
               or self.request.user.is_superuser


class DeletePhotoView(PermissionRequiredMixin, DeleteView):
    template_name = 'photo/delete_photo.html'
    model = Photo
    context_object_name = 'vacancy'
    permission_required = 'webapp.delete_photo'

    def get_success_url(self):
        return reverse('index')

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user \
               or self.request.user.is_superuser


class ChoosePhotoView(CreateView):
    model = FavouritePhotos

    def post(self, request, *args, **kwargs):
        photo_pk = kwargs.get('pk')
        photo = get_object_or_404(Photo, pk=photo_pk)
        if not self.model.objects.filter(photo_id=photo_pk, author_id=self.request.user.pk):
            self.model.objects.create(photo_id=photo_pk, author_id=self.request.user.pk)
            photo.save()
        else:
            photo.save()
            self.model.objects.filter(photo_id=photo_pk, author_id=self.request.user.pk).delete()
        return redirect(request.META.get('HTTP_REFERER'))
