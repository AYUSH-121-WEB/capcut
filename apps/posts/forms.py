from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    # Field to capture hashtags as string, parsed in View
    hashtags = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Add hashtags...'}))

    class Meta:
        model = Post
        fields = ('content', 'image', 'video')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind?", 'class': 'w-full rounded-lg border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'}),
        }

    def save_hashtags(self, post):
        from .models import Tag
        hashtags_str = self.cleaned_data.get('hashtags')
        if hashtags_str:
            # Parse hashtags: split by space or comma, remove leading #, strip whitespace
            tags_list = [t.strip().lstrip('#') for t in hashtags_str.replace(',', ' ').split()]
            for tag_name in tags_list:
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...', 'class': 'w-full rounded-lg border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'}),
        }
