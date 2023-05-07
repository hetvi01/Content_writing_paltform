from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from common.models import UUID
from writers.constants import UNIQUE_USERNAME, UNIQUE_EMAIL, FIRSTNAME_ERROR, LASTNAME_ERROR


# Create your models here.


class Writer(AbstractUser, UUID):
    """
    Stores employee's personal and authentication details.
    """

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=50, unique=True, validators=[username_validator, MinLengthValidator(2)],
                                error_messages={"unique": UNIQUE_USERNAME, })
    email = models.EmailField(unique=True, error_messages={"unique": UNIQUE_EMAIL, })
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(2),
                                                             RegexValidator(regex='^[a-zA-Z]+$',
                                                                            message=FIRSTNAME_ERROR,
                                                                            code='first_name')])
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(2),
                                                            RegexValidator(regex='^[a-zA-Z]+$',
                                                                           message=LASTNAME_ERROR,
                                                                           code='last_name')])

    about_me = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username}-{self.id}"
