from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, FormView, RedirectView, ListView, DetailView, UpdateView, \
    DeleteView
from django.views.generic.base import View
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

# Create your views here.
from muxic.form import UserForm, CreatSongForm
from muxic.models import *


class IndexView(TemplateView):
    template_name = 'muxic/index.html'


class AllSong(ListView):
    template_name = 'muxic/all_song.html'
    context_object_name = 'all_song'

    def get_queryset(self):
        return Song.objects.all()


class SongDetail(DetailView):
    template_name = 'muxic/song_detail.html'
    model = Song

    # def get(self, request, id, **kwargs):
    #     song_title = Song.objects.get(pk=id)
    #     return render(request, self.template_name, {'detSong': song_title})


class ProfileView(View):
    template_name = 'muxic/user.html'

    # username = User.username

    def get(self, request, username):
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        return render(request, self.template_name, {'user_profile': user_profile})


class RegisterView(View):
    form_class = UserForm
    template_name = 'muxic/registration_form.html'

    # Display blank form
    def get(self, request):
        form = self.form_class(None)
        print(form)
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


class LoginView(FormView):
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'muxic/login.html'
    # template_name = 'muxic/theme.html'
    success_url = '../../'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            # redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

            redirect_to = 'muxic/index.html'
        # netloc = urlparse.urlparse(redirect_to)[1]
        # if not redirect_to:
        #     redirect_to = settings.LOGIN_REDIRECT_URL
        # # Security check -- don't allow redirection to a different host.
        # elif netloc and netloc != self.request.get_host():
        #     redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)


class LogoutView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'muxic:index'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class Search(ListView):
    template_name = 'muxic/search.html'

    def get(self, request):

        queryset_list = Song.objects.all().order_by("-date_release")
        query = request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)
                # Q(artist__icontains=query)
            ).distinct()
            # paginator = Paginator(queryset_list, 5)
            # page_request_var = 'page'
            # page = request.GET.get(page_request_var)
            # try:
            #     queryset = paginator.page(page)
            # except PageNotAnInteger:
            #     queryset = paginator.page(1)
            # except EmptyPage:
            #     queryset = paginator.page(paginator.num_pages)
            #
            # context = {
            #     "queryset_list": queryset,
            #     "title":"list",
            #     "page_request_var": page_request_var
            # }
            return render(request, self.template_name, {'queryset_list': queryset_list})
        else:
            return render(request, self.template_name, )


# class SongCreate(CreateView):
#     # form_class = CreateSongForm
#     model = Song
#     template_name = 'muxic/song_form.html'
#     fields = ['title', 'artist', 'logo', 'file', 'date_release', 'lyric']
#
#     def get_form(self):
#         form_class = self.get_form_class()
#         form = super(SongCreate, self).get_form(form_class)
#         form.fields['date_release'].widget = forms.DateInput()
#         return form

class SongCreate(CreateView):
    form_class = CreatSongForm
    model = Song
    template_name = 'muxic/song_form.html'


class SongUpdate(forms.ModelForm):
    model = Song
    fields = ['title', 'artist', 'genre', 'logo', 'file', 'date_release', 'lyric']


class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('muxic:allsong')
