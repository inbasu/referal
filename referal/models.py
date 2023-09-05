from django.db import models
from uuid import uuid4

# Prefer use uuid4
INVITE_CODE_LENGHT = 0


def validate_this(code):
    """
    Validate lenght of invite code in view
    """
    return len(code) == INVITE_CODE_LENGHT


# Create your models here.
class Referal(models.Model):
    """
    Referal boilerplate
    """

    def generate_code():
        """I prefere to use uuid4"""
        return str(uuid4())[:8]

    invite_code = models.CharField(
        max_length=INVITE_CODE_LENGHT,
        default=generate_code,
        editable=False,
    )
    invite_from = models.ForeignKey(
        to="Referal",
        on_delete=models.SET_NULL,
    )

    @property
    def referals(self):
        self.__class__.objects.filter(invite_from=self)

    def invite(self, invite_code: str):
        if self.invite_code is None:
            parent = self.__class__.objects.filter(invite_code=invite_code)
            if parent:
                self.invite_from = parent
                return parent
        return None
