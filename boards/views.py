from django.shortcuts import render, redirect
from django.http import Http404
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm

# Create your views here.
def index(request):
    boards = Board.objects.all()

    return render(
        request,
        'boards/index.html',
        {
            'boards':boards
        }
    )

def board_topics(request, pk):
    try:
        board=Board.objects.get(pk=pk)
    except Board.DoesNotExist :
        raise Http404
    return render(
        request,
        'boards/topics.html',
        {
            'board':board
        }
    )

def new_topic(request, pk):
    try:
        board=Board.objects.get(pk=pk)
    except Board.DoesNotExist :
        raise Http404
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', pk=board.pk)  
    else:
        form=NewTopicForm()
    
    return render(
        request, 
        'boards/new_topic.html', 
        {
            'board': board, 
            'form': form
        }
    )
