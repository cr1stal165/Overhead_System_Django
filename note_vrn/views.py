import csv

from django.http import HttpResponse
from django.shortcuts import render

from note_vrn.models import Worker, Manufacturer, Product, Customer, Note, Purchased


def index(request):
    note = Note.objects.all()
    return render(request, "index.html", context={'all': note})


def show_stuff(request):
    stuff = Worker.objects.all()
    return render(request, "show_staff.html", context={'all':stuff})


def show_manufacturer(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, "show_manufacturer.html", context={'all': manufacturers})


def show_all_products(request):
    products = Product.objects.all()
    return render(request, "show_all_products.html", context={'all': products})


def show_purchased(request):
    purchased = Purchased.objects.all()
    return render(request, "show_purchased.html", context={'purch': purchased})


def add_note(request):
    products = Product.objects.all()
    worker = Worker.objects.all()
    return render(request, "add_note.html", context={'all': products, 'work': worker})


def confirm_add_note(request):

    if request.method == 'POST':
        #создание заказчика
        name = request.POST.get('fio')
        phone = request.POST.get('phone')
        mail = request.POST.get('mail')
        customer = Customer.objects.create(name=name, phone=phone, mail=mail)
        customer.save()

        # получаем список id товаров
        list_id = request.POST.getlist('product')
        curr = convert_id_to_integer_list(list_id)
        #получаем сотрудника
        worker = request.POST.get('work')

        # создание накладной
        data = request.POST.get('date')
        note = Note.objects.create(date=data, sum=0, customer_id=customer.id, worker_id=worker, product_id="")

        resp = request.POST.getlist('count')
        print(curr)
        print(convert_to_int(resp))
        curr_set = convert_to_int(resp)
        # создание купленных товаров
        products = Product.objects.filter(id__in=curr)
        sum_price = 0
        num = 0
        for product in products:
            push_prod = Purchased.objects.create(name=product.name, price=product.price,
                                                 manufacturer_id=product.manufacturer.id, note_id=note.id, count=curr_set[num])
            sum_price += (product.price * curr_set[num])
            push_prod.save(update_fields=["count"])
            num += 1
        print(sum_price)
        note.sum = sum_price
        note.save(update_fields=["sum"])

        note_vrn = Note.objects.all()
    return render(request, "index.html", context={'all': note_vrn})


def note_show(request, note_id):
    note = Note.objects.get(id=note_id)
    purchased = Purchased.objects.filter(note_id=note.id)
    return render(request, "note.html", context={'note': note, 'prod': purchased})


def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    customer = Customer.objects.filter(id=note.customer.id)
    customer.delete()
    note.delete()

    all_note = Note.objects.all()
    return render(request, "index.html", context={'all': all_note})


def download_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['Название', 'Производитель', 'Цена'])
    products = Product.objects.all()
    for product in products:
        writer.writerow([str(product.name), product.manufacturer.name, product.price])
    return response


def convert_id_to_integer_list(list_objects):
    curr_list = []
    for i in list_objects:
        curr_list.append(int(i))
    return curr_list


def convert_to_int(array):
    curr_list = []
    for i in array:
        if i == '':
            continue
        else:
            curr_list.append(int(i))
    return curr_list
