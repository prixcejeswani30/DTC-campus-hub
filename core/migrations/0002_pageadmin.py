from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies=[('core','0001_initial')]
    operations=[migrations.CreateModel(
        name='PageAdmin',
        fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('page',models.CharField(choices=[('NEWS','News'),('EVENTS','Events'),('ACADEMICS','Academics'),('CAMPUS','Campus Life'),('SPORTS','Sports')],max_length=20)),
            ('created_at',models.DateTimeField(auto_now_add=True)),
            ('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='page_admin_assignments',to=settings.AUTH_USER_MODEL)),
        ],
        options={'ordering':['page','user__email'],'unique_together':{('user','page')}},
    )]
