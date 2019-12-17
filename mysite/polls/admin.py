from django.contrib import admin

from .models import Question, Choice

'''
1.(app_name)/admin.py helps to keep track of all models used in a particular app
2. Provides a friendly UI via the browser to CRUD each of the fields in the model
3. The browser layout can be further customized through a user-defined class (eg QuestionAdmin)
'''
admin.site.register(Question)
admin.site.register(Choice)