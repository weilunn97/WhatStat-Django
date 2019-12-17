from django.db import models
from django.utils import timezone
import datetime

'''
1. Models are simply classes which function as database TABLES for information storage
2. Again, models are app-specific. Each app will have its own model(s)
3. The database defaults to sqlite (changeable in settings.py)
4. Each time a model is added, we follow 3 KEY STEPS in the terminal
(i) [ONLY ONCE] Install the app on your site (settings.py > INSTALLED_APPS = [...])
(ii) Make migrations (python manage.py makemigrations) - Generates the SQL 
statements (depending on what type of changes (CRUD) were made to your model(s)
(iii) Perform migrations (python manage.py migrate) - Executes the SQL statements
(iv) Register your models with the admin interface (polls/admin.py)
5. Performing migrations is only essential if you alter the UNDERLYING TABLE 
STRUCTURE (eg. create, remove fields)
'''


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now())

    # RETURN STRING TEXT
    def __str__(self):
        return self.question_text

    # RETURN BOOLEAN
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # RETURN STRING TEXT
    def __str__(self):
        return self.choice_text


'''WHATSAPP PROJECT MODELS'''
class FileProcessing(models.Model):
    uploadedFile = models.FileField(null=True, blank=True)
    fileContents = models.TextField()
    # fileContentLines = models.

    def __str__(self):
        return self.uploadedFile.name
