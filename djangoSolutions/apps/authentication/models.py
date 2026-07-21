# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class CustomUser(AbstractUser):

#     username = None

#     LEARNING_TYPES = (
#         ('normal', 'Normal Learning'),
#         ('examples', 'Learning with Examples'),
#         ('concept', 'Concept-Based Learning'),
#         ('visual', 'Visual Learning'),
#         ('simplified', 'Simplified Learning'),
#     )

#     name = models.CharField(max_length=255)

#     email = models.EmailField(unique=True)

#     dob = models.DateField()

#     phone_number = models.CharField(max_length=20)

#     school_name = models.CharField(max_length=255)

#     standard = models.CharField(max_length=50)

#     preferred_learning_type = models.CharField(
#         max_length=50,
#         choices=LEARNING_TYPES,
#         default='normal'
#     )

#     address = models.TextField()

#     USERNAME_FIELD = 'email'

#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email
