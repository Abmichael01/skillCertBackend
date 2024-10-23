import random
from faker import Faker
from django.core.management.base import BaseCommand
from api.models import Category, Test, Question, Option
from users.models import User

fake = Faker()

def generate_test_data(num_tests_per_category, num_questions_per_test):
    categories = Category.objects.all()
    users = User.objects.all()

    for category in categories:
        for _ in range(num_tests_per_category):
            user = random.choice(users)
            test_title = generate_test_title(category.name)
            test = Test(
                creator=user,
                category=category,
                title=test_title,
                difficulty=random.choice(["S", "M", "H"]),
                duration=random.randint(5, 60),
                banner_img=fake.image_url(width=800, height=400)
            )
            test.save()  # Ensure the slug and other fields are processed
            generate_questions(test, num_questions_per_test)

def generate_test_title(category_name):
    return f"{fake.word().title()} {category_name} Test"

def generate_questions(test, num_questions):
    for _ in range(num_questions):
        question_text = fake.sentence()
        question = Question(
            test=test,
            question=question_text
        )
        question.save()
        generate_options(question)

def generate_options(question):
    correct_option_index = random.randint(0, 3)
    for i in range(4):
        option = Option(
            question=question,
            option="Correct Option" if i == correct_option_index else fake.word(),
            is_correct=i == correct_option_index
        )
        option.save()

class Command(BaseCommand):
    help = 'Generate test data for the Test app'

    def handle(self, *args, **kwargs):
        num_tests_per_category = 10  # Adjust as needed
        num_questions_per_test = 10  # Adjust as needed
        generate_test_data(num_tests_per_category, num_questions_per_test)
        self.stdout.write(self.style.SUCCESS('Test data generated successfully'))
