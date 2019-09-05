# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.urls.base import resolve
from .models import *

admin.site.site_header = "Matter Administration"


# class TraineeAdminForm(forms.ModelForm):
#     class Meta:
#         model = Trainee
#         fields = '__all__'
#     def __init__(self, *args, **kwargs):
#         super(TraineeAdminForm, self).__init__(*args, **kwargs)
#         # import pdb;pdb.set_trace()
#         trainee_instance = self.instance
#         # if trainee_instance.id:
#         self.fields['group'] = forms.ModelChoiceField(
#             queryset=Class.objects.filter(level=trainee_instance.level))


class TraineeAdmin(admin.ModelAdmin):
    model = Trainee
    exclude = ('reference', )
    # form = TraineeAdminForm
    list_display = ('name', 'phone_number', 'group', 'level', 'reference')
    search_fields = ('reference',)
    def __init__(self, *args, **kwargs):
        super(TraineeAdmin, self).__init__(*args, **kwargs)
        self.reference = str(uuid.uuid4())


    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.args:
            return self.parent_model.objects.get(pk=resolved.args[0])
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            trainee = self.get_parent_object_from_request(request)
            if trainee:
                kwargs["queryset"] = Class.objects.filter(level=trainee.level)
        return super(TraineeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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

