from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) #One to one relationship with user model
    #Now a user is associated with this profile.

    #Now you can add extra fields ontop of the fields already included in the User model
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

