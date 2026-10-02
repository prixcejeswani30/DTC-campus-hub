from django.urls import path
from . import views
urlpatterns=[
 path('',views.home,name='home'), path('about/',views.about,name='about'),
 path('login/',views.login_view,name='login'), path('signup/',views.signup,name='signup'), path('logout/',views.logout_view,name='logout'),
 path('dashboard/',views.dashboard,name='dashboard'), path('profile/',views.profile,name='profile'), path('notifications/',views.notifications,name='notifications'),
 path('clubs/',views.clubs,name='clubs'), path('clubs/<slug:slug>/',views.organization_detail,name='club_detail'),
 path('societies/',views.societies,name='societies'), path('societies/<slug:slug>/',views.organization_detail,name='society_detail'),
 path('org/<slug:slug>/follow/',views.toggle_follow,name='toggle_follow'), path('org/<slug:slug>/media/',views.add_media,name='add_media'), path('org/<slug:slug>/manage/',views.org_manage,name='org_manage'), path('org/<slug:slug>/manage/news/',views.org_add_news,name='org_add_news'), path('org/<slug:slug>/manage/event/',views.org_add_event,name='org_add_event'),
 path('news/',views.news,name='news'), path('news/<slug:slug>/',views.news_detail,name='news_detail'),
 path('events/',views.events,name='events'), path('events/<slug:slug>/',views.event_detail,name='event_detail'), path('events/<slug:slug>/register/',views.register_event,name='register_event'),
 path('academics/',views.academics,name='academics'), path('campus/',views.campus,name='campus'), path('sports/',views.sports,name='sports'),
 path('page/<slug:page>/save/',views.page_save,name='page_save'), path('page/<slug:page>/delete/',views.page_delete,name='page_delete'),
]
