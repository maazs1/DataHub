from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from django.db.models import Q


class ProfileManager(models.Manager):
    
    def get_all_profiles(self):
        profiles = Profile.objects.all()
        return profiles

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    description = models.TextField(max_length=500, blank=False)
    email = models.EmailField(max_length=200, blank=False)
    country = models.EmailField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatarT.png', upload_to='avatars/')
    slug = models.SlugField(unique=True, blank=True)
    link = models.TextField(blank=False)

    objects = ProfileManager()
    #followers = models.ManyToManyField(User, blank=True, related_name='followers')
    #liked = models.ManyToManyField(User, blank=True, related_name='likes')

    # install pillow
    #create media_root
    # find avatr.png

    # def __str__(self):
    #     return f"{self.user.username}-{self.created}"
    # def num_likes(self):
    #     return self.liked.all().count()

    # def get_followers(self):
    #     return self.followers.all()

    # def get_followers_no(self):
    #     return self.followers.all().count()

    def get_absolute_url(self):
        return reverse("homepage:profile-detail-view", kwargs={"slug": self.slug})

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)