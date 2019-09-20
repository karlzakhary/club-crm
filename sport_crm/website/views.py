# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# importing required packages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import AttendanceForm
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.db import IntegrityError
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class AttendanceCreateView(FormView):

    def get(self, request, *args, **kwargs):
        context = {'form': AttendanceForm()}
        return render(request, 'attendance.html', context)

    # def clean(self):
    #     cleaned_data = super(AttendanceForm, self).clean()
    #     reference = cleaned_data.get('reference')
    #
    #     if not Trainee.objects.filter(reference=reference).exists():
    #         raise forms.ValidationError(_("This reference code doesn't exist. Please supply a different one."))
    #     return reference

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     trainee = Trainee.objects.get(reference=self.cleaned_data['reference'])
    #     self.object.trainee = trainee
    #     self.object.status = self.cleaned_data['status']
    #     self.object.group = trainee.group
    #     self.object.save()
    #     template = loader.get_template('showAttendance.html')
    #     return HttpResponse(template.render(object))


    def post(self, request, *args, **kwargs):
        form = AttendanceForm(request.POST)
        if form.is_valid():
            trainee = Trainee.objects.get(reference=form.cleaned_data['reference'])
            try:
                attendance = AttendanceRecord.objects.create(trainee=trainee, status=form.cleaned_data['status'], group=trainee.group)
                attendance.save()
                context = {
                    'name': attendance.trainee.name,
                    'group': attendance.trainee.group,
                    'status': attendance.status,
                    'reference': form.cleaned_data['reference']
                }
                template = loader.get_template('showAttendance.html')
                return HttpResponse(template.render(context, request))
            except IntegrityError as e:
                form.add_error('status','Trainee has been signed in')
        return render(request, 'attendance.html', {'form': form})




# disabling csrf (cross site request forgery)
@login_required(login_url='/admin/')
@csrf_exempt
def attendance(request):
    # if post request came
    args = {}
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            reference = form.cleaned_data['reference']
            trainee = Trainee.objects.find(reference=reference)
            status = form.cleaned_data['status']
            context = {
                'name': trainee.name,
                'reference': reference,
                'group': trainee.group,
                'status': status
            }
            template = loader.get_template('showAttendance.html')
            return HttpResponse(template.render(context, request))

        else:
            form = AttendanceForm()
        args['form'] = form

        # template = loader.get_template('attendance.html')
        return render (request, 'attendance.html', args)
        # returing the template
        # return HttpResponse(template.render())



class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
