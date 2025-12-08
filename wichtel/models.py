import random
from datetime import datetime

from django.conf import settings
from django.db import models, transaction
from django.db.models import CheckConstraint, F, Q, UniqueConstraint


def generate_assignments(user_ids: list[int]) -> list[tuple[int, int]]:
    """
    Generate gift assignments where each user gives to exactly one other user.

    Args:
        user_ids: List of user IDs to include in the drawing

    Returns:
        List of (giver_id, receiver_id) tuples

    Raises:
        ValueError: If fewer than 2 users (can't do a drawing with 1 person)
    """
    if len(user_ids) < 2:
        raise ValueError("Need at least 2 users for a drawing")

    # Alternative (simpler, also uniform): rejection sampling on full permutation
    #   while True:
    #       perm = random.sample(user_ids, len(user_ids))
    #       if all(g != r for g, r in zip(user_ids, perm)):
    #           return list(zip(user_ids, perm))

    while True:  # Retry if we get stuck
        available = set(user_ids)
        assignments = []

        for giver in user_ids:
            choices = available - {giver}
            if not choices:
                break  # Stuck, restart
            receiver = random.choice(list(choices))
            assignments.append((giver, receiver))
            available.remove(receiver)
        else:
            return assignments  # Success, all assigned


class Drawing(models.Model):
    year = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Drawing {self.year}"

    @classmethod
    def current(cls):
        """Get the drawing for the current year."""
        return cls.objects.get(year=datetime.now().year)

    @classmethod
    def create_with_assignments(cls, year: int, assignments: list[tuple[int, int]]):
        """
        Create a Drawing with all UserDrawings atomically.

        Args:
            year: The year for this drawing
            assignments: List of (giver_id, receiver_id) tuples

        Returns:
            The created Drawing instance

        Raises:
            ValueError: If assignments don't cover all active users exactly once
        """
        from django.contrib.auth import get_user_model

        User = get_user_model()

        eligible = set(User.objects.filter(is_active=True).values_list("id", flat=True))
        givers = set(a[0] for a in assignments)
        receivers = set(a[1] for a in assignments)

        if givers != eligible:
            missing = eligible - givers
            extra = givers - eligible
            raise ValueError(f"Giver mismatch. Missing: {missing}, Extra: {extra}")
        if receivers != eligible:
            missing = eligible - receivers
            extra = receivers - eligible
            raise ValueError(f"Receiver mismatch. Missing: {missing}, Extra: {extra}")

        with transaction.atomic():
            drawing = cls.objects.create(year=year)
            UserDrawing.objects.bulk_create(
                [UserDrawing(drawing=drawing, giver_id=g, receiver_id=r) for g, r in assignments]
            )

        return drawing

    @classmethod
    def create_for_year(cls, year: int):
        """Create a drawing for the given year with all active users."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        # TODO: add sanity checks:
        # - every user has an address
        # - every user has a none-empty wishlist
        # - every user has a secret_name
        user_ids = list(User.objects.filter(is_active=True).values_list("id", flat=True))
        assignments = generate_assignments(user_ids)
        return cls.create_with_assignments(year, assignments)


class UserDrawing(models.Model):
    drawing = models.ForeignKey(
        Drawing,
        on_delete=models.CASCADE,
        related_name="user_drawings",
    )
    giver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="as_giver",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="as_receiver",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["drawing", "giver"], name="unique_giver_per_drawing"),
            UniqueConstraint(fields=["drawing", "receiver"], name="unique_receiver_per_drawing"),
            CheckConstraint(check=~Q(giver=F("receiver")), name="no_self_gifting"),
        ]

    def __str__(self):
        return f"{self.giver} → {self.receiver.profile.code_name} ({self.drawing.year})"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    code_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user}"


class Wishlist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist for {self.user}"


class Event(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user} at {self.created_at}"
