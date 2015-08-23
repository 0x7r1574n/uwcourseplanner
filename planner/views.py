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
from rest_framework import generics


def get_courses(courses, year, quarter):
    return courses.filter(year=year).filter(quarter=quarter)


@login_required(login_url='/accounts/login/')
def course_list(request):
    curr_user = request.user.id
    courses = Course.objects.filter(user=curr_user)
    remaining = []
    cores = Core.objects.get_queryset()
    for core in cores:
        try:
            courses.get(fullname=core.fullname)
        except Course.DoesNotExist:
            remaining.append(core)
    context = {
        'years_quarters': sorted({('y%iq%i' % (y, q)): get_courses(courses, y, q) for y in range(1, 5) for q in range(1, 5)}.iteritems()),
        'courses': courses,
        'cores': remaining
    }
    return render(request, 'planner/course_list.html', context)


@login_required(login_url='/accounts/login/')
def course_new(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.fullname = course.fullname.lower().replace(' ', '')  # reformat user input
            courses = Course.objects.filter(user=request.user.id)
            cores = Core.objects.get_queryset()
            master = Master.objects.filter(fullname=course.fullname)
            if len(master) != 0:
                for core in cores:
                    # check if is adding a core and has a prereq
                    if core.fullname == course.fullname and core.prereq != '':
                        fulfilled = False
                        for course in courses:
                            # check if user has prereq
                            if course.fullname == core.prereq:
                                fulfilled = True
                                course.dept = master[0].dept
                                course.number = master[0].number
                                course.title = master[0].title
                                course.description = master[0].description
                                course.save()
                        if not fulfilled:
                            form = CourseForm()
                    # if not core or is core but no prereqs (add the class)
                    else:
                        course.dept = master[0].dept
                        course.number = master[0].number
                        course.title = master[0].title
                        course.description = master[0].description
                        course.save()
            else:
                form = CourseForm()
                return render(request, 'planner/course_edit.html', {'form': form})
            return redirect('planner.views.course_detail', pk=course.pk)
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
        courses = Course.objects.filter(user=request.user.id)
        serializer = CourseSerializer(courses, many=True)
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
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)


class RestCoreList(generics.ListCreateAPIView):
    queryset = Core.objects.all()
    serializer_class = CoreSerializer


class RestCoreDetail(generics.RetrieveDestroyAPIView):
    queryset = Core.objects.all()
    serializer_class = CoreSerializer
