from django import forms
from .models import Book
from .models import Student, Address, Student2, Address2 ,Course


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price', 'quantity', 'pubdate', 'rating', 'publisher']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'



class Student2Form(forms.ModelForm):
    class Meta:
        model = Student2
        fields = '__all__'




class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'