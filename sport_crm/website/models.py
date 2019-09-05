# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
# from django.conf import settings


# Models
class Trainer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)


class Class(models.Model):
    name = models.CharField(max_length=255)
    trainer = models.ForeignKey(Trainer, related_name="trainers", on_delete=models.CASCADE)
    LEVEL_CHOICES = (
                ("A", "A"),
                ("B", "B"),
                ("C", "C"),
                    )
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.name

class Trainee(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255)
    date_of = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True, unique=True)
    group = models.ForeignKey(Class, related_name="trainees", on_delete=models.CASCADE)

    def __init__(self):
        super(Trainee, self).__init__()
        self.ref = str(uuid.uuid4())

    def __unicode__(self):
        return self.name


class AttendanceRecord(models.Model):
    group = models.ForeignKey(Class, related_name="records", on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, related_name="trainees", on_delete=models.CASCADE)
    ATTENDANCE_TYPES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )
    status = models.CharField(max_length=10, choices=ATTENDANCE_TYPES)
