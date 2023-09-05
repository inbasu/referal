from django.db import models


# Managers definition here
class ReferalManager(models.Managers):
    def creare_referal(self, **kwargs):
        invite_code: str = ""
        return Referal.objects.creare_referal(invite_code=invite_code, **kwargs)


# Create your models here.
class Referal(models.Model):
    """
    If reuse this class boilerplate
    Than delete models.Model inheritance
    And inherit itself
    """

    phone_number = models.CharField(max_lengh=10)
    invite_code = models.CharField(max_lengh=8)
    invite_from = models.ForeignKey(to="Referal", on_delete=models.SET_NULL)

    objects = ReferalManager()

    @property
    def referals(self):
        Referal.objects.filter(invite_from=self)

    def invite(self, invite_code: str) -> None | Referal:
        if self.invite_code is None:
            parent = Referal.objects.filter(invite_code=invite_code)
            if parent:
                self.invite_from = parent
                return parent
        return None
