from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q,F



class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name="followings", blank=True)
    # def save(self, *args, **kwargs):
    #     # Check if a follower of an user is indeed that user
    #     # Save the changes
    #     # super(User, self).save(*args, **kwargs)   
    #     print(1)
    #     # Check the followers at the time it's saved
    #     print(self.followers.all())
    #     # Check if the object is existed in that object's followers field
    #     if self.followers.filter(pk=self.pk).exists():
    #         follower = self.followers.get(pk=self.pk)
    #         print(follower)
    #         # If right, remove that object from followers field
    #         self.followers.remove(follower)
    #         print(2)
    #         # Check the followers field again to make sure the object is not there    
    #         print(self.followers.all())
    #         # # Raise the error
    #         # raise ValueError("A user cannot be a follower of themselves.")
        
class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, related_name="liked_posts")
    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "content": self.content,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            
        }
    def serialize_like_post(self):
        return {
            "id": self.id,
            "likes": [liker.username for liker in self.likes.all()],
            "number_likes": self.likes.count(),
        }


    