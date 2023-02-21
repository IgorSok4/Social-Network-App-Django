from django.db import models
from django.contrib.auth.models import User

class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    
    class Meta:
        ordering = ('-created',)