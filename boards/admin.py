from django.contrib import admin

from .models import Board, Topic, Post

class InLineLesson(admin.TabularInline):
    model=Topic
    extra=1
    max_num=3

class BoardAdmin(admin.ModelAdmin):
    # fields=('name','description')
    inlines=[InLineLesson]
    fieldsets=(
    (None,{
        'fields':(
            'name',
            'description'
        )
    }),
    )
    list_display=('name','description')
    list_display_links=('description',)
    list_editable=('name',)
    list_filter=('name',)
    search_fields=('name',)
    # change_list_template='1/change_list.html'

class TopicAdmin(admin.ModelAdmin):
    list_display=('subject','board','starter','views','last_updated')
    list_filter=('subject','starter','last_updated')

class PostAdmin(admin.ModelAdmin):
    list_display=('message','topic','created_at','created_by','updated_at','updated_by')
    list_filter=('topic','updated_at')

admin.site.register(Board, BoardAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
