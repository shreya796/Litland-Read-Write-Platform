
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.conf import settings


def upload_location(instance,filename):
    return "%s/%s"%(instance.id,filename)

class Post(models.Model):
   # author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1) # to associate a post with a user which may or may not be admin
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True, default=None)
    category = models.ForeignKey('blog.Category', related_name='posts')
    drafts = models.BooleanField(default=False)
    publish=models.DateField(auto_now=False,auto_now_add=False)  #this is the to publish date
    image=models.ImageField(upload_to=upload_location,null=True,blank=True,width_field="width_field",height_field="height_field")
    width_field=models.IntegerField(default=0)
    height_field=models.IntegerField(default=0)
    #image=models.FileField(null=True, blank=True)


    def get_absolute_url(self):
        return reverse('view:post_detail',kwargs={'pk':self.pk})


"""
    def publish(self):
        self.published_date = timezone.now()
        self.cleaned_data['award_grant_date'] = None
        self.save()

    def __str__(self):
        return self.title
"""


class Category(models.Model):
    category_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.category_type

