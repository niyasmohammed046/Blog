from django import forms
from . models import Comments ,Subscribe


class CommentForm(forms.ModelForm):
    # name = forms.CharField(max_length=100,label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter Your Name"}))
    # comment = forms.CharField(max_length=100,label="",widget=forms.Textarea(attrs={'class':'form-control','placeholder':"Type your comments..."}))
    # email = forms.EmailField(max_length=100,label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}))


    class Meta:
        model = Comments
        fields = ('comment','name','email')

    def __init__(self, *args ,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['comment'].widget.attrs['placeholder'] = 'type your comments...'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Your Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'



class SubscribeForm(forms.ModelForm):

    email = forms.EmailField(max_length=100,label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}))
    class Meta:
        model = Subscribe
        fields = '__all__'
    
    # def __init__(self,*args,**kwars):
    #     super().__init__(*args,**kwars)
    #     self.fields['email'].widget.attrs['label'] = ''
    #     self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'