# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
#
#
# @receiver(post_save, sender=get_user_model())
# def create_aut_token(sender, instance=None, created=False, **kwargs):
#     print(sender, instance, created, kwargs, sep='\n')
#     print(23000000000000000000000010000000)
#     if created:
#         Token.objects.create(user=instance)
