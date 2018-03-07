from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.views.generic.base import View

# Create your views here.
from muxic.form import UserForm


class IndexView(TemplateView):
    template_name = 'muxic/index.html'


class AddAlbumView(TemplateView):
    template_name = 'muxic/add_album.html'


class UserView(TemplateView):
    template_name = 'muxic/user.html'


class UserFormView(View):
    form_class = UserForm
    # success_url = 'muxic:index'
    template_name = 'muxic/registration_form.html'

    # def form_valid(self, form):
    #     # form = self.form_class(request.POST)
    #     user = form.save(commit=False)
    #
    #     # Clean data
    #     username = form.cleaned_data['username']
    #     email = form.cleaned_data['email']
    #     password = form.cleaned_data['password']
    #     user.set_password(password)
    #     user.save()
    #
    #     # returns User objects if credentials are correct
    #     user = authenticate(username=username, password=password)
    #
    #     # login(request, user)
    #     # return redirect('music:index')
    #
    #     if user is not None:
    #         if user.is_active:
    #             login(request, user)
    #             return redirect('music:index')
    #
    #     return render(request, self.template_name, {'form': form})

    # Display blank form
    def get(self, request):
        if request.method != 'POST':
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})

    # Process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            # login(request, user)
            # return redirect('muxic:index')

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('muxic:index')

        return render(request, self.template_name, {'form': form})
