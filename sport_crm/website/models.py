# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
from datetime import date, datetime

from django.core.exceptions import ValidationError
import string, random
from recurrence.fields import RecurrenceField
# from django.conf import settings

LEVEL_CHOICES = (
                ("A", "A"),
                ("B", "B"),
                ("C", "C"),
                    )


def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
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
    trainer = models.ForeignKey(Trainer, related_name="trainers", on_delete=models.CASCADE)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, blank=True, null=True)
    recurrences = RecurrenceField(null=True)
    price = models.IntegerField(null=True, blank=True)
    CAPACITY_CHOICES = (
                (6, 6),
                (12, 12),
                (1 , 1),
                    )
    capacity = models.IntegerField(choices=CAPACITY_CHOICES, null = True, blank= True)
    season = models.CharField(max_length=1, choices=LEVEL_CHOICES, blank=True)

    def __str__(self):
        return self.name

    def save(self):
        if not self.price:
            # Generate ID once, then check the db. If exists, keep trying.
            switcher = { 
                1: 450,
                6: 350, 
                12: 250,
                        } 
 
            self.price =  switcher.get(self.capacity)
        super(Class, self).save()

    @property
    def days(self):
        if self.recurrences.rrules[0].byday:
            return self.recurrences.rrules[0].byday

    @property
    def until(self):
        if self.recurrences.rrules[0].until:
            datetimeobj = self.recurrences.rrules[0].until.strftime('%Y-%m-%d')
            return datetimeobj

class Trainee(models.Model):

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    registered_at = models.DateField(auto_now_add=True, null=True, blank=True)
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
        
        if self.group.capacity <= self.group.trainees.all().count():
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
    def save(self):
        if not self.registered_at:
            self.registered_at = date.today()
        super(AttendanceRecord, self).save()


    def clean(self):
        if not self.pk:
            if AttendanceRecord.objects.filter(group=self.group, trainee=self.trainee, registered_at=date.today()).exists():
                raise ValidationError('Duplicate Attendance Record!')
