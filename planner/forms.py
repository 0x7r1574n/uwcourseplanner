from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    fullname = forms.CharField(max_length=50)
    year = forms.IntegerField(max_value=4, min_value=1)
    quarter = forms.IntegerField(max_value=4, min_value=1)
    credit = forms.IntegerField(max_value=20, min_value=1)

    class Meta:
        model = Course
        fields = ('fullname', 'year', 'quarter', 'credit')
