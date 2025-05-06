from .models import SuggestedQuestion
from django import forms
from .models import ScheduleEntry

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = ScheduleEntry
        fields = ['day', 'time', 'subject']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Пән атауы'}),
        }


class SuggestedQuestionForm(forms.ModelForm):
    class Meta:
        model = SuggestedQuestion
        fields = ['question_text', 'correct_answer']
        labels = {
            'question_text': 'Сұрақ мәтіні',
            'correct_answer': 'Дұрыс жауап',
        }
