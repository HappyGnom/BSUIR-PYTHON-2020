from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import logout
from .models import NewsSubscription, NewsThread, News
from django.utils import timezone
import logging
from .forms import EditForm

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class NewsView(generic.View):
    template_name = 'news/news.html'
    context_object_name = 'context'

    def get_context(self, **kwargs):
        context = {}
        user_subs = map(lambda subs: subs.thread,
                        NewsSubscription.objects.filter(user=kwargs.get("user")))
        context['all_news'] = News.objects.filter(
            thread__in=user_subs, pub_date__lte=timezone.now()).order_by('-pub_date')

        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            logger.info(
                "User wasn't authenticated but tried to access news view")
            return HttpResponseNotFound("You are not authenticated as a developer.")
        else:
            is_manager = False
            if request.user.groups.filter(name='manager').count():
                logger.info("Manager " + request.user.username +
                            "accessed news")
                is_manager = True
            else:
                logger.info("Regular developer " +
                            request.user.username + " accessed news")

            return render(request, self.template_name, {**self.get_context(user=request.user), 'is_manager': is_manager})

    def post(self, request, *args, **kwargs):
        method = request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(request, *args, **kwargs)

        logout(request)
        logger.info("Loggin out user " + request.user.username)
        return HttpResponseRedirect(reverse('portfolio:portfolio'))

    def delete(self, request, *args, **kwargs):
        news_id = request.POST.get("_id", '')
        News.objects.filter(id=news_id).delete()

        logger.info("Deleted news number " + str(news_id))
        return self.get(request, *args, **kwargs)


class EditView(generic.View):
    template_name = 'news/edit_news.html'
    context_object_name = 'context'

    def get_context(self, **kwargs):
        context = {}

        if kwargs.get('news_id') != 0:
            news = News.objects.get(pk=kwargs.get('news_id'))
            context["news_form"] = EditForm(
                initial={'title_field': news.title, 'content_field': news.content})
        else:
            context["news_form"] = EditForm()

        context['thread'] = NewsThread.objects.get(pk=kwargs.get('thread_id'))

        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous or not request.user.groups.filter(name='manager').count():
            logger.info(
                "User wasn't authenticated as manager, but tried to access news edit view")
            return HttpResponseNotFound("You are not authenticated as a manager.")
        else:
            return render(request, self.template_name, self.get_context(**kwargs))

    def post(self, request, *args, **kwargs):
        news_form = EditForm(self.request.POST)
        if news_form.is_valid():
            title = news_form.cleaned_data['title_field']
            content = news_form.cleaned_data['content_field']

            news_id = kwargs.get('news_id')
            thread_id = kwargs.get('thread_id')
            thread = NewsThread.objects.get(pk=thread_id)

            if news_id == 0:
                new_news = News(title=title, pub_date=timezone.now(),
                                content=content, thread=thread)
                new_news.save()
                logger.info("Created news " + title +
                            " in thread " + thread.thread_name)
            else:
                News.objects.filter(pk=news_id).update(
                    title=title, content=content)
                logger.info("Updated news " + title +
                            " in thread " + thread.thread_name)

            return HttpResponseRedirect(reverse('news:news'))

        logger.warning("Form wasn't valid, but sent POST for save")
        return render(request, self.template_name, self.get_context(**kwargs))
