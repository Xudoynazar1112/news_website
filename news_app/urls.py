from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_list, name='all_news_list'),
    path('news/<slug:news>/', news_detail, name="news_detail_page"),
    path('create/', NewsCreateView.as_view(), name='create_page'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='update_page'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='delete_page'),
    path('contact-us/', contactPageViews, name='contact_page'),
    path('categories/', categoriesPageViews, name='categories_page'),
    path('single-news/', singlePageViews, name='single_news'),
    path('404error/', page404, name='page_404'),
    path('mahalliy/', LocalPageView.as_view(), name='local_page'),
    path('xorij/', ForeignPageView.as_view(), name='foreign_page'),
    path('texnalogiya/', TecnologyPageView.as_view(), name='tecnology_page'),
    path('sport/', SportPageView.as_view(), name='sport_page'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresults/', SearchResultsList.as_view(), name='search_results'),
]