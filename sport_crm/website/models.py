# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
from datetime import date, datetime
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
import string, random
from recurrence.fields import RecurrenceField
# from django.conf import settings

LEVEL_CHOICES = (
                ("A", "A"),
                ("B", "B"),
                ("C", "C"),
                    )


def id_generator(size=5, chars=string.digits):
    # chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
# Models


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    reference = models.CharField(max_length=5, null=True, blank=True, unique=True)
    
    def __str__(self):
        return "{}, id:{}".format(self.user.username,self.reference)

    def save(self,*args, **kwargs):
        if not self.reference:
            # Generate ID once, then check the db. If exists, keep trying.
            self.reference = id_generator()
            while Trainer.objects.filter(reference=self.reference).exists():
                self.reference = id_generator()
        super(Trainer, self).save(*args, **kwargs)

    @property
    def groups(self):
        groups = []
        if self.trainers.all():
            for group in self.trainers.all():
                groups.append(group)
        return groups

class Class(models.Model):

    class Meta:
        verbose_name_plural = "Groups"
        verbose_name = "Group"
    
    name = models.CharField(max_length=255)
    start_day = models.DateField(null=True, blank=True)
    trainer = models.ForeignKey(Trainer, related_name="trainers", on_delete=models.CASCADE)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, blank=True, null=True)
    recurrences = RecurrenceField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    CAPACITY_CHOICES = (
                (3, 3),
                (6, 6),
                (12, 12),
                    )
    capacity = models.IntegerField(choices=CAPACITY_CHOICES, null = True, blank= True)
    SESSION_NUMBER_CHOICES = (
        (8, 8),
        (12, 12),
    )
    sessions_number = models.IntegerField(choices=SESSION_NUMBER_CHOICES, null = True, blank= True)
    SEASON_CHOICES = (
        ('winter', 'Winter'),
        ('summer', 'Summer'),
    )
    
    season = models.CharField(max_length=200, choices=SEASON_CHOICES, blank=True)
    starts_at = models.TimeField(null=True, blank=True)
    ends_at = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        # if not self.price:
        #     # Generate ID once, then check the db. If exists, keep trying.
        #     switcher = {
        #         1: 450,
        #         6: 350,
        #         12: 250,
        #                 }
        #
        #     self.price =  switcher.get(self.capacity)
        super(Class, self).save(*args, **kwargs)

    @property
    def days(self):
        if self.recurrences:
            if self.recurrences.rrules:
                return self.recurrences.rrules[0].byday

    @property
    def ratio(self):
        return '{}/{}'.format(self.trainees.all().count(), self.capacity)

    @property
    def until(self):
        if self.recurrences:
            if self.recurrences.rrules[0].until:
                datetimeobj = self.recurrences.rrules[0].until.strftime('%Y-%m-%d')
                return datetimeobj

class Trainee(models.Model):

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    registered_at = models.DateField(auto_now_add=True, null=True, blank=True)
    reference = models.CharField(max_length=5, null=True, blank=True, unique=True)
    group = models.ForeignKey(Class, related_name="trainees", on_delete=models.CASCADE)
    level = models.CharField(max_length=1,  choices=LEVEL_CHOICES, null=True, blank=True)
    club_member = models.BooleanField(default=False)
    #
    # def __init__(self, *args, **kwargs):
    #     self.reference = str(uuid.uuid4())
    #     super(Trainee, self).__init__(self, *args, **kwargs)

    def save(self,*args, **kwargs):
        if not self.reference:
            # Generate ID once, then check the db. If exists, keep trying.
            self.reference = id_generator()
            self.level = self.group.level
            while Trainee.objects.filter(reference=self.reference).exists():
                self.reference = id_generator()
        if (not self.level) and self.group:
            self.level = self.group
        super(Trainee, self).save(*args, **kwargs)

    def clean(self):
        if self.level:
            if self.group:
                if self.level != self.group.level:
                    raise ValidationError('Chosen group\'s level doesn\'t match with trainee level')
        if self.group.capacity:
            if self.group.capacity < self.group.trainees.all().count():
                raise ValidationError('Chosen group\'s capacity is full')

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
    registered_at = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('registered_at', 'trainee',)
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['registered_at', 'trainee'], name='Single trainee per session')
    #     ]
    def save(self,*args, **kwargs ):
        if not self.registered_at:
            self.registered_at = date.today()
        super(AttendanceRecord, self).save(*args, **kwargs)


    def clean(self):
        if not self.pk:
            if AttendanceRecord.objects.filter(group=self.group, trainee=self.trainee, registered_at=date.today()).exists():
                raise ValidationError('Duplicate Attendance Record!')
