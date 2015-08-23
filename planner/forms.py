from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    fullname = forms.CharField(max_length=50)
    year = forms.IntegerField(max_value=4)
    quarter = forms.IntegerField(max_value=4)
    credit = forms.IntegerField(max_value=20)

    class Meta:
        model = Course
        fields = ('fullname', 'year', 'quarter', 'credit')
