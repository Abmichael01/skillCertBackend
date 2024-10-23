from django.db import models
from users.models import User
from django.utils.text import slugify
import random
import string

 
class Category(models.Model):
    name = models.CharField(max_length=225) 
    icon = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Test(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tests")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tests")
    title = models.CharField(max_length=225)
    public = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    difficulty = models.CharField(max_length=2, default="S")
    duration = models.IntegerField(default=5)
    banner = models.ImageField(upload_to="SkillCert", default="", blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Test.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{self.get_random_string()}"
        super().save(*args, **kwargs)

    def get_random_string(self, length=5):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    
    def __str__(self):
        return self.title
        
    
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions", null=True)
    question = models.TextField()
    
    def __str__(self):
        return self.question
    
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options", null=True)
    option = models.CharField(max_length=225)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.option

    
class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_attempts")
    test = models.ForeignKey(Test, on_delete=models.PROTECT, related_name="test_attempts")
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=55)
    
    def __str__(self):
        return f"{str(self.user.username)} - {str(self.test.title)}"
    
class TestAttemptAnswer(models.Model):
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{str(self.test_attempt)} - {str(self.question)}"
    
class TestAttemptResult(models.Model):
    test_attempt = models.OneToOneField(TestAttempt, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    incorrect_answers = models.IntegerField()
    skipped_questions = models.IntegerField()
    
    
    
    
