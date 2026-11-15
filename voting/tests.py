from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Poll, PollOption, PollVote


User = get_user_model()


class VotingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.poll = Poll.objects.create(
            title="Улюблена гра",
            is_active=True,
            allow_revote=False
        )

        self.option1 = PollOption.objects.create(
            poll=self.poll,
            text="Minecraft",
            order=1
        )

        self.option2 = PollOption.objects.create(
            poll=self.poll,
            text="Roblox",
            order=2
        )

        self.vote_url = reverse(
            "vote",
            args=[self.poll.pk]
        )

    def test_user_cannot_vote_twice(self):
        self.client.force_login(self.user)

        self.client.post(
            self.vote_url,
            {"choice": self.option1.pk}
        )

        self.client.post(
            self.vote_url,
            {"choice": self.option2.pk}
        )

        self.assertEqual(
            PollVote.objects.filter(
                poll=self.poll,
                user=self.user
            ).count(),
            1
        )

        vote = PollVote.objects.get(
            poll=self.poll,
            user=self.user
        )

        self.assertEqual(vote.option, self.option1)

    def test_user_can_change_vote(self):
        self.poll.allow_revote = True
        self.poll.save()

        self.client.force_login(self.user)

        self.client.post(
            self.vote_url,
            {"choice": self.option1.pk}
        )

        self.client.post(
            self.vote_url,
            {"choice": self.option2.pk}
        )

        self.assertEqual(
            PollVote.objects.filter(
                poll=self.poll,
                user=self.user
            ).count(),
            1
        )

        vote = PollVote.objects.get(
            poll=self.poll,
            user=self.user
        )

        self.assertEqual(vote.option, self.option2)

    def test_anonymous_user_cannot_vote(self):
        response = self.client.post(
            self.vote_url,
            {"choice": self.option1.pk}
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            PollVote.objects.filter(poll=self.poll).count(),
            0
        )