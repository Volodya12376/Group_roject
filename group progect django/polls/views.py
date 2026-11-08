from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView, TemplateView, CreateView, UpdateView, DeleteView

from .forms import AnswerForm, PollForm
from .models import Poll, PollAttempt, Answer, Question
from .permissions import PollManagerRequiredMixin


class PollListView(LoginRequiredMixin, ListView):
    model = Poll
    template_name = "polls/poll_list.html"
    context_object_name = "polls"

    def get_queryset(self):
        return Poll.objects.filter(is_published=True).prefetch_related("questions")


class PollDetailView(LoginRequiredMixin, DetailView):
    model = Poll
    template_name = "polls/poll_detail.html"
    context_object_name = "poll"

    def get_queryset(self):
        return Poll.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attempt"] = PollAttempt.objects.filter(
            poll=self.object, user=self.request.user
        ).first()
        context["question_count"] = self.object.questions.count()
        return context


class PollStepView(LoginRequiredMixin, FormView):
    template_name = "polls/poll_step.html"
    form_class = AnswerForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        self.poll = get_object_or_404(Poll, pk=kwargs["poll_id"], is_published=True)
        self.questions = list(self.poll.questions.prefetch_related("choices"))
        if not self.questions:
            messages.error(request, "У цьому опитуванні ще немає запитань.")
            return redirect("polls:poll-detail", pk=self.poll.pk)
        self.step = kwargs["step"]
        if self.step < 1 or self.step > len(self.questions):
            raise Http404("Такого етапу опитування немає.")
        self.attempt, created = PollAttempt.objects.get_or_create(
            poll=self.poll, user=request.user,
            defaults={"status": PollAttempt.STATUS_IN_PROGRESS},
        )
        if self.attempt.status == PollAttempt.STATUS_COMPLETED:
            return redirect("polls:poll-detail", pk=self.poll.pk)
        self.question = self.questions[self.step - 1]
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["question"] = self.question
        answer = Answer.objects.filter(attempt=self.attempt, question=self.question).first()
        if answer and not kwargs.get("data"):
            kwargs["initial"] = {"choice": answer.choice_id}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "poll": self.poll,
            "question": self.question,
            "step": self.step,
            "total_steps": len(self.questions),
        })
        return context

    def form_valid(self, form):
        choice = form.cleaned_data.get("choice")
        if choice and choice.question_id != self.question.id:
            form.add_error("choice", "Неприпустимий варіант відповіді.")
            return self.form_invalid(form)
        with transaction.atomic():
            if choice:
                Answer.objects.update_or_create(
                    attempt=self.attempt, question=self.question,
                    defaults={"choice": choice},
                )
            else:
                Answer.objects.filter(attempt=self.attempt, question=self.question).delete()

        if self.step < len(self.questions):
            return redirect("polls:poll-step", poll_id=self.poll.pk, step=self.step + 1)

        if self.poll.questions.filter(required=True).exclude(
            id__in=self.attempt.answers.values_list("question_id", flat=True)
        ).exists():
            messages.error(self.request, "Будь ласка, дайте відповіді на всі обов'язкові запитання.")
            return redirect("polls:poll-step", poll_id=self.poll.pk, step=1)

        self.attempt.status = PollAttempt.STATUS_COMPLETED
        self.attempt.completed_at = timezone.now()
        self.attempt.save(update_fields=["status", "completed_at"])
        messages.success(self.request, "Опитування завершено!")
        return redirect("polls:my-result", pk=self.poll.pk)


class MyPollResultView(LoginRequiredMixin, TemplateView):
    template_name = "polls/my_result.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        self.poll = get_object_or_404(Poll, pk=kwargs["pk"])
        self.attempt = get_object_or_404(
            PollAttempt, poll=self.poll, user=request.user,
            status=PollAttempt.STATUS_COMPLETED,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["poll"] = self.poll
        context["attempt"] = self.attempt
        context["answers"] = self.attempt.answers.select_related("question", "choice").order_by("question__order")
        context["answered_count"] = self.attempt.answers.count()
        context["question_count"] = self.poll.questions.count()
        return context


class RetakePollView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=kwargs["pk"], is_published=True)
        with transaction.atomic():
            attempt = PollAttempt.objects.filter(poll=poll, user=request.user).first()
            if attempt:
                attempt.answers.all().delete()
                attempt.status = PollAttempt.STATUS_IN_PROGRESS
                attempt.completed_at = None
                attempt.save(update_fields=["status", "completed_at"])
            else:
                PollAttempt.objects.create(poll=poll, user=request.user)
        return redirect("polls:poll-step", poll_id=poll.pk, step=1)


class ManageResultsView(LoginRequiredMixin, PollManagerRequiredMixin, ListView):
    model = PollAttempt
    template_name = "polls/results_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        qs = PollAttempt.objects.select_related("poll", "user").prefetch_related("answers")
        poll_id = self.request.GET.get("poll")
        if poll_id:
            qs = qs.filter(poll_id=poll_id)
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["polls"] = Poll.objects.all()
        return context


class PollManageListView(LoginRequiredMixin, PollManagerRequiredMixin, ListView):
    model = Poll
    template_name = "polls/manage_list.html"
    context_object_name = "polls"


class PollCreateView(LoginRequiredMixin, PollManagerRequiredMixin, CreateView):
    model = Poll
    form_class = PollForm
    template_name = "polls/poll_form.html"
    success_url = reverse_lazy("polls:manage-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Опитування створено. Тепер додайте запитання та варіанти відповідей в адмінпанелі.")
        return super().form_valid(form)


class PollUpdateView(LoginRequiredMixin, PollManagerRequiredMixin, UpdateView):
    model = Poll
    form_class = PollForm
    template_name = "polls/poll_form.html"
    success_url = reverse_lazy("polls:manage-list")


class PollDeleteView(LoginRequiredMixin, PollManagerRequiredMixin, DeleteView):
    model = Poll
    template_name = "polls/poll_confirm_delete.html"
    success_url = reverse_lazy("polls:manage-list")


class ManageAttemptDetailView(LoginRequiredMixin, PollManagerRequiredMixin, DetailView):
    model = PollAttempt
    template_name = "polls/poll_result.html"
    context_object_name = "attempt"

    def get_queryset(self):
        return PollAttempt.objects.select_related("poll", "user").prefetch_related(
            "answers__question", "answers__choice"
        )


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
