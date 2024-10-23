from django.shortcuts import render
from django.views import View
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import json
from users.models import User
from . models import *
from . serializers import (
    CategorySerializer,
    TestSerializer,
    QuestionSerializer,
    TestWithQuestionsSerializer,
    TestAttemptSerializer,
    AttemptAnswersSerializer
)
from users.serializers import UserSerializer
from django.db.models import Q


@api_view(["GET"])
@permission_classes([AllowAny])
def categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def tests(request):
    tests = Test.objects.all()
    serializer = TestSerializer(tests, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def test(request, slug):
    test = Test.objects.get(slug=slug)
    serializer = TestSerializer(test, many=False)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(["GET"])
@permission_classes([AllowAny])
def get_test_and_questions(request, slug):
    test = Test.objects.get(slug=slug)
    
    test_serializer = TestWithQuestionsSerializer(test, many=False)
    
    data = {
        "test": test_serializer.data,
        'questions': test_serializer.data["questions"]
    }
    
    data["test"].pop("questions")
    
    
    return Response(data, status=status.HTTP_200_OK)
    

@api_view(["POST"])
def create_test(request):
    data = json.loads(request.body)
    
    title = data["title"]
    category_id = int(data["category"])
    duration = data["duration"]
    difficulty = data["difficulty"]
    public = True if data["public"] == "True" else False
    category = Category.objects.get(id=category_id)
    
    new_test = Test.objects.create(
        title=title,
        category=category,
        duration=duration,
        difficulty=difficulty,
        creator= request.user, 
        public = public, 
        published = False
        
    )
    new_test.save()
    
    serializer = TestSerializer(new_test, many=False)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def edit_test(request):
    data = json.loads(request.body)
    
    slug = data["slug"]
    title = data["title"]
    category_id = int(data["category"])
    duration = data["duration"]
    difficulty = data["difficulty"]
    public = True if data["public"] == "True" else False
    test = Test.objects.filter(slug=slug).first()
    category = Category.objects.get(id=category_id)
    print(data["public"])
    print(public)
    if request.user == test.creator and test:
        test.title = title
        test.category = category
        test.duration = duration
        test.difficulty = difficulty
        test.public = public
        test.save()
        return Response(status=status.HTTP_200_OK)
    return Response({"message": "You are not allowed to make changes to this test"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def delete_test(request):
    slug = json.loads(request.body)
    try:
        test = Test.objects.filter(slug=slug)
    except:
        return Response({"message": "Test not found"}, status=status.HTTP_404_NOT_FOUND)
    if test.creator == request.user:
        test.delete()
        return Response({"message": "Test was deleted successfully"}, status=status.HTTP_200_OK)
    return Response({"message": "You are not allowed to make changes to this test"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def add_question(request):
    data = json.loads(request.body)
    
    test_slug = data["testSlug"]
    question = data["question"]
    options = data["options"]
    
    test = Test.objects.get(slug=test_slug)
    
    if test.creator == request.user:
        new_question = Question.objects.create(
            test = test,
            question = question,
        )
        new_question.save()
        
        for option in options:
            new_option = Option.objects.create(
                question = new_question,
                option = option["option"],
                is_correct = option["is_correct"]
            )
            new_option.save()
            
        return Response(status=status.HTTP_201_CREATED)
    return Response({"message": "You are not allowed to make changes to this test"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def edit_question(request):
    data = json.loads(request.body)
    print(data)
    question_id = data["id"]
    question = data["question"]
    options = data["options"]
    option_ids = [option["id"] for option in options if "id" in option]
    
    question_object = Question.objects.get(id=question_id)
    if question_object.test.creator == request.user:
        options_object = question_object.options
        question_object.question = question
        question_object.save()
        
        options_object.exclude(id__in=option_ids).delete()
        
        for option in options:
            if "id" in option and options_object.filter(id=option["id"]).exists():
                option_object = Option.objects.get(id=option["id"])
                option_object.option = option["option"]
                option_object.is_correct  = option["is_correct"]
                option_object.save()
            else:
                new_option = Option.objects.create(
                    question = question_object,
                    option = option["option"],
                    is_correct = option["is_correct"],
                )
                new_option.save()
                
        return Response(status=status.HTTP_200_OK)
    return Response({"message": "You are not allowed to make changes to this test"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def delete_question(request):
    question_id = json.loads(request.body)
    question = Question.objects.get(id=question_id)
    if question.test.creator == request.user:
        question.delete()
        return Response(status=status.HTTP_200_OK)
    return Response({"message": "You are not allowed to make changes to this test"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def attempt_test(request):
    testId = json.loads(request.body)
    test = Test.objects.get(id=testId)
    
    new_attempt = TestAttempt.objects.create(
        test = test,
        user = request.user
    )
    new_attempt.save()
    
    serializer = TestAttemptSerializer(new_attempt, many=False)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def submit_test(request):
    data = json.loads(request.body)
    attempt_id = int(data["attemptId"])
    answers = data["answers"]
    
    test_attempt = TestAttempt.objects.get(id=attempt_id)
    score = 0  
    total_questions = test_attempt.test.questions.count() 

    
    for answer in answers:
        question = Question.objects.get(id=answer["question"])
        selected_option = Option.objects.get(id=answer["selected_option"])

        if selected_option.is_correct:
            score += 1 

        new_answer = TestAttemptAnswer.objects.create(
            test_attempt=test_attempt,
            question=question,
            selected_option=selected_option
        )
        new_answer.save()

    percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0

    test_attempt.score = percentage_score
    test_attempt.save()

    return Response({"id": test_attempt.id, "score": test_attempt.score}, status=status.HTTP_200_OK)



@api_view(["GET"])
def tests_by_user(request, pk):
    user = User.objects.get(id=pk)
    tests = Test.objects.filter(creator=user)
    serializer = TestSerializer(tests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(["POST"])
def upload_banner(request):
    banner = request.FILES.get("banner")
    slug = request.POST.get("slug")
    
    
    if not banner:
        return Response({"message": "NO image was provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        test = Test.objects.get(slug=slug)
    except Test.DoesNotExist:
        return Response({"message": "Test not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if test.creator == request.user:
        try: 
            test.banner = banner
            test.save()
        except:
            return Response({"message": "An error occured while uploading the image"}, status=status.HTTP_417_EXPECTATION_FAILED)
                
        return Response({"message": "Banner uploaded successfully"}, status=status.HTTP_200_OK)
    return Response({"message": "You are not allowed to make changes to this test"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def publish_test(request):
    slug = json.loads(request.body)["slug"]
    print(slug)
    try:
        test = Test.objects.get(slug=slug)
    except Test.DoesNotExist:
        return Response({"message": "Test not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if test.creator == request.user:
        test.published = True
        test.save()
        return Response({"public": test.public}, status=status.HTTP_200_OK)
    return Response({"message": "You are not allowed to make changes to this test"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def attempt_answers(request, pk):
    attempt = TestAttempt.objects.get(id=pk)
    
    serializer = AttemptAnswersSerializer(attempt, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def attempted_tests(request):
    user = request.user
    tests = TestAttempt.objects.filter(user=user)
    serializer = TestAttemptSerializer(tests, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def tests_by_category(request, pk):
    # page = request.GET["page"]
    category = Category.objects.get(id=pk)
    tests = Test.objects.filter(category=category)
    serializer = TestSerializer(tests, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def user_profile(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def search(request):
    query = request.GET.get("query", None)
    if query:
        tests = Test.objects.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query)
        )
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "No query provided"}, status=400)
    