from planner.models import Course, Core
from scheduleapi.models import Course as Master
from django.shortcuts import render, get_object_or_404
from .forms import CourseForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from serializers import CourseSerializer, CoreSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def get_courses(courses, year, quarter):
    return courses.filter(year=year).filter(quarter=quarter)


@login_required(login_url='/accounts/login/')
def course_list(request):
    curr_user = request.user.id
    courses = Course.objects.filter(user=curr_user)
    context = {
        'years_quarters': sorted({('y%iq%i' % (y, q)): get_courses(courses, y, q) for y in range(1, 5) for q in range(1, 5)}.iteritems()),
        'courses': courses}
    return render(request, 'planner/course_list.html', context)


@login_required(login_url='/accounts/login/')
def course_new(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            try:
                # if it is core
                core = Core.objects.get(fullname=course.fullname)
                # if prereq is fulfilled
                if core.prereq:
                    Course.objects.get(fullname=core.prereq)
                    master = Master.objects.get(fullname=course.fullname)
                    course.dept = master.dept
                    course.number = master.number
                    course.title = master.title
                    course.description = master.description
                    course.save()
                else:
                    master = Master.objects.get(fullname=course.fullname)
                    course.dept = master.dept
                    course.number = master.number
                    course.title = master.title
                    course.description = master.description
                    course.save()
                return redirect('planner.views.course_detail', pk=course.pk)
            except Core.DoesNotExist:  # if not core
                master = Master.objects.get(fullname=course.fullname)
                course.dept = master.dept
                course.number = master.number
                course.title = master.title
                course.description = master.description
                course.save()
                return redirect('planner.views.course_detail', pk=course.pk)
            except Course.DoesNotExist, Master.DoesNotExist:  # not in master or prereq not fulfilled
                form = CourseForm()
    else:
        form = CourseForm()
    return render(request, 'planner/course_edit.html', {'form': form})


@login_required(login_url='/accounts/login/')
def course_remove(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('planner.views.course_list')


@login_required(login_url='/accounts/login/')
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'planner/course_detail.html', {'course': course})


@login_required(login_url='/accounts/login/')
@api_view(['GET', 'POST'])
def rest_course_list(request):
    if request.method == 'GET':
        snippets = Course.objects.all()
        serializer = CourseSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/accounts/login/')
@api_view(['GET', 'DELETE'])
def rest_course_detail(request, pk):
    course = get_object_or_404(Course, pk)
    if request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)


@login_required(login_url='/accounts/login/')
@api_view(['GET', 'POST'])
def rest_core_list(request):
    if request.method == 'GET':
        cores = Core.objects.all()
        serializer = CoreSerializer(cores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
