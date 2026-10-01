from django import forms
from django.contrib.auth import authenticate
from .models import User, NewsPost, Event, AcademicResource, MediaItem

class SignupForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['first_name','last_name','email','password','university','course','branch','semester']
    def save(self,commit=True):
        u=super().save(commit=False); u.set_password(self.cleaned_data['password']); u.username=u.email
        if commit: u.save()
        return u

class LoginForm(forms.Form):
    email=forms.EmailField(); password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        c=super().clean(); self.user=authenticate(username=c.get('email'),password=c.get('password'))
        if not self.user: raise forms.ValidationError('Invalid email or password.')
        return c

class NewsForm(forms.ModelForm):
    class Meta: model=NewsPost; fields=['title','excerpt','content','image','organization','featured']

class EventForm(forms.ModelForm):
    class Meta: model=Event; fields=['title','description','poster','organizer','venue','starts_at','ends_at','registration_url','registration_deadline','status','capacity']
    widgets={
        'starts_at':forms.DateTimeInput(attrs={'type':'datetime-local'}),
        'ends_at':forms.DateTimeInput(attrs={'type':'datetime-local'}),
        'registration_deadline':forms.DateTimeInput(attrs={'type':'datetime-local'}),
    }

class AcademicForm(forms.ModelForm):
    class Meta: model=AcademicResource; fields=['title','university','course','branch','semester','resource_type','description','file','external_url']

class MediaForm(forms.ModelForm):
    class Meta: model=MediaItem; fields=['title','image','video_url','caption']
