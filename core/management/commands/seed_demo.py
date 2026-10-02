from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import *

class Command(BaseCommand):
    help='Seed DTC Campus Hub with demo data'
    def handle(self,*args,**kwargs):
        admin,created=User.objects.get_or_create(email='admin@dtc.ac.in',defaults={'first_name':'DTC','last_name':'Admin','role':'SUPER_ADMIN'})
        if created: admin.set_password('Admin@123')
        admin.role='SUPER_ADMIN'
        admin.is_staff=True
        admin.is_superuser=True
        admin.save()
        technical=[
            ('ACE DTC','The ACE DTC | Blockchain | AR/VR','Blockchain, AR/VR'),('AIR DTC','AI Renaissance DTC | AI | ML','AI, ML'),('CESTA DTC','DSA & CP | Gaming | IoT | Defence','DSA, CP, Gaming, IoT'),('E-Cell DTC','Entrepreneurship & Innovation','Entrepreneurship'),('FOSS DTC','Open Source | Cybersecurity','Open Source, Cybersecurity'),('GDG DTC','Google Technologies | Google Cloud | Android','Google Technologies'),('GFG DTC','GeeksforGeeks Campus Body','DSA, Development'),('INDUS RISE DTC','Entrepreneurship, Innovation & Community','Entrepreneurship')]
        cultural=[('Aavansh DTC','The Dramatics Society - DTC','Dramatics'),('Ameya DTC','The Dance Society - DTC','Dance'),('Artistia DTC','Fine Arts Society - DTC','Fine Arts'),('Awaaz DTC','The Publication Society - DTC | Debate & Poetry','Literature, Debate'),('Conchord DTC','The Music Club - DTC','Music'),('IBTIDAA DTC','The Cultural Council DTC','Cultural'),('Tasveer DTC','The Photography Club - DTC','Photography')]
        for name,tag,domain in technical:
            Club.objects.get_or_create(name=name,defaults={'tagline':tag,'domains':domain,'description':f'{name} is a student-led technical community at Delhi Technical Campus.','contact_email':f'{name.lower().replace(" ","").replace("&","")}@dtc.ac.in'})
        for name,tag,cat in cultural:
            Society.objects.get_or_create(name=name,defaults={'tagline':tag,'category':cat,'description':f'{name} brings students together through creativity, culture and campus life.','contact_email':f'{name.lower().replace(" ","")}@dtc.ac.in'})
        for i,(title,org) in enumerate([('DTC Campus Hub goes live',None),('Club recruitment season begins',Club.objects.first()),('Inter-college sports calendar announced',None)]):
            NewsPost.objects.get_or_create(title=title,defaults={'content':f'{title}. Follow DTC Campus Hub for verified campus updates, announcements and events.','excerpt':'Latest campus update for DTC students.','author':admin,'organization':org,'status':'PUBLISHED','published_at':timezone.now()-timedelta(hours=i)})
        for title,venue in [('DTC Hackathon Kickoff','Innovation Lab'),('Freshers Cultural Night','Main Auditorium'),('Inter-Club Tech Quiz','Seminar Hall')]:
            Event.objects.get_or_create(title=title,defaults={'description':f'{title} at Delhi Technical Campus.','venue':venue,'starts_at':timezone.now()+timedelta(days=2),'organizer':Club.objects.first(),'registration_url':'https://example.com/register','status':'UPCOMING'})
        for uni in ['GGSIPU','AKTU']:
            for typ,title in [('SYLLABUS',f'{uni} B.Tech Syllabus'),('EXAM',f'{uni} Upcoming Exam Dates'),('CALENDAR',f'{uni} Academic Calendar'),('NOTICE',f'{uni} Latest Notices'),('RESULT',f'{uni} Results & Result Notices'),('STUDY',f'{uni} Study Resources')]:
                AcademicResource.objects.get_or_create(title=title,university=uni,resource_type=typ,defaults={'description':f'Demo {uni} academic resource. Replace this with the official document before production.'})
        for name in ['Central Cafeteria','Food Court','DTC Mess']:
            Cafe.objects.get_or_create(name=name,defaults={'location':'Delhi Technical Campus','opening_hours':'8:00 AM – 9:00 PM','menu':'Breakfast, snacks, lunch, beverages','prices':'See counter menu / update in admin','is_mess':name=='DTC Mess'})
        for name in ['Football','Basketball','Cricket','Badminton']:
            sport,_=Sport.objects.get_or_create(name=name,defaults={'team':f'DTC {name} Team','description':f'Upcoming {name} fixtures, results and registration.'})
            Match.objects.get_or_create(sport=sport,opponent='Inter-College XI',venue='DTC Sports Ground',starts_at=timezone.now()+timedelta(days=5),defaults={'tournament':'DTC Inter-College League','registration_url':'https://example.com/register'})
        self.stdout.write(self.style.SUCCESS('DTC demo data ready. Admin: admin@dtc.ac.in / Admin@123'))
