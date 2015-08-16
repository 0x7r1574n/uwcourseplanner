from django.shortcuts import render
from django.utils import timezone
from .models import Course
from django.shortcuts import render, get_object_or_404
from .forms import CourseForm

from django.shortcuts import redirect
# Create your views here.


def course_list(request):
    courses = Course.objects.filter(author=user).order_by('year')
    year1 = courses.filter(year=1)
    y1q1 = year1.filter(quarter=1)
    y1q2 = year1.filter(quarter=2)
    y1q3 = year1.filter(quarter=3)
    y1q4 = year1.filter(quarter=4)
    return render(request, 'planner/course_list.html', {'courses' : courses}, {'y1' : year1}, {'y1q1' : y1q1}, {'y1q2' : y1q2}, {'y1q3' : y1q3}, {'y1q4' : y1q4})

def course_new(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('planner.views.course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'planner/course_edit.html', {'form': form})

def course_edit(request, pk):
    course = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('planner.views.course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'planner/course_edit.html', {'form': form})

def course_remove(request, pk):
	course = get_object_or_404(Course, pk=pk)
	course.delete()
	return redirect('planner.views.course_list')

def course_detail(request, pk):
	course = get_object_or_404(Course, pk=pk)
	return render(request, 'planner/course_detail.html', {'course': course})
