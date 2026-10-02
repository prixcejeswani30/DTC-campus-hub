from django import forms
from django.contrib.auth import authenticate
from cloudinary.forms import CloudinaryFileField
from .models import User, NewsPost, Event, AcademicResource, MediaItem, Cafe, Sport, Match

class SignupForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['first_name','last_name','email','password','university','course','branch','semester']
    def clean_email(self):
        email=self.cleaned_data['email'].lower().strip()
        if not email.endswith('@dtc.ac.in'):
            raise forms.ValidationError('Use your DTC college email address.')
        return email

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
    image=CloudinaryFileField(required=False, options={'tags':'dtc_news','quality':'auto','fetch_format':'auto','width':1600,'height':1000,'crop':'limit'})
    class Meta: model=NewsPost; fields=['title','excerpt','content','image','organization','featured']

class EventForm(forms.ModelForm):
    poster=CloudinaryFileField(required=False, options={'tags':'dtc_events','quality':'auto','fetch_format':'auto','width':1600,'height':1200,'crop':'limit'})
    class Meta:
        model=Event
        fields=['title','description','poster','organizer','venue','starts_at','ends_at','registration_url','registration_deadline','status','capacity']
        widgets={
            'starts_at':forms.DateTimeInput(attrs={'type':'datetime-local'}),
            'ends_at':forms.DateTimeInput(attrs={'type':'datetime-local'}),
            'registration_deadline':forms.DateTimeInput(attrs={'type':'datetime-local'}),
        }

class AcademicForm(forms.ModelForm):
    class Meta: model=AcademicResource; fields=['title','university','course','branch','semester','resource_type','description','file','external_url']

class MediaForm(forms.ModelForm):
    image=CloudinaryFileField(required=False, options={'tags':'dtc_gallery','quality':'auto','fetch_format':'auto','width':1800,'height':1200,'crop':'limit'})
    class Meta: model=MediaItem; fields=['title','image','video_url','caption']


class CafeForm(forms.ModelForm):
    class Meta:
        model=Cafe
        fields=['name','location','opening_hours','menu','prices','image','is_mess']

class SportForm(forms.ModelForm):
    class Meta:
        model=Sport
        fields=['name','team','description','image']

class MatchForm(forms.ModelForm):
    class Meta:
        model=Match
        fields=['sport','opponent','venue','starts_at','tournament','result','registration_url','notice']
        widgets={'starts_at':forms.DateTimeInput(attrs={'type':'datetime-local'})}
