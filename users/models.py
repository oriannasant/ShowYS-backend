from django.db import models
from django.contrib.auth.models import User


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

#aqui el desmadre

# Create your models here.


class Profile(models.Model):
    type_role = (
        ('A', 'Admin'),
        ('S', 'Standard'),
    )
    code = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_birth = models.DateField(auto_now=False, auto_now_add=False)
    phone = models.CharField(max_length=20)
    biography = models.CharField(blank=True, null=True, max_length=255)
    photo = models.ImageField(upload_to='profile_pictures',
                              default='profile_pictures/default.png', max_length=255)
    is_private = models.BooleanField(default=False)
    type = models.CharField(max_length=1, choices=type_role, default='S')

    def __str__(self):
        return '{} profile'.format(self.user.username)

    class Meta:
        db_table = 'Profile'


class Follow(models.Model):
    code = models.AutoField(primary_key=True)
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rel_from_set')
    user_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rel_to_set')

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

    class Meta:
        db_table = 'Follow'

#''''''''''''''''''''''''


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="SHOWYS"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
