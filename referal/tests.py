from django.db.models.expressions import Ref
from django.test import TestCase

from .models import Referal, INVITE_CODE_LENGHT


# Create your tests here.
class ReferalTest(TestCase):
    def test_create_referal(self) -> None:
        Referal.objects.create()
        self.assertTrue(Referal.objects.first(), msg="Referal wasnt created")

    def test_referal_code_created_and_valid(self) -> None:
        Referal.objects.create()
        referal: Referal = Referal.objects.first()
        self.assertTrue(referal.invite_code, msg="Code wasnt created")
        self.assertEqual(
            len(referal.invite_code),
            INVITE_CODE_LENGHT,
            msg="Wrong lenght of created code",
        )

    def test_base_invitation_system(self) -> None:
        Referal.objects.create()
        referal: Referal = Referal.objects.first()
        for _ in range(5):
            Referal.objects.create()
            new_one: Referal = Referal.objects.last()
            new_one.invite(referal.invite_code)
        referal = Referal.objects.get(id=referal.id)
        self.assertTrue(referal.referals, msg="Empty referal list")
        self.assertEqual(len(referal.referals), 5, msg="Wrong referals count")

    def test_delete_parent_referal(self) -> None:
        Referal.objects.create()
        referal: Referal = Referal.objects.first()
        Referal.objects.create()
        new_one: Referal = Referal.objects.last()
        new_one.invite(referal.invite_code)
        referal.delete()
        new_one = Referal.objects.get(id=new_one.id)
        self.assertIsNone(new_one.invite_from, msg="Parent referal wasnt delete")

    def test_wrong_code_invite(self) -> None:
        Referal.objects.create()
        referal = Referal.objects.first()
        referal.invite("badcode")
        after = Referal.objects.first()
        self.assertIsNone(after.invite_from, msg="Wrong invite code work!?")
        self.assertEqual(referal, after, msg="Referal unmatched after bad invite")

    def test_loop_invite(self) -> None:
        Referal.objects.create()
        referal = Referal.objects.first()
        referal.invite(referal.invite_code)
        referal = Referal.objects.first()
        self.assertIsNone(referal.invite_from, msg="Referal itself is error")
