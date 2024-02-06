from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['category'].widget = forms.Select(choices=self.category_choices())

    def category_choices(self):
        #select function expecting a list of tuple with 1st value will be submitted
        #second values is human readable
        choices = [
            ('OBC', 'OBC'),
            ('SC', 'SC'),
            ('ST', 'ST'),
            ('OEC', 'OEC'),
            ('GENERAL','GEN')
        ]
        return choices
    
class AllotementForm(forms.ModelForm):
    class Meta:
        model = Allotment
        fields = '__all__'