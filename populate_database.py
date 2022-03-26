import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'inquizitive_wad2_project.settings')
import django
django.setup()

# from django.core.files import File
from inquizitive.models import UserProfile, Quiz
from django.contrib.auth.models import User


def add_quiz(name: str, subject: str, difficulty: str, questions: dict, description: str, comments: dict, rating: list):
    q = Quiz.objects.get_or_create(name=name, subject=subject, difficulty=difficulty, questions=questions,
                                   description=description, comments=comments, rating=rating)[0]


def add_user(username: str, complete_quizzes: dict, score: list, rated_quizzes: dict, password: str, email: str,
             name: str):
    u = User.objects.get_or_create(username=username, complete_quizzes=complete_quizzes, score=score,
                                          rated_quizzes=rated_quizzes,
                                          password=password, email=email, name=name)

    # Add image to user's profile

    # Add quiz ratings
    for quiz in rated_quizzes.keys():
        rates(name, quiz)

    for quiz in complete_quizzes:
        score(name, quiz)

    return u


def rates(user: str, quiz: str):
    # Create a link between the user and the quiz.
    user_obj = UserProfile.objects.get(name=user)
    quiz_obj = Quiz.objects.get(quiz=quiz)

    user_obj.rates.add(quiz_obj)
    # Append rating to ratings list.
    quiz_obj.ratings.append(user_obj.rated_quizzes[quiz_obj.quiz])
    quiz_obj.save()


def populate():
    # Quiz data, list of dictionaries?
    quiz_data = [
        {"name": "Biology 101", "subject": "Biology", "difficulty": "Easy",
         "questions": [{"question": "What is the powerhouse of the cell?",
                        "choices": ["The Nucleus", "The Mitochondria", "The Membrane", "Tiny"], "correct_index": 1},
                       {"question": "What organ pumps blood around the body?",
                        "choices": ["The Liver", "The Brain", "The Kidneys", "The Heart"], "correct_index": 3},
                       {"question": "Who discovered penicillin?",
                        "choices": ["Andy Warhol", "Nikolas Tesla", "Alexander Fleming", "Adam Smith"],
                        "correct_index": 2},
                       {"question": "What is the human body's largest organ?",
                        "choices": ["The Brain", "The Heart", "The Skin", "The Ego"], "correct_index": 2},
                       {"question": "Botany is the study of what life form?",
                        "choices": ["Plants", "Diseases", "Crustaceans", "Mammals"]}],
         "description": "Quick general biology quiz.",
         "comments": {}, "rating": []},

        {"name": "General Knowledge", "subject": "General", "difficulty": "Medium",
         "questions": [{"question": "What is the world's largest land mammal?",
                        "choices": ["Elephant", "Giraffe", "Yeti", "Giant camel"], "correct_index": 0},
                       {"question": "The first atomic bomb was dropped on which Japanese city?",
                        "choices": ["Nagasaki", "Kyoko", "Tokyo", "Hiroshima"], "correct_index": 3},
                       {"question": "How many of Henry VIII's wives were called Anne?",
                        "choices": ["One", "Two", "Four", "Six"], "correct_index": 1},
                       {"question": "What was the middle name of Wolfgang Mozart?",
                        "choices": ["Georg", "Heinrich", "Amadeus", "Maddeus"], "correct_index": 2},
                       {"question": "Which middle eastern city is also the name of an artichoke?",
                        "choices": ["Jerusalem", "Istanbul", "Ankara", "Izmir"], "correct_index": 0},
                       {"question": "In mythology, Romulus and Remus were brought up by which animal?",
                        "choices": ["Lion", "Bear", "Tiger", "Wolf"], "correct_index": 3},
                       {"question": "Nostradamus was famous for making what?",
                        "choices": ["Cakes", "Potions", "Predictions", "Enchantments"], "correct_index": 2},
                       ],
         "description": "Short general knowledge quiz.", "comments": {}, "rating": []},

        {"name": "Sports Trivia", "subject": "Sports", "difficulty": "Medium",
         "questions": [{
             "question": "Who became the first driver to win the first four races of a Formula One grand prix season in 1991?",
             "choices": ["Lewis Hamilton", "Fernando Alonso", "Ayrton Senna", "Michael Schumacher"],
             "correct_index": 2},
             {
                 "question": "Which brothers have held boxing World Heavyweight titles in the twenty-first century?",
                 "choices": ["The Klitschko Brothers", "The Wright Brothers", "The Kennedy Brothers",
                             "The Kray Brothers"], "correct_index": 0},
         ],
         "description": "Test your sports knowledge with this quiz!", "comments": {}, "rating": []},

        {"name": "Shakespeare Quiz", "subject": "Literature", "difficulty": "Hard",
         "questions": [{"question": "How many plays did Shakespeare write?",
                        "choices": ["36", "42", "37", "47"], "correct_index": 2},
                       {"question": "How many sonnets did Shakespeare write?",
                        "choices": ["32", "150", "54", "154"], "correct_index": 3},
                       {"question": "What is Shakespeare's Venus and Adonais?",
                        "choices": ["A Tragedy", "A Comedy", "A Narrative Poem", "A Romance"], "correct_index": 2},
                       {"question": "Who called Shakespeare 'an upstart crow beautified with our feathers?'",
                        "choices": ["Robert Greene", "Thomas Kyd", "George Peele", "John Lyly"], "correct_index": 0},
                       {"question": "Who said, 'Shakespeare has only heroines and no heroes'?",
                        "choices": ["Sidney", "Ruskin", "Ben Jonson", "Marlowe"], "correct_index": 1},
                       {"question": "The well-know phrase 'What's in a name' occurs in which of the following?",
                        "choices": ["Othello", "Hamlet", "Julius Caesar", "Romeo and Juliet"], "correct_index": 3},
                       ],
         "description": "How well do you know the bard?", "comments": {}, "rating": []}
    ]


if __name__ == "__main__":
    print("Starting population script...")
    populate()

    print("Population completed.")
