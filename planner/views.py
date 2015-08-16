from django.shortcuts import render

# Create your views here.


def course_list(request):
    courses = Course.objects.filter(author=user).order_by('year')
    return render(request, 'planner/course_list.html', {'courses' : courses})

def course_new(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('planner.views.course_detail', pk=post.pk)
    else:
        form = CourseForm()
    return render(request, 'planner/course_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('planner.views.course_detail', pk=post.pk)
    else:
        form = CourseForm()
    return render(request, 'planner/course_edit.html', {'form': form})
