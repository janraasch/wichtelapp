from django.test import SimpleTestCase

from wichtel.models import generate_assignments


class GenerateAssignmentsTests(SimpleTestCase):
    def test_fewer_than_2_users_raises_empty(self):
        """ValueError for empty list."""
        with self.assertRaisesMessage(ValueError, "Need at least 2 users"):
            generate_assignments([])

    def test_fewer_than_2_users_raises_single(self):
        """ValueError for single user."""
        with self.assertRaisesMessage(ValueError, "Need at least 2 users"):
            generate_assignments([1])

    def test_each_user_gives_exactly_once(self):
        """All givers are unique and match input."""
        user_ids = [1, 2, 3, 4, 5, 6, 7]
        assignments = generate_assignments(user_ids)

        givers = [a[0] for a in assignments]
        self.assertEqual(sorted(givers), sorted(user_ids))

    def test_each_user_receives_exactly_once(self):
        """All receivers are unique and match input."""
        user_ids = [1, 2, 3, 4, 5, 6, 7]
        assignments = generate_assignments(user_ids)

        receivers = [a[1] for a in assignments]
        self.assertEqual(sorted(receivers), sorted(user_ids))

    def test_no_self_assignments(self):
        """No (x, x) pairs exist."""
        user_ids = [1, 2, 3, 4, 5, 6, 7]
        # Run multiple times to increase confidence
        for _ in range(100):
            assignments = generate_assignments(user_ids)
            for giver, receiver in assignments:
                self.assertNotEqual(giver, receiver, f"Self-assignment found: {giver} -> {receiver}")

    def test_randomness(self):
        """Multiple runs can produce different orderings."""
        user_ids = [1, 2, 3, 4, 5, 6, 7]
        results = set()

        for _ in range(50):
            assignments = generate_assignments(user_ids)
            # Convert to tuple for hashability
            results.add(tuple(assignments))

        # With 50 runs and 1854 possible derangements, we should get multiple unique results
        self.assertGreater(len(results), 1, "All 50 runs produced identical results - randomness not working")

    def test_two_users(self):
        """Edge case: exactly 2 users must swap with each other."""
        user_ids = [10, 20]
        assignments = generate_assignments(user_ids)

        # Only one valid derangement: each gives to the other
        self.assertEqual(set(assignments), {(10, 20), (20, 10)})

    def test_preserves_input_order_for_givers(self):
        """Givers appear in the same order as input user_ids."""
        user_ids = [5, 3, 8, 1]
        assignments = generate_assignments(user_ids)

        givers = [a[0] for a in assignments]
        self.assertEqual(givers, user_ids)
