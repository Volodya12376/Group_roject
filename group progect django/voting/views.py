
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db import IntegrityError, transaction
from .models import Poll, PollOption, PollVote


def poll_list(request):
    polls = Poll.objects.filter(is_active=True)
    return render(request, "voting/poll_list.html", {
        "polls": polls,
    })


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, is_active=True)
    return render(request, "voting/poll_detail.html", {
        "poll": poll,
    })



    
class VoteView(LoginRequiredMixin, View):
    def post(self, request, poll_id):
        poll = get_object_or_404(
            Poll, pk=poll_id, is_active=True
        )
        now = timezone.now()

        if poll.starts_at and now < poll.starts_at:
            messages.error(request, "Голосування ще не почалося.")
            return redirect("poll_detail", poll_id=poll_id)

        if poll.ends_at and now > poll.ends_at:
            messages.error(request, "Голосування вже завершено.")
            return redirect("poll_detail", poll_id=poll_id)

        option = get_object_or_404(
            PollOption,
            pk=request.POST.get("choice"),
            poll=poll,
        )

        try:
            with transaction.atomic():
                existing_vote = PollVote.objects.filter(
                    poll=poll,
                    user=request.user,
                ).first()

                if existing_vote:
                    if not poll.allow_revote:
                        messages.error(request, "Ти вже проголосував.")
                        return redirect("results", poll_id=poll.pk)

                    existing_vote.option = option
                    existing_vote.full_clean()
                    existing_vote.save()
                else:
                    new_vote = PollVote(
                        poll=poll,
                        user=request.user,
                        option=option,
                    )
                    new_vote.full_clean()
                    new_vote.save()

        except IntegrityError:
            messages.error(request, "Ти вже проголосував.")
            return redirect("results", poll_id=poll.pk)

        return redirect("results", poll_id=poll.pk)



def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, is_active=True)

    if not poll.show_results and not request.user.is_staff:
        messages.info(request, "Результати доступні не всім.")
        return redirect("poll_detail", poll_id=poll.pk)

    total_votes = PollVote.objects.filter(poll=poll).count()
    options = poll.options.all()

    for option in options:
        option.vote_count = option.votes.count()
        option.percent = (
            round(option.vote_count / total_votes * 100, 1)
            if total_votes else 0
        )

    return render(request, "voting/results.html", {
        "poll": poll,
        "options": options,
        "total_votes": total_votes,
    })


def add_poll(request):
    return redirect("/admin/voting/poll/add/")


def delete_poll(request, poll_id):
    return redirect("/admin/voting/poll/")
