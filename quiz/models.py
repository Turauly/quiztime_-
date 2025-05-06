from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ScheduleEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=[
        ('Дүйсенбі', 'Дүйсенбі'),
        ('Сейсенбі', 'Сейсенбі'),
        ('Сәрсенбі', 'Сәрсенбі'),
        ('Бейсенбі', 'Бейсенбі'),
        ('Жұма', 'Жұма'),
        ('Сенбі', 'Сенбі'),
    ])
    time = models.TimeField()
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.day} | {self.time.strftime('%H:%M')} | {self.subject}"


class SuggestedQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text[:50]


class QuizResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    user_answer = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question}"


class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'дұрыс' if self.is_correct else 'қате'})"



class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    youtube_url = models.URLField()

    def __str__(self):
        return self.title
