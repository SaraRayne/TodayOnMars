from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=25, default=None)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.category}"


class Thread(models.Model):
    title = models.CharField(max_length=64, default=None)
    content = models.TextField(default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name="categories", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.poster.username,
            "content": self.content,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "category": self.category.category
        }


class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="replies")
    reply = models.TextField(default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"

    def serialize(self):
        return {
            "id": self.id,
            "thread": self.thread.id,
            "author": self.author.username,
            "reply": self.reply,
            "date": self.date.strftime("%b %d %Y, %I:%M %p")
        }
