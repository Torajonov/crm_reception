from .models import *

def students(request):
    context = {
        'teachers':Teacher.objects.all(),
        'student':Student.objects.all(),

    }
    return context
    
def historys(request,pk):
    h = History.objects.get(pk=pk)
    context = {
        'teachers':h,}
    return context