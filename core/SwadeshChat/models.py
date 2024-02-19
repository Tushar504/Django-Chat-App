from django.db import models
from django.contrib.auth.models import User


class ReceiverType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacted_by')
    slug = models.SlugField(max_length=10, unique=True)
    contact_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    receiver_type = models.ForeignKey(ReceiverType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=10, unique=True)
    receiver_type = models.ForeignKey(ReceiverType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class MemberType(models.Model):
    name = models.CharField(max_length=50)


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    member_type = models.ForeignKey(MemberType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
