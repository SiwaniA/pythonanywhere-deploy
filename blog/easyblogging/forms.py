from django import forms
from . models import BlogModel,Comment,Feedback

class Edit_Blog(forms.ModelForm):
    class Meta:
        model=BlogModel
        fields=('title','content')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields= {'comment',}
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }

class Feedback_form(forms.ModelForm):
    class Meta:
        model=Feedback
        fields='__all__'