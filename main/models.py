from django.db import models
from django.contrib.auth.models import User
import random

from django.db.models.fields import DateTimeField
# Create your models here.

class Subjects(models.Model):
    name = models.CharField("Fan nomi", max_length=150)
    
    def __str__(self):
        return self.name


class CameWith(models.Model):
    name = models.CharField("Sabab nomi", max_length=250)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.ForeignKey(User, related_name="teacher", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField("Ismi", max_length=150)
    surname = models.CharField("Familiyasi", max_length=150)
    image = models.ImageField("O'qituvchi rasmi", upload_to='teacher_img/',null=True, blank=True)
    tel_num = models.CharField("Telefon raqami", max_length=50, blank=True)
    subject = models.ForeignKey(Subjects, related_name="teachers", on_delete=models.PROTECT)
    price = models.PositiveIntegerField("Bitta dars uchun narx", default=0)
    # harajatlar hisobi
    countsub = models.PositiveIntegerField("Bir oydagi darslar soni", default=0)
    allprice = models.PositiveIntegerField("Jami maosh", default=0)




    def __str__(self):
        return f"{self.name} {self.surname}"

class Name(models.Model):
    name = models.CharField(name='ismingizni kiriting',max_length=250)
class Group(models.Model):
    own = models.ForeignKey(User, related_name="own_group", on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, related_name="group", on_delete=models.CASCADE, blank=True)
    name = models.CharField("Guruh nomi", max_length=350)
    subject = models.ForeignKey(Subjects, related_name="teachers_group", on_delete=models.CASCADE, blank=True)
    time = models.CharField("Vaqti", max_length=50)
    kunlari = models.CharField("Hafta kunlari", max_length=350)
    payment = models.PositiveIntegerField("To'lov", default=0)
    days_in_month = models.PositiveIntegerField("Kun soni", default=0)

    active = models.BooleanField("aktiv/aktiv emas", default=False)
    
    def __str__(self):
        if self.active == True:
            return self.name
        else:
            return f"{self.name} (Qabuldagi guruh)"


class Student(models.Model):
    own = models.ForeignKey(User, related_name="students", on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(Group, related_name="student", on_delete=models.CASCADE, blank=True, null=True)
    # shaxsiy ma'lumotlari
    name = models.CharField("Ismi", max_length=150)
    surname = models.CharField("Familiyasi", max_length=150)
    brith = models.CharField("Tug'ulgan sanasi", max_length=50)
    image = models.ImageField("O'quvchi rasmi", upload_to='student_img/', blank=True, null=True)
    password_img = models.ImageField("Pasort rasmi", upload_to='students_passport', blank=True)
    tel_num = models.CharField("Telefon raqami", max_length=50, blank=True)
    place = models.CharField("Yashash manzili", max_length=50)
    # harajatlar hisobi
    price = models.PositiveIntegerField("Chegirma",default=0)
    countsub = models.PositiveIntegerField("Bir oydagi darslar soni",default=0)
    allprice = models.PositiveIntegerField("Jami to'lov",default=0)

    called = models.BooleanField("called/not called",default=False)
    camewith = models.ForeignKey(CameWith, related_name="students", blank=True, on_delete=models.PROTECT)
        
    def __str__(self):
        return self.name


class CameHistory(models.Model):
    student = models.ForeignKey(Student, related_name="history", on_delete=models.CASCADE)
    time = models.CharField("Kelgan sanasi", blank=True, max_length=100)
    came = models.BooleanField("keldi/kelmadi", default=False)
    apset = models.BooleanField("sababli/sababsiz", default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.student.name


class PayedHistory(models.Model):
    student = models.ForeignKey(Student, related_name="payment", on_delete=models.CASCADE)
    time = models.CharField("To'lagan sanasi", blank=True, max_length=100)
    payed = models.PositiveIntegerField("summasi", default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.student.name
    

class TeacherHistory(models.Model):
    teacher = models.ForeignKey(Teacher, related_name="history", on_delete=models.CASCADE)
    time = models.CharField("to'langan vaqt", blank=True, max_length=150)
    price = models.PositiveIntegerField("to'langan summa", default=0)

    def __str__(self):
        return self.teacher.name

    