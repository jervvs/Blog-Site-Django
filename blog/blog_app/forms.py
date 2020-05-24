from django import forms
from blog_app.models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

    #widgets for styling by giving them css classes connect widgets to css styling
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }



class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
