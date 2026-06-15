import random
import uuid
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models

from team_finder.constants import (AVATAR_COLORS, MAX_LENGTH_ABOUT,
                                   MAX_LENGTH_NAME, MAX_LENGTH_PHONE,
                                   MAX_LENGTH_SURNAME)
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    surname = models.CharField(max_length=MAX_LENGTH_SURNAME)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=MAX_LENGTH_PHONE, unique=True)
    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=MAX_LENGTH_ABOUT, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        color = random.choice(AVATAR_COLORS)
        first_letter = self.name[0].upper() if self.name else '?'

        img = Image.new('RGB', (200, 200), color=color)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 100)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), first_letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (200 - text_width) / 2
        y = (200 - text_height) / 2
        draw.text((x, y), first_letter, fill='white', font=font)

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'avatar_{uuid.uuid4()}.png'
        return ContentFile(buffer.getvalue(), filename)