from sys import exception
from django.db import models
from uuid import uuid4
from django.core.exceptions import ObjectDoesNotExist

from django.db.models.fields import uuid

import referal

# Prefer use uuid4
INVITE_CODE_LENGHT = 8


def validate_this(code):
    """
    Validate lenght of invite code in view
    """
    return len(code) == INVITE_CODE_LENGHT


# Create your models here.
class Referal(models.Model):
    """
    Referal boilerplate
    Inherrit it in another model
    """

    def generate_code():
        """
        I prefere user uuid
        """
        code = str(uuid4())[:INVITE_CODE_LENGHT]
        return code

    invite_code = models.CharField(
        max_length=INVITE_CODE_LENGHT,
        default=generate_code,
        editable=False,
        null=True,
    )
    invite_from = models.ForeignKey(
        to="Referal",
        on_delete=models.SET_NULL,
        null=True,
    )

    @property
    def referals(self):
        return self.__class__.objects.filter(invite_from=self)

    def invite(self, invite_code: str):
        if self.invite_from is None:
            try:
                parent = self.__class__.objects.get(invite_code=invite_code)
                if parent.id != self.id:
                    self.invite_from = parent
                    self.save()
                    return self
            except ObjectDoesNotExist:
                return None
