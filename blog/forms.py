from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        label='태그',
        help_text='쉼표(,)로 구분하여 입력  예) 파이썬, 장고, 웹',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '태그1, 태그2, 태그3'}),
    )

    class Meta:
        model = Post
        fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']


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
