from django.contrib import admin
from . models import *


admin.site.register([Category, Test, Question, Option, TestAttempt, TestAttemptAnswer, TestAttemptResult])
