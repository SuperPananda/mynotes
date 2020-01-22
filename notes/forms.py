from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    #author = forms.ModelChoiceField(queryset =None )
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author','slug','favorite') 
        #years = [(year, year) for year in ["Cсылка", "Памятка", "Заметка"]]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),      
        }