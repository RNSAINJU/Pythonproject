from django import forms

from .models import Board,Topic, Post

class NewBoardForm(forms.ModelForm):
    name=forms.CharField(max_length=12,
    widget=forms.TextInput(
    attrs={'class':"form-control"}
    ),required=True)
    description=forms.CharField(
        max_length=100,
        widget=forms.Textarea(
        attrs={'rows':2,'cols':30,'class':"form-control",'placeholder':'Type description'}
        )
    )

    class Meta:
        model=Board
        fields=['name','description']

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is in your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
