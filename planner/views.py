from django.shortcuts import render
from django.utils import timezone
from .models import Course
from django.shortcuts import render, get_object_or_404
from .forms import CourseForm

from django.shortcuts import redirect


# Create your views here.

def get_courses(courses, year, quarter):
    return courses.filter(year=year).filter(quarter=quarter)


def course_list(request):
    curUser = request.user.id
    courses = Course.objects.filter(user=curUser)
    params = {('y%iq%i' % (y, q)): get_courses(courses, y, q) for y in range(1, 5) for q in range(1, 5)}
    params['courses'] = courses
    return render(request, 'planner/course_list.html', params)


def course_new(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect('planner.views.course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'planner/course_edit.html', {'form': form})


def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
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
