# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import *

admin.site.site_header = "Matter Administration"

class TraineeAdmin(admin.ModelAdmin):
    model = Trainee

class TrainerAdmin(admin.ModelAdmin):
    model = Trainer

class ClassAdmin(admin.ModelAdmin):
    model = Class

class AttendanceRecordAdmin(admin.ModelAdmin):
    model = AttendanceRecord


admin.site.register(Trainee, TraineeAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)

