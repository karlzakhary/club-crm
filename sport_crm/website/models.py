# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
# from django.conf import settings

LEVEL_CHOICES = (
                ("A", "A"),
                ("B", "B"),
                ("C", "C"),
                    )

# Models


class Trainer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
    reference = models.CharField(max_length=100, null=True, blank=True, unique=True)
    group = models.ForeignKey(Class, related_name="trainees", on_delete=models.CASCADE)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, null=True, blank=True)
    #
    # def __init__(self, *args, **kwargs):
    #     self.reference = str(uuid.uuid4())
    #     super(Trainee, self).__init__(self, *args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = str(uuid.uuid4())[:5]
            super(Trainee, self).save(*args, **kwargs)
            return Trainee

    def __unicode__(self):
        return self.name

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
