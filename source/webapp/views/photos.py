from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import Photo
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


class EditPhotoView(LoginRequiredMixin, UpdateView):
    template_name = 'photo/add_photo.html'
    model = Photo
    form_class = PhotoForm

    def get_success_url(self):
        return reverse('photo', kwargs={'pk': self.object.pk})


class DeletePhotoView(LoginRequiredMixin, DeleteView):
    template_name = 'photo/delete_photo.html'
    model = Photo
    context_object_name = 'vacancy'

    def get_success_url(self):
        return reverse('index')


