from django.db import models




# Create your models here. 
  
class AudioData(models.Model): 
    user_id=models.TextField(primary_key=True,max_length=8000)
    offset_in_milliseconds = models.TextField()
    index=models.TextField()
    has_previous_playback_session=models.BooleanField(default=False)
    in_playback_session=models.BooleanField(default=False)
    is_playback=models.BooleanField(default=False)
    
