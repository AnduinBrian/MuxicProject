from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.base import View

# Create your views here.
from muxic.form import UserForm


class IndexView(TemplateView):
    template_name = 'muxic/index.html'


class AddAlbumView(TemplateView):
    template_name = 'muxic/add_album.html'


# class UserView(TemplateView):
#     template_name = 'muxic/user.html'


class UserFormView(View):
    form_class = UserForm
    template_name = 'muxic/registration_form.html'

    # Display blank form
    def get(self, request):
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

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})
