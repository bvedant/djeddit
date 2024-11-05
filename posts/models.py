from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid
from django.urls import reverse


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_posts', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create base slug from title
            base_slug = slugify(self.title)
            
            # Truncate the slug to 50 chars max (leaving room for UUID)
            truncated_slug = base_slug[:40]
            
            # Remove trailing hyphen if exists
            truncated_slug = truncated_slug.rstrip('-')
            
            # Add UUID slice for uniqueness (first 8 characters)
            uuid_slice = str(self.id)[:8]
            self.slug = f"{truncated_slug}-{uuid_slice}"
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
