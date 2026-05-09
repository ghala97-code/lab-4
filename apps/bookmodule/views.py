from django.http import HttpResponse
from .models import Book, Publisher, Author
from django.db.models import Count, Sum, Avg, Max, Min, ExpressionWrapper, F, FloatField
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm

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