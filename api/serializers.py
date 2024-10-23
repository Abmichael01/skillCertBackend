from rest_framework import serializers
from .models import (
    Category,
    Test, TestAttempt, TestAttemptAnswer, TestAttemptResult, Question, Option
) 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "icon"]
        
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ["id", "creator", "category", "title", "slug", "duration", "banner", "difficulty", "public", "published"]

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "question", "option", "is_correct"]

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ["id", "question", "options"]
        
class TestWithQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta: 
        model = Test
        fields = ["id", "creator", "category", "title", "slug", "duration", "banner", "difficulty", "public", "published", "questions"] 

class TestAttemptAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAttemptAnswer 
        fields = ["id", "question", "selected_option"]

class AttemptAnswersSerializer(serializers.ModelSerializer):
    answers = TestAttemptAnswerSerializer(many=True, read_only=True)
    test = TestWithQuestionsSerializer(many=False, read_only=True)
    class Meta:
        model = TestAttempt
        fields = ["id", "test", "score" ,"answers"]

class TestAttemptSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=False, read_only=True)
    class Meta:
        model = TestAttempt
        fields = ["id", "user", "test"]