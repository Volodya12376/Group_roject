from django.contrib.auth.mixins import UserPassesTestMixin


def can_manage_polls(user):
    if not user.is_authenticated:
        return False
    return (
        user.is_superuser
        or user.groups.filter(name="Moderator").exists()
        or user.has_perm("polls.add_poll")
        or user.has_perm("polls.change_poll")
        or user.has_perm("polls.delete_poll")
        or user.has_perm("polls.view_poll")
    )


class PollManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return can_manage_polls(self.request.user)
