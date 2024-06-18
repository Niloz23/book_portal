from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import MyActivationCodeForm, CommentForm, BookForm, AcceptCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .filters import CommentFilter


def activation(request):
    if request.user.is_authenticated:
        return redirect('/books/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get('code')
                print('code_use', code_use)
                if OneTimeCode.objects.filter(code=code_use):
                    code1 = OneTimeCode.objects.get(code=code_use)
                    p1 = EmailAddress.objects.get(user_id=code1.user.id)
                else:
                    form.add_error(None, 'Неправильный код')
                    return render(request, 'account/email/activate.html', {'form': form})
                if not p1.verified:
                    p1.verified = True
                    p1.save()

                    u1 = User.objects.get(id=p1.user_id)
                    user = authenticate(request, username=u1.username, password=u1.password)
                    if user is not None:
                        login(request, user)

                    code1.delete()
                    return redirect('/accounts/login/')
                else:
                    form.add_error(None, 'Unknown or disabled account')
                return render(request, 'account/email/activate.html', {'form': form})
            else:
                form.add_error(None, 'Форма не валидна')
                return render(request, 'account/email/activate.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'account/email/activate.html', {'form': form})


class BooksList(ListView):
    model = Book
    ordering = '-created_at'
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 10


class BooksDetail(DetailView):
    model = Book
    template_name = 'book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.request.path_info[7:][:-1]
        c1 = Comment.objects.filter(book_id=book_id)
        context['Books'] = c1
        return context


class BookCreate(LoginRequiredMixin, CreateView):
    form_class = BookForm
    model = Book
    template_name = 'book_edit.html'
    success_url = ''

    def form_valid(self, form):
        book = form.save(commit=False)
        author = User.objects.filter(username=self.request.user).values('id')
        author_id = author.values_list('id')[0][0]
        book.user_id = author_id
        book.save()
        photos = self.request.FILES.getlist('photo')
        if photos:
            for photo in photos:
                photo_obj = Photo(image=photo)
                photo_obj.save()
                book_photo_obj = BookPhoto(book=book, photo=photo_obj)
                book_photo_obj.save()
        return super().form_valid(form)


class BookUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = BookForm
    model = Book
    template_name = 'Book_edit.html'


class BookDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('books_list')


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'
    success_url = reverse_lazy('books_list')


class CommentAccept(LoginRequiredMixin, UpdateView):
    form_class = AcceptCommentForm
    model = Comment
    queryset = Comment.objects.filter(is_acept=False)
    template_name = 'comment_accept.html'
    success_url = '/comments/'


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = '/comments/'


class CommentsList(LoginRequiredMixin, ListView):
    model = Comment
    ordering = '-created_at'
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = 5

    def get_queryset(self):
        u1 = self.request.user
        c1 = Comment.objects.select_related('book').filter(book__user=u1)
        queryset = c1
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u1 = self.request.user
        print('self.request.user', self.request.user)
        c1 = Comment.objects.select_related('book').filter(book__user=u1)
        context['filterset'] = self.filterset
        return context


class PhotoList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photos.html'
    context_object_name = 'photos'
    paginate_by = 10
