from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import SignupForm, LoginForm, NewsForm, EventForm, AcademicForm, MediaForm, CafeForm, SportForm, MatchForm
from .models import *


def home(request):
    featured=NewsPost.objects.filter(status='PUBLISHED').order_by('-featured','-published_at')[:6]
    events=Event.objects.filter(starts_at__gte=timezone.now()).select_related('organizer')[:6]
    clubs=Club.objects.filter(is_active=True)[:8]; societies=Society.objects.filter(is_active=True)[:8]
    return render(request,'core/home.html',{'featured':featured,'events':events,'clubs':clubs,'societies':societies})

def about(request): return render(request,'core/about.html')

def login_view(request):
    if request.user.is_authenticated:return redirect('dashboard')
    form=LoginForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): login(request,form.user); return redirect(request.GET.get('next','dashboard'))
    return render(request,'registration/login.html',{'form':form})

def signup(request):
    form=SignupForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        u=form.save(); login(request,u); messages.success(request,'Welcome to DTC Campus Hub!'); return redirect('dashboard')
    return render(request,'registration/signup.html',{'form':form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    user=request.user
    my_orgs=Organization.objects.filter(membership__user=user).distinct()
    pending=NewsPost.objects.filter(status='PENDING').count() if user.role=='SUPER_ADMIN' else 0
    stats={'users':User.objects.count(),'news':NewsPost.objects.filter(status='PUBLISHED').count(),'events':Event.objects.count(),'orgs':Organization.objects.count()}
    return render(request,'dashboard/dashboard.html',{'my_orgs':my_orgs,'pending':pending,'stats':stats})

@login_required
def profile(request):
    if request.method=='POST':
        for f in ['first_name','last_name','university','course','branch','bio']:
            setattr(request.user,f,request.POST.get(f,getattr(request.user,f)))
        request.user.save(); messages.success(request,'Profile updated.'); return redirect('profile')
    return render(request,'accounts/profile.html')

@login_required
def notifications(request):
    Notification.objects.filter(user=request.user).update(is_read=True)
    return render(request,'accounts/notifications.html',{'items':request.user.notifications.all()[:30]})

def clubs(request): return render(request,'clubs/list.html',{'clubs':Club.objects.filter(is_active=True)})
def societies(request): return render(request,'societies/list.html',{'societies':Society.objects.filter(is_active=True)})

def organization_detail(request,slug):
    org=get_object_or_404(Organization,slug=slug,is_active=True)
    org_kind='Technical Club' if isinstance(org, Club) else 'Cultural Society'
    news=org.news.filter(status='PUBLISHED')[:6]; events=org.event_set.filter(starts_at__gte=timezone.now())[:6]
    members=org.membership_set.select_related('user')[:30]; media=org.media.all()[:12]
    following=request.user.is_authenticated and Follow.objects.filter(user=request.user,organization=org).exists()
    return render(request,'core/organization_detail.html',{'org':org,'org_kind':org_kind,'news':news,'events':events,'members':members,'media':media,'following':following})

@login_required
def toggle_follow(request,slug):
    org=get_object_or_404(Organization,slug=slug)
    f=Follow.objects.filter(user=request.user,organization=org)
    if f.exists(): f.delete(); messages.info(request,f'Unfollowed {org.name}.')
    else:
        Follow.objects.create(user=request.user,organization=org); messages.success(request,f'Following {org.name}.')
    return redirect(request.META.get('HTTP_REFERER','home'))

@login_required
def add_media(request,slug):
    org=get_object_or_404(Organization,slug=slug)
    if not Membership.objects.filter(user=request.user,organization=org).exists() and request.user.role!='SUPER_ADMIN': raise Http404
    form=MediaForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        m=form.save(commit=False); m.organization=org; m.save(); messages.success(request,'Media uploaded.'); return redirect(org.get_absolute_url() if hasattr(org,'get_absolute_url') else 'home')
    return render(request,'core/simple_form.html',{'form':form,'title':f'Upload media to {org.name}'})

@login_required
def org_manage(request,slug):
    org=get_object_or_404(Organization,slug=slug,is_active=True)
    if request.user.role!='SUPER_ADMIN' and not Membership.objects.filter(user=request.user,organization=org,role__in=['LEAD','COORDINATOR']).exists():
        messages.error(request,'You do not have permission to manage this community.'); return redirect('home')
    context={'org':org,'news':org.news.all(),'events':org.event_set.all(),'members':org.membership_set.select_related('user'),'media':org.media.all()}
    return render(request,'dashboard/org_manage.html',context)

@login_required
def org_add_news(request,slug):
    org=get_object_or_404(Organization,slug=slug)
    if request.user.role!='SUPER_ADMIN' and not Membership.objects.filter(user=request.user,organization=org,role__in=['LEAD','COORDINATOR']).exists(): raise Http404
    form=NewsForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        n=form.save(commit=False); n.author=request.user; n.organization=org; n.status='PUBLISHED' if request.user.role=='SUPER_ADMIN' else 'PENDING'; n.published_at=timezone.now() if n.status=='PUBLISHED' else None; n.save(); messages.success(request,'News submitted.'); return redirect('org_manage',slug=slug)
    return render(request,'core/simple_form.html',{'form':form,'title':f'Post news — {org.name}'})

@login_required
def org_add_event(request,slug):
    org=get_object_or_404(Organization,slug=slug)
    if request.user.role!='SUPER_ADMIN' and not Membership.objects.filter(user=request.user,organization=org,role__in=['LEAD','COORDINATOR']).exists(): raise Http404
    form=EventForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        e=form.save(commit=False); e.organizer=org; e.save(); messages.success(request,'Event created.'); return redirect('org_manage',slug=slug)
    return render(request,'core/simple_form.html',{'form':form,'title':f'Create event — {org.name}'})


PAGE_MODELS = {'news': NewsPost, 'events': Event, 'academics': AcademicResource, 'campus': Cafe, 'sports': Sport}

def can_manage_page(request, page):
    return request.user.is_authenticated and (request.user.role == 'SUPER_ADMIN' or PageAdmin.objects.filter(user=request.user, page=page.upper()).exists())

def page_editor_context(request, page):
    if not can_manage_page(request,page): return {'can_manage_page':False,'page_key':page}
    if page=='news': items=NewsPost.objects.order_by('-created_at')[:30]; form=NewsForm(); forms=[(x,NewsForm(instance=x)) for x in items]
    elif page=='events': items=Event.objects.order_by('-starts_at')[:30]; form=EventForm(); forms=[(x,EventForm(instance=x)) for x in items]
    elif page=='academics': items=AcademicResource.objects.order_by('-published_at')[:40]; form=AcademicForm(); forms=[(x,AcademicForm(instance=x)) for x in items]
    elif page=='campus': items=Cafe.objects.order_by('is_mess','name')[:40]; form=CafeForm(); forms=[(x,CafeForm(instance=x)) for x in items]
    else: items=Sport.objects.order_by('name')[:30]; form=SportForm(); forms=[(x,SportForm(instance=x)) for x in items]
    return {'can_manage_page':True,'page_key':page,'page_editor_title':f'{page.title()} editor','page_editor_form':form,'page_editor_items':forms}

@login_required
def page_save(request,page):
    if request.method!='POST' or not can_manage_page(request,page): raise Http404
    kind=request.POST.get('kind'); pk=request.POST.get('pk') or None
    cfg={'news':(NewsPost,NewsForm,'news'),'event':(Event,EventForm,'events'),'academic':(AcademicResource,AcademicForm,'academics'),'cafe':(Cafe,CafeForm,'campus'),'sport':(Sport,SportForm,'sports')}
    if kind not in cfg or cfg[kind][2]!=page: raise Http404
    model,Form,_=cfg[kind]; obj=get_object_or_404(model,pk=pk) if pk else None
    form=Form(request.POST,request.FILES,instance=obj)
    if form.is_valid():
        item=form.save(commit=False)
        if kind=='news': item.author=request.user; item.status='PUBLISHED'; item.published_at=item.published_at or timezone.now()
        item.save(); messages.success(request,'Changes saved.')
    else: messages.error(request,'Please check the editor fields.')
    return redirect(request.META.get('HTTP_REFERER',f'/{page}/'))

@login_required
def page_delete(request,page):
    if request.method!='POST' or not can_manage_page(request,page): raise Http404
    cfg={'news':NewsPost,'event':Event,'academic':AcademicResource,'cafe':Cafe,'sport':Sport}; kind=request.POST.get('kind')
    expected={'news':'news','event':'events','academic':'academics','cafe':'campus','sport':'sports'}
    if kind not in cfg or expected[kind]!=page: raise Http404
    get_object_or_404(cfg[kind],pk=request.POST.get('pk')).delete(); messages.success(request,'Deleted.'); return redirect(request.META.get('HTTP_REFERER',f'/{page}/'))

def news(request):
    q=request.GET.get('q','').strip(); items=NewsPost.objects.filter(status='PUBLISHED')
    if q: items=items.filter(Q(title__icontains=q)|Q(content__icontains=q)|Q(excerpt__icontains=q))
    context={'items':items,'q':q}; context.update(page_editor_context(request,'news')); return render(request,'news/list.html',context)
def news_detail(request,slug): return render(request,'news/detail.html',{'item':get_object_or_404(NewsPost,slug=slug,status='PUBLISHED')})

def events(request):
    context={'events':Event.objects.select_related('organizer').order_by('starts_at')}; context.update(page_editor_context(request,'events')); return render(request,'events/list.html',context)
def event_detail(request,slug): return render(request,'events/detail.html',{'event':get_object_or_404(Event,slug=slug)})
@login_required
def register_event(request,slug):
    event=get_object_or_404(Event,slug=slug)
    EventRegistration.objects.get_or_create(event=event,user=request.user)
    messages.success(request,'You are registered for this event.'); return redirect('event_detail',slug=slug)

def academics(request):
    university=request.GET.get('university','GGSIPU'); rtype=request.GET.get('type','')
    resources=AcademicResource.objects.filter(university=university)
    if rtype: resources=resources.filter(resource_type=rtype)
    context={'resources':resources,'university':university,'rtype':rtype}; context.update(page_editor_context(request,'academics')); return render(request,'academics/index.html',context)

def campus(request):
    context={'cafes':Cafe.objects.filter(is_mess=False),'mess':Cafe.objects.filter(is_mess=True)}; context.update(page_editor_context(request,'campus')); return render(request,'campus/index.html',context)
def sports(request):
    context={'sports':Sport.objects.prefetch_related('matches')}; context.update(page_editor_context(request,'sports')); return render(request,'sports/index.html',context)
