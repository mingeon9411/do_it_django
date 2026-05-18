from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'head_image', 'file_upload', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content', 'image', 'file']
        labels = {
            'author': '작성자',
            'content': '댓글 내용',
            'image': '이미지 첨부',
            'file': '파일 첨부',
        }
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '댓글을 입력하세요'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
