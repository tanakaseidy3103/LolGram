from django.db import models
from django.contrib.auth.models import User
from PIL import Image


def user_avatar_path(instance, filename):
    return f'profile_pics/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_avatar_path, 
        null=True, 
        blank=True, 
        default='profile_pics/default_avatar.png'
    )
    face_image = models.ImageField(
        upload_to='face_recognition',
        null=True,
        blank=True
    )
    face_recognition_enabled = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        
        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
            except Exception as e:
                print(f"Error processing image: {e}")

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'