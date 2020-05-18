from django.contrib import admin
from .models import News, NewsThread, NewsSubscription


class NewsInline(admin.TabularInline):
    model = News
    extra = 3
    verbose_name = "Thread news"
    verbose_name_plural = "News"


class NewsThreadAdmin(admin.ModelAdmin):
    inlines = [NewsInline]
    search_fields = ['thread_name']


class NewsSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'thread')


admin.site.register(NewsThread, NewsThreadAdmin)
admin.site.register(NewsSubscription, NewsSubscriptionAdmin)

# admin.site.register(Review)
# admin.site.register(Project)

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3


# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': [
#          'pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
#     search_fields = ['question_text']
#     list_filter = ['pub_date']
#     list_display = ('question_text', 'pub_date', 'was_published_recently')


# admin.site.register(Question, QuestionAdmin)
