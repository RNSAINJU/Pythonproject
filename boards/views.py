from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect, render,reverse, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView

from .forms import NewBoardForm,NewTopicForm, PostForm
from .models import Board, Post, Topic
from django.db.models import Count
from django.views.generic import CreateView, UpdateView, TemplateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.mail import send_mail

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.mail import send_mail
from django.contrib.auth.mixins import PermissionRequiredMixin

import json

def about(request):
    return render(request, 'about.html')


def partners(request):
    return render(request, 'partners.html')

def news(request):
    # send_mail('subject', 'body of the message', 'help.khwoppagiftcard.store', ['aryan.sainju@gmail.com'],fail_silently=False)
    return render(request, 'news.html')

class BoardListView(ListView):
    model= Board
    context_object_name = 'boards'
    template_name = 'home.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board']=self.board
        return super().get_context_data(**kwargs)
    def get_queryset(self):
        self.  board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset=self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset



class PostListView(ListView):
    model=Post
    context_object_name= 'posts'
    template_name ='topic_posts.html'
    paginate_by=20

    def get_context_data(self, **kwargs):

        session_key='viewed_topics{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views +=1
            self.topic.save()
            self.request.session[session_key]=True

        kwargs['topic'] =self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic=get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset=self.topic.posts.order_by('created_at')
        return queryset

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated=timezone.now()
            topic.save()

            topic_url =reverse('boards:topic_posts', kwargs={'pk':pk, 'topic_pk':topic_pk})
            topic_post_url='{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name='new_post.html'

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'

    ''' pk_url_kwarg will be used to identify the name of the keyword argument used
    to retrieve the Post object. It’s the same as we define in the urls.py.
    '''
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        '''
        line queryset = super().get_queryset() we are reusing the get_queryset method
        from the parent class, that is, the UpateView class. Then, we are adding an extra
        filter to the queryset, which is filtering the post using the logged in user,
        available inside the request object.
        '''
        queryset=super().get_queryset()
        return  queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post=form.save(commit=False)
        post.updated_by=self.request.user
        post.updated_at=timezone.now()
        post.save()
        return redirect('boards:topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        uploaded_file_url=fs.url(filename)
        return render(request, 'simple_upload.html',{
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')


def board_edit(request, pk):
    post = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        form = NewBoardForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('boards:boards', pk=post.pk)
    else:
        form = NewBoardForm(instance=post)
    return render(request, 'kgc/board_edit.html', {'form': form})

class BoardView(PermissionRequiredMixin, TemplateView):
    permission_required='superuserstatus'
    template_name='kgc/boards.html'

    def get(self,request):
        board=Board.objects.all().order_by('id')
        model_name,view=self.__class__.__name__.split('V')
        form=NewBoardForm()

        queryset={'form':form,'board':board,'model_name':model_name}
        return render(request,self.template_name,queryset)

    def post(self,request):
        form=NewBoardForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            return redirect('boards:boards')

    def delete(self,request):
        id=json.loads(request.body)['id']
        board=get_object_or_404(Board, id=id)
        board.delete()
        return HttpResponse('')
