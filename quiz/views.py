from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, QuizResponse, ScheduleEntry
from .forms import SuggestedQuestionForm, ScheduleForm
from .models import Course  # 🟢 Course моделін импорттаңыз

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'quiz/course_list.html', {'courses': courses})


# 🔒 Басты бет
@login_required
def home(request):
    return render(request, 'home.html')


# 🎯 Викторина
@login_required
def quiz_view(request):
    if request.method == 'POST':
        correct = 0
        total = 0
        answers_feedback = []

        for key, value in request.POST.items():
            if key.startswith('question_'):
                qid = int(key.split('_')[1])
                question = Question.objects.get(id=qid)
                selected_answer = question.answers.get(id=int(value))
                correct_answer = question.answers.get(is_correct=True)

                # Жауапты сақтау
                QuizResponse.objects.create(
                    user=request.user,
                    question=question.text,
                    user_answer=selected_answer.text,
                    correct_answer=correct_answer.text,
                    is_correct=selected_answer.is_correct
                )

                answers_feedback.append({
                    'question': question.text,
                    'selected': selected_answer.text,
                    'correct': correct_answer.text,
                    'is_correct': selected_answer.is_correct
                })

                if selected_answer.is_correct:
                    correct += 1
                total += 1

        return render(request, 'quiz/result.html', {
            'score': correct,
            'total': total,
            'answers_feedback': answers_feedback
        })

    questions = Question.objects.all()
    return render(request, 'quiz/quiz.html', {'questions': questions})


# 📊 Статистика
@login_required
def statistics_view(request):
    responses = QuizResponse.objects.filter(user=request.user)
    total = responses.count()
    correct = responses.filter(is_correct=True).count()
    incorrect = total - correct

    return render(request, 'quiz/statistics.html', {
        'total': total,
        'correct': correct,
        'incorrect': incorrect
    })


# ❓ Сұрақ ұсыну
@login_required
def suggest_question_view(request):
    if request.method == 'POST':
        form = SuggestedQuestionForm(request.POST)
        if form.is_valid():
            suggested = form.save(commit=False)
            suggested.user = request.user
            suggested.save()
            return render(request, 'quiz/success.html')
    else:
        form = SuggestedQuestionForm()
    return render(request, 'quiz/suggest_question.html', {'form': form})


# 🗓 Кестені көру және қосу
@login_required
def schedule_view(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('schedule')
    else:
        form = ScheduleForm()

    schedule = ScheduleEntry.objects.filter(user=request.user).order_by('day', 'time')
    return render(request, 'quiz/schedule.html', {'form': form, 'schedule': schedule})


# ✏️ Кестені өңдеу
@login_required
def edit_schedule(request, pk):
    entry = get_object_or_404(ScheduleEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        form = ScheduleForm(instance=entry)
    return render(request, 'quiz/edit_schedule.html', {'form': form})


# ❌ Кестені өшіру
@login_required
def delete_schedule(request, pk):
    entry = get_object_or_404(ScheduleEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('schedule')
    return render(request, 'quiz/delete_confirm.html', {'entry': entry})
