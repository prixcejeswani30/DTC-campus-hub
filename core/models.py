from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPER = 'SUPER_ADMIN', 'Super Admin'
        CLUB = 'CLUB_ADMIN', 'Club Admin'
        SOCIETY = 'SOCIETY_ADMIN', 'Society Admin'
        STUDENT = 'STUDENT', 'Student'
    username = models.EmailField(unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)
    university = models.CharField(max_length=20, blank=True)
    course = models.CharField(max_length=120, blank=True)
    branch = models.CharField(max_length=120, blank=True)
    semester = models.PositiveIntegerField(null=True, blank=True)
    avatar = CloudinaryField('avatar', blank=True, null=True, asset_folder='dtc-campus-hub/avatars')
    bio = models.TextField(blank=True)
    notifications_enabled = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.username = self.email.lower().strip()
        super().save(*args, **kwargs)

class Organization(models.Model):
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    short_name = models.CharField(max_length=60, blank=True)
    tagline = models.CharField(max_length=220, blank=True)
    description = models.TextField(blank=True)
    logo = CloudinaryField('logo', blank=True, null=True, asset_folder='dtc-campus-hub/organizations/logos')
    cover = CloudinaryField('cover', blank=True, null=True, asset_folder='dtc-campus-hub/organizations/covers')
    contact_email = models.EmailField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)
    coordinator = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Club(Organization):
    domains = models.CharField(max_length=250, blank=True)

class Society(Organization):
    category = models.CharField(max_length=120, blank=True)

class Membership(models.Model):
    class MemberRoles(models.TextChoices):
        MEMBER='MEMBER','Member'
        COORDINATOR='COORDINATOR','Coordinator'
        LEAD='LEAD','Lead'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=MemberRoles.choices, default=MemberRoles.MEMBER)
    title = models.CharField(max_length=120, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','organization')

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','organization')

class NewsPost(models.Model):
    class Status(models.TextChoices):
        DRAFT='DRAFT','Draft'; PENDING='PENDING','Pending approval'; PUBLISHED='PUBLISHED','Published'
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.CharField(max_length=320, blank=True)
    content = models.TextField()
    image = CloudinaryField('image', blank=True, null=True, asset_folder='dtc-campus-hub/news')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='news_posts')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='news')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-published_at','-created_at']
    def save(self,*args,**kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args,**kwargs)

class Event(models.Model):
    class Status(models.TextChoices):
        UPCOMING='UPCOMING','Upcoming'; LIVE='LIVE','Live now'; COMPLETED='COMPLETED','Completed'; CANCELLED='CANCELLED','Cancelled'
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    poster = CloudinaryField('poster', blank=True, null=True, asset_folder='dtc-campus-hub/events')
    organizer = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    venue = models.CharField(max_length=220)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    registration_url = models.URLField(blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPCOMING)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['starts_at']
    def save(self,*args,**kwargs):
        if not self.slug: self.slug=slugify(self.title)
        super().save(*args,**kwargs)

class EventRegistration(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='registrations')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=('event','user')

class MediaItem(models.Model):
    class Kinds(models.TextChoices): PHOTO='PHOTO','Photo'; VIDEO='VIDEO','Video'
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='media')
    title=models.CharField(max_length=160)
    image=CloudinaryField('image',blank=True,null=True,asset_folder='dtc-campus-hub/gallery')
    video_url=models.URLField(blank=True)
    caption=models.CharField(max_length=300,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class AcademicResource(models.Model):
    class Universities(models.TextChoices): GGSIPU='GGSIPU','GGSIPU'; AKTU='AKTU','AKTU'
    class Types(models.TextChoices): SYLLABUS='SYLLABUS','Syllabus'; EXAM='EXAM','Exam dates'; CALENDAR='CALENDAR','Academic calendar'; NOTICE='NOTICE','Notice'; RESULT='RESULT','Result'; STUDY='STUDY','Study resource'
    title=models.CharField(max_length=220)
    university=models.CharField(max_length=20,choices=Universities.choices)
    course=models.CharField(max_length=160,blank=True)
    branch=models.CharField(max_length=160,blank=True)
    semester=models.PositiveIntegerField(null=True,blank=True)
    resource_type=models.CharField(max_length=20,choices=Types.choices)
    description=models.TextField(blank=True)
    file=models.FileField(upload_to='academics/',blank=True,null=True)
    external_url=models.URLField(blank=True)
    published_at=models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    title=models.CharField(max_length=220)
    message=models.CharField(max_length=500)
    url=models.CharField(max_length=300,blank=True)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

class Cafe(models.Model):
    name=models.CharField(max_length=120)
    location=models.CharField(max_length=220,blank=True)
    opening_hours=models.CharField(max_length=120,blank=True)
    menu=models.TextField(blank=True)
    prices=models.TextField(blank=True)
    image=CloudinaryField('image',blank=True,null=True,asset_folder='dtc-campus-hub/cafeteria')
    is_mess=models.BooleanField(default=False)

class Sport(models.Model):
    name=models.CharField(max_length=100)
    team=models.CharField(max_length=160,blank=True)
    description=models.TextField(blank=True)
    image=CloudinaryField('image',blank=True,null=True,asset_folder='dtc-campus-hub/sports')

class Match(models.Model):
    sport=models.ForeignKey(Sport,on_delete=models.CASCADE,related_name='matches')
    opponent=models.CharField(max_length=160)
    venue=models.CharField(max_length=220)
    starts_at=models.DateTimeField()
    tournament=models.CharField(max_length=180,blank=True)
    result=models.CharField(max_length=160,blank=True)
    registration_url=models.URLField(blank=True)
    notice=models.TextField(blank=True)

class SiteSetting(models.Model):
    key=models.CharField(max_length=80,unique=True)
    value=models.TextField(blank=True)
    class Meta: verbose_name='Site setting'; verbose_name_plural='Site settings'
