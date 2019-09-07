# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
from django.core.exceptions import ValidationError
import string, random
# from django.conf import settings

LEVEL_CHOICES = (
                ("A", "A"),
                ("B", "B"),
                ("C", "C"),
                    )


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
# Models


class Trainer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    reference = models.CharField(max_length=5, null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.name

    def save(self):
        if not self.reference:
            # Generate ID once, then check the db. If exists, keep trying.
            self.reference = id_generator()
            while Trainer.objects.filter(reference=self.reference).exists():
                self.reference = id_generator()
        super(Trainer, self).save()


class Class(models.Model):

    class Meta:
        verbose_name_plural = "Groups"
        verbose_name = "Group"

    name = models.CharField(max_length=255)
    trainer = models.ForeignKey(Trainer, related_name="trainers", on_delete=models.CASCADE)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name


class Trainee(models.Model):

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    reference = models.CharField(max_length=5, null=True, blank=True, unique=True)
    group = models.ForeignKey(Class, related_name="trainees", on_delete=models.CASCADE)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, null=True, blank=True)
    #
    # def __init__(self, *args, **kwargs):
    #     self.reference = str(uuid.uuid4())
    #     super(Trainee, self).__init__(self, *args, **kwargs)

    def save(self):
        if not self.reference:
            # Generate ID once, then check the db. If exists, keep trying.
            self.reference = id_generator()
            while Trainee.objects.filter(reference=self.reference).exists():
                self.reference = id_generator()
        super(Trainee, self).save()

    def clean(self):
        if self.level != self.group.level:
            raise ValidationError('Chosen group\'s level doesn\'t match with trainee level')

    # def __unicode__(self):
    #     return self.name

    def __str__(self):
        return "{}, id:{}".format(self.name,self.reference)


class AttendanceRecord(models.Model):
    group = models.ForeignKey(Class, related_name="records", on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, related_name="trainees", on_delete=models.CASCADE)
    ATTENDANCE_TYPES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('excuse', 'Excuse')
    )
    status = models.CharField(max_length=10, choices=ATTENDANCE_TYPES)
    registered_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
