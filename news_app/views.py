from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from hitcount.views import HitCountMixin
from hitcount.utils import get_hitcount_model

from news_project.custom_permissions import OnlyLoggedSuperUser
from .models import News, Category
from .forms import ContactForm, CommentForm


def news_list(request):
    # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hitcount_response = HitCountMixin.hit_count(request, hit_count)
    if hitcount_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hitcount_response.hit_counted
        hitcontext['hit_message'] = hitcount_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi koment obektini yaratamiz, lekin DBga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # ma'lumotlar bazasiga saqlash
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        "news": news,
        'comments': comments,
        'comment_count': comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'news/single_page.html', context)


def homePageView(request):
    news_list = News.published.all().order_by('-published_time')[:15]
    categories = Category.objects.all()
    local_one = News.published.all().filter(category__name='Mahalliy').order_by('-published_time')[:1]
    local_news = News.published.all().filter(category__name='Mahalliy').order_by('-published_time')[1:6]
    context = {
        'news_list': news_list,
        'categories': categories,
        'local_news': local_news,
        'local_one': local_one,
    }
    return render(request, 'news/index.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-published_time')[:15]
        context['mahalliy_xabarlar'] = News.published.all().filter(category__name='Mahalliy').order_by('-published_time')[:5]
        context['sport_xabarlar'] = News.published.all().filter(category__name='Sport').order_by('-published_time')[:5]
        context['xorij_xabarlar'] = News.published.all().filter(category__name='Xorij').order_by('-published_time')[:5]
        context['texnalogiya_xabarlar'] = News.published.all().filter(category__name='Texnalogiya').order_by('-published_time')[:5]

        return context


def contactPageViews(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse("<h2>Biz bilan bog'langaningiz uchun rahmat!</h2>")
    context = {
        "form": form
    }

    return render(request, 'news/contact.html', context)


class LocalPageView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news

class ForeignPageView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news


class TecnologyPageView(ListView):
    model = News
    template_name = 'news/texnalogiya.html'
    context_object_name = 'texnalogiya_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnalogiya')
        return news


class SportPageView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'image', 'body', 'category', 'status',)
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'title_uz', 'title_en', 'title_ru', 'slug', 'body',
              'body_uz', 'body_en', 'body_ru', 'image', 'category', 'status')


def categoriesPageViews(request):
    context = {

    }
    return render(request, 'news/category.html', context)


def singlePageViews(request):
    context = {

    }
    return render(request, 'news/single.html', context)


def page404(request):
    context = {

    }
    return render(request, 'news/404.html', context)

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }

    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))