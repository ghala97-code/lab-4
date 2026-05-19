from pyexpat.errors import messages

from django.http import HttpResponse
from .models import Book, Publisher, Author , Student, Address, Student2, Address2, Course
from django.db.models import Count, Sum, Avg, Max, Min, ExpressionWrapper, F, FloatField
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CourseForm, StudentForm, Student2Form, AddressForm, BookForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, 'bookmodule/list_books.html')

def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def links(request):
    return render(request, 'bookmodule/links.html')

def text_formatting(request):
    return render(request, 'bookmodule/text_formatting.html')

def listing(request):
    return render(request, 'bookmodule/listing.html')

def tables(request):
    return render(request, 'bookmodule/tables.html')

def getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]

def search_books(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = getBooksList()
        newBooks = []

        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower(): contained = True
            if contained: newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})
    
    return render(request, 'bookmodule/search.html')



def lab9_task1(request):
    total_q = Book.objects.aggregate(total=Sum('quantity'))['total'] or 1
    books = Book.objects.annotate(
        availability_pct=ExpressionWrapper((F('quantity') * 100.0) / total_q, output_field=FloatField())
    )
    print("\n--- Task 1: Percentage ---")
    for b in books: print(f"{b.title}: {b.availability_pct:.2f}%")
    return HttpResponse("Task 1 Done. Check Terminal!")

def lab9_task2(request):
    publishers = Publisher.objects.annotate(total_stock=Sum('book__quantity'))
    print("\n--- Task 2: Stock ---")
    for p in publishers: print(f"{p.name}: {p.total_stock}")
    return HttpResponse("Task 2 Done. Check Terminal!")

def lab9_task3(request):
    publishers = Publisher.objects.annotate(oldest=Min('book__pubdate'))
    print("\n--- Task 3: Oldest Book ---")
    for p in publishers: print(f"{p.name}: {p.oldest}")
    return HttpResponse("Task 3 Done. Check Terminal!")

def lab9_task4(request):
    publishers = Publisher.objects.annotate(avg_p=Avg('book__price'), min_p=Min('book__price'), max_p=Max('book__price'))
    print("\n--- Task 4: Price Stats ---")
    for p in publishers: print(f"{p.name} -> Avg: {p.avg_p}, Min: {p.min_p}, Max: {p.max_p}")
    return HttpResponse("Task 4 Done. Check Terminal!")

def lab9_task5(request):
    publishers = Publisher.objects.filter(book__rating__gt=3).annotate(high_rated_count=Count('book')).distinct()
    print("\n--- Task 5: High Rated ---")
    for p in publishers: print(f"{p.name}: {p.high_rated_count} books")
    return HttpResponse("Task 5 Done. Check Terminal!")

def lab9_task6(request):
    publishers = Publisher.objects.filter(book__price__gt=50, book__quantity__gte=1, book__quantity__lte=5).annotate(count_books=Count('book')).distinct()
    print("\n--- Task 6: Filtered ---")
    for p in publishers: print(f"{p.name}: {p.count_books} books")
    return HttpResponse("Task 6 Done. Check Terminal!")


# Task 1
def lab10_listbooks(request):
    books = Book.objects.all()
    print("\n--- Current Books in DB ---")
    for b in books: print(f"ID: {b.id} | Title: {b.title}")
    return render(request, 'bookmodule/lab10_list.html', {'books': books})

# Task 2
def lab10_addbook(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        new_book = Book.objects.create(title=title, price=price, pubdate='2024-05-09')
        print(f"--- Added: {new_book.title} ---")
        return redirect('/books/lab10/listbooks')
    return render(request, 'bookmodule/lab10_add.html')


# Task 3
def lab10_editbook(request, id):
   book = get_object_or_404(Book, id=id)
   if request.method == 'POST':
        book.title = request.POST.get('title')
        book.price = request.POST.get('price')
        book.save()
        
        print(f"--- Updated: {book.title} ---")
        return redirect('/books/lab10/listbooks')
   return render(request, 'bookmodule/lab10_edit.html', {'obj': book})

# Task 4
def lab10_deletebook(request, id):
    book = get_object_or_404(Book, id=id)
    print(f"--- Deleting: {book.title} ---")
    book.delete()
    return redirect('/books/lab10/listbooks')



def lab10_part2_listbooks(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/lab10_part2_list.html', {'books': books})

def lab10_part2_addbook(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/books/lab10_part2/listbooks')
    else:
        form = BookForm()
    return render(request, 'bookmodule/lab10_add_form.html', {'form': form})

def lab10_part2_editbook(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('/books/lab10_part2/listbooks')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookmodule/lab10_edit.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

# 1
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

# 2
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form, 'title': 'Add Student'})

# 3
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form, 'title': 'Update Student'})

# 4
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('student_list') 
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered!')
            return redirect('login')
        else:
            messages.error(request, 'Registration error. Please check the fields.')
    else:
        form = UserCreationForm()
    return render(request, 'bookmodule/register.html', {'form': form})

# Task 2 & Task 5
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successfully!') 
            return redirect('view_books')
        else:
            messages.error(request, 'Error logging in. Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'bookmodule/login.html', {'form': form})

# Task 4
def logout_view(request):
    logout(request)
    return redirect('login')
# Task 3
@login_required
def view_books(request):
    return render(request, 'bookmodule/view_books.html')