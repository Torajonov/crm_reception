from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import escape
from .models import *


class CreateTeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ['name','surname','image','tel_num','subject','price']


class CreateGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name','subject','kunlari','teacher','payment','days_in_month','time']
        

class CreateStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['group','name','surname','brith','image','tel_num','place','price','camewith','password_img']


class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )


        