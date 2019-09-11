# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.urls import resolve
from .models import *
from django.db.models import Q
from datetime import date
from django.contrib import messages
from django.forms.models import BaseInlineFormSet

admin.site.site_header = "Winner Academy Administration"



class AttendanceRecordAdminInline(admin.TabularInline):
    extra = 0
    model = AttendanceRecord
    max_num = 6

    def get_formset(self, request, obj=None, **kwargs):
        
        self.parent_obj = None
        self.registered = None
        if obj is None:
            return super(AttendanceRecordAdminInline, self).get_formset(request, obj, **kwargs)
        else:
            self.parent_obj = obj
            self.registered = AttendanceRecord.objects.filter(Q(registered_at=date.today()) & Q(group=self.parent_obj))
        extra = obj.trainees.all().count() - self.registered.count()
        # registered = obj.trainees.get()
        kwargs['extra'] = extra
        kwargs['max_num'] = obj.capacity
        return super(AttendanceRecordAdminInline, self).get_formset(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(AttendanceRecordAdminInline, self).get_queryset(request).filter(registered_at=date.today())
        return qs


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "trainee":
            group = self.parent_obj
            if group:
                kwargs["queryset"] = Trainee.objects.filter(group=group)
                # .difference(self.parent_obj.trainees.all())

        return super(AttendanceRecordAdminInline, self).formfield_for_foreignkey(db_field, request, **kwargs)



class TraineeAdmin(admin.ModelAdmin):
    model = Trainee
    exclude = ('reference', )
    list_display = ('name', 'phone_number', 'group', 'level', 'reference')
    search_fields = ('reference','group__trainer__reference')
    # inlines = (AttendanceRecordAdminInline,)
    
    # def get_object(self, request, object_id):
    #     self.object = super(TraineeAdmin, self).get_object(request, object_id)
    #     return self.object

    # def get_parent_object_from_request(self, request):
    #         resolved = resolve(request.path_info)
    #         if resolved.args:
    #             return self.parent_model.objects.get(pk=resolved.args[0])
    #         return None
    



class TrainerAdmin(admin.ModelAdmin):
    model = Trainer
    exclude = ('reference', )
    readonly_fields = ('reference',)
    list_display = ('name', 'phone_number', 'reference', 'groups', )
    search_fields = ('reference','name', 'phone_number', )

class ClassAdmin(admin.ModelAdmin):
    model = Class
    inlines = (AttendanceRecordAdminInline,)
    readonly_fields = ('price',)
    list_display = ('name', 'trainer', 'days', 'until', 'level', 'capacity', 'season',)

    def message_user(self, *args):
        pass

    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)
    #     for instance in instances:
    #         similar_instance = AttendanceRecord.objects.get(trainee=instance.trainee,registered_at=date.today())
    #         # import pdb;pdb.set_trace()
    #         if similar_instance:
    #             if similar_instance.registered_at == instance.registered_at:
    #                 return messages.error(request, "A trainee attendance is duplicated")
    #             else:
    #                 instance.save()
    #     formset.save_m2m()
    #     return messages.success(request, "Attendance is saved correctly!")
        

class AttendanceRecordAdmin(admin.ModelAdmin):
    model = AttendanceRecord
    list_display = ('trainee','group','registered_at',)

admin.site.register(Trainee, TraineeAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)

