import os
import django
import requests
import random
import logging

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appConfig.settings')
django.setup()

from api.models import Category, Test, Question, Option
from users.models import User

HUGGING_FACE_API_KEY = ''

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_categories():
    categories = Category.objects.all()
    return categories

def generate_test_data(category, num_tests, num_questions):
    user = User.objects.first()  # Assuming you have at least one user
    if not user:
        raise ValueError("No user found in the database.")

    for _ in range(num_tests):
        title = generate_text(f"Generate a relevant and realistic title for a test in the {category.name} category.")
        if not title:
            continue
        
        difficulty = random.choice(["S", "M", "H"])
        test = Test.objects.create(
            creator=user,
            category=category,
            title=title,
            difficulty=difficulty,
            duration=random.randint(5, 60),
            banner_img=f"https://source.unsplash.com/1600x900/?{category.name}",
        )
        
        # Generate questions for the test
        for _ in range(num_questions):
            question_text = generate_text(f"Generate a question for a {category.name} test with difficulty {difficulty}.")
            if not question_text:
                continue
            
            question = Question.objects.create(test=test, question=question_text)
            
            # Generate options for the question
            correct_option_index = random.randint(0, 3)
            for i in range(4):
                is_correct = (i == correct_option_index)
                option_text = generate_text(f"Generate an {'correct' if is_correct else 'incorrect'} option for the question: {question_text}")
                if not option_text:
                    continue
                
                Option.objects.create(question=question, option=option_text, is_correct=is_correct)

def generate_text(prompt):
    headers = {
        'Authorization': f'Bearer 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',
        'Content-Type': 'application/json'
    }
    data = {
        'inputs': prompt,
        'parameters': {
            'max_length': 100,
            'top_p': 0.95,
            'top_k': 60,
            'temperature': 0.7
        }
    }
    response = requests.post('https://api-inference.huggingface.co/models/gpt2', headers=headers, json=data)
    
    if response.status_code != 200:
        logger.error(f"Failed to generate text: {response.status_code} - {response.text}")
        return None

    result = response.json()
    
    if not isinstance(result, list) or not result:
        logger.error(f"Unexpected response format: {result}")
        return None

    return result[0].get('generated_text')

if __name__ == "__main__":
    categories = get_categories()
    num_tests_per_category = 50
    num_questions_per_test = 10

    for category in categories:
        generate_test_data(category, num_tests_per_category, num_questions_per_test)
    
    print("Test data generation complete.")
