from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) #One to one relationship with user model
    #Now a user is associated with this profile.

    #Now you can add extra fields ontop of the fields already included in the User model
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #Run the original save method of the parent class

        img = Image.open(self.image.path) #Open image of the current instance

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) #resize image
            img.save(self.image.path)

