from django.db import models
from account.models import Account
from django.utils.translation import ugettext_lazy as _


class MessageImage(models.Model):
    img = models.ImageField(upload_to="chat/")


class Message(models.Model):
    sender = models.ForeignKey(
        Account, verbose_name=_("sender"), on_delete=models.CASCADE,
        related_name='sender'
    )
    recipient = models.ForeignKey(
        Account, verbose_name=_("recipient"), on_delete=models.CASCADE,
        related_name='recipient'
    )
    message = models.TextField(_("message"))
    img = models.ForeignKey(MessageImage, null=True, on_delete=models.SET_NULL)
    published = models.DateTimeField(_("published"), auto_now_add=True)

    class Meta:
        verbose_name = _("chat")
        verbose_name_plural = _("chats")

    def __str__(self):
        return str(self.sender) + str(self.recipient) + str(self.message) + str(self.published)
