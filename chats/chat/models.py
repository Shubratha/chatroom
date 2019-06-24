from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Message(models.Model):
	sender = models.ForeignKey(User, related_name='sender_messages', on_delete=models.CASCADE)
	text = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username

	def last_20_messages(self):
		return Message.objects.order_by('-timestamp').all()[:20]
