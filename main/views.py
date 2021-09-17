from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from .forms import *
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
import datetime

# Create your views here.

class HomeView(LoginRequiredMixin,View):

    def get(self, request):
        camewith = CameWith.objects.all()
        groups = Group.objects.filter(active=True)
        students = 0
        for group in groups:
            students += int(group.student.all().count())
        context = {
            'groups':groups,
            'students':students,
            'camewith':camewith,
        }
        return render(request, 'index.html',context)


class TeachersView(LoginRequiredMixin,View):

    def get(self, request):
        return render(request, 'teachers.html')


class StudentsView(LoginRequiredMixin,View):

    def get(self, request):
        return render(request, 'students.html')


class GroupsView(LoginRequiredMixin,View):

    def get(self, request):
        groups = Group.objects.filter(active=True)
        context = {'groups':groups}
        return render(request, 'groups.html', context)


class NewGroupsView(LoginRequiredMixin,View):

    def get(self, request):
        groups = Group.objects.filter(active=False)
        context = {'groups':groups}
        return render(request, 'new_groups.html', context)

# ------Update views -------------------------------------------------------------------------------------------------

class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = CreateTeacherForm
    success_url = '/teachers/'
    template_name = "update_teacher.html"

class GroupUpdateView(UpdateView):
    model = Group
    form_class = CreateGroupForm
    success_url = '/groups/'
    template_name = "update_group.html"

class StudentUpdateView(UpdateView):
    model = Student
    form_class = CreateStudentForm
    success_url = '/students/'
    template_name = "update_student.html"

# ------Delete views------------------------------------------------------------------------------------------------

class TeacherDeleteView(DeleteView):
    model = Teacher
    success_url = '/teachers/'
    template_name = 'teacher_confirm_delete.html'

class GroupDeleteView(DeleteView):
    model = Group
    success_url = '/groups/'
    template_name = 'group_confirm_delete.html'

class StudentDeleteView(DeleteView):
    model = Student
    success_url = '/students/'
    template_name = 'student_confirm_delete.html'


# --------Create views--------------------------------------------------------------------------------------------------

def add_subject(request):
    new_sub = request.GET.get('name')
    s = Subjects.objects.create(name=new_sub)
    s.save()
    return redirect('/')

def add_camewith(request):
    camewith = request.GET.get('name')
    s = CameWith.objects.create(name=camewith)
    s.save()
    return redirect('/')

class TeacherCreateView(LoginRequiredMixin,View):
    
    def get(self, request):
        form = CreateTeacherForm(request.GET)
        context = {
            'form':form
        }
        return render(request, 'add_teacher.html', context)




    def post(self, request):
        form = CreateTeacherForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            teacher = Teacher.objects.create(
                user=request.user,
                name=new.name,
                surname=new.surname,
                image=new.image,
                tel_num=new.tel_num,
                subject=new.subject,
                price=new.price, 
            )
            teacher.save()
            return redirect('/')
        context = {
            'form':form
        }
        return render(request, 'add_teacher.html', context)

def create_group(request):
    form = CreateGroupForm(request.GET)
    if request.method == 'POST':
        form = CreateGroupForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            new = Group.objects.create(
                own=request.user,
                teacher=f.teacher,
                name=f.name,
                subject=f.subject,
                kunlari=f.kunlari,
                time=f.time,
                payment=f.payment,
                days_in_month=f.days_in_month,
            )
            new.save()
            return redirect('/')
        else:
            form = CreateGroupForm()
    return render(request, 'add_group.html',{'form':form})

def create_student(request):
    form = CreateStudentForm(request.GET)
    if request.method == 'POST':
        form = CreateStudentForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            new = Student.objects.create(
                own=request.user,
                group=f.group,
                name=f.name,
                surname=f.surname,
                brith=f.brith,
                image=f.image,
                tel_num=f.tel_num,
                place=f.place,
                price=f.price,
                camewith=f.camewith,
                password_img=f.password_img,
            )
            new.save()
            return redirect('/')
        else:
            form = CreateStudentForm()
    return render(request, 'add_student.html', {'form':form})


# --------Detail views--------------------------------------------------------------------------------------------------

def group_detail(request, pk):
    group = Group.objects.get(pk=pk)
    context = {
        'group':group,
    }
    return render(request, 'group_detail.html', context)

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    context = {'stu':student}
    return render(request, "student_detail.html", context)

def get_plus(request):
    pk = request.GET.get('data')
    action = request.GET.get('action')
    student = Student.objects.get(pk=pk)
    if action == "came":
        history = CameHistory.objects.create(
            student=student,
            time=datetime.datetime.now().strftime('%d/%m/%y'),
            came=True,
        )
        history.save()
        try:
            student.allprice+=(student.group.payment/student.group.days_in_month)
        except:
            None
        student.countsub+=1
        student.save()
    elif action == "apset":
        history = CameHistory.objects.create(
            student=student,
            time=datetime.datetime.now().strftime('%d/%m/%y'),
            came=False,
            apset=True,
        )
        history.save()
    else:
        history = CameHistory.objects.create(
            student=student,
            time=datetime.datetime.now().strftime('%d/%m/%y'),
            came=False,
        )
        history.save()
        try:
            student.allprice+=(student.group.payment/student.group.days_in_month)
        except:
            None
        student.save()
    return JsonResponse({'status':200})


# --------Other functions--------------------------------------------------------------------------------------------------

def call(request):
    pk = request.GET.get('pk')
    stu = Student.objects.get(pk=pk)

    stu.called = True
    stu.save()

    return JsonResponse({'status':'ok'})

def active_group(request, pk):
    group = Group.objects.get(pk=pk)
    group.active = True
    group.save()

    return redirect('/groups/')

def pay(request):
    pk = request.GET.get('pk')
    action = request.GET.get('action')
    student = Student.objects.get(pk=pk)
    if action == 'skit':
        v = request.GET.get('price')
        value = int(v) - int(student.price)
    else:
        value = request.GET.get('price')
    teacher = student.group.teacher
    price = (int(value) / 100) * int(teacher.price)
    teacher.allprice += price
    teacher.save()
    history = PayedHistory.objects.create(
        student=student,
        time=datetime.datetime.now().strftime('%d-%m-%Y'),
        payed=value,
    )
    history.save()
    student.allprice = 0
    student.countsub = 0
    student.save()
    return JsonResponse({'status':200})

def pay_for_teacher(request):
    pk = request.GET.get('pk')
    value = request.GET.get('price')
    teacher = Teacher.objects.get(pk=pk)
    history = TeacherHistory.objects.create(
        teacher=teacher,
        time=datetime.datetime.now().strftime('%d-%m-%Y'),
        price=value,
    )
    history.save()
    teacher.countsub = 0
    teacher.allprice = 0
    teacher.save()
    return JsonResponse({'status':200})

def group_history(request, pk):
    group = get_object_or_404(Group, pk=pk)
    students = Student.objects.filter(group=group)
    context = {
        'group':group,
        'students':students,
    }
    return render(request, 'group_history.html', context)

def brithdays(request):
    today = datetime.datetime.now().strftime('%m-%d')
    student = Student.objects.filter(brith__icontains=today)

    context = {
        'today':today,
        'stu':student
    }
    return render(request, "brithday.html", context)


class FaqView(TemplateView):
    template_name = "faq.html"
