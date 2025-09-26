from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
import os
from config import settings
from django.views.decorators.csrf import csrf_exempt
import json
from .models import OTP, User, Category, Product, Customer, Invoice, InvoiceProduct
from django.db.models import Q, F, Sum, Count, Avg, Max, Min, Exists, OuterRef, Subquery, When, Case, Value, CharField, DateField, DateTimeField
from django.core.serializers import serialize

# home page
def home(request):
    #return render(request, 'home.html')
    res = User.objects.filter().select_related('categories').values(
        'id', 
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff', 
        'is_active', 
        'date_joined', 
        'last_login', 
        'categories__id', 
        'categories__name', 
        'categories__description', 
        'categories__created_at', 
        'categories__updated_at'
    )

    res2 = Category.objects.filter().select_related('user').values(
        'id',
        'name',
        'description',
        'created_at',
        'updated_at',
        'user__id',
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
        'user__is_staff',
        'user__is_active',
        'user__date_joined',
        'user__last_login'
    )
    return JsonResponse({'data': list(res2)}, status=200)

"""
    Product.objects.create(
        name='Samsung Galaxy S23',
        description='Latest Samsung flagship smartphone with cutting-edge features.',
        price=999.99,
        unit='pcs',
        img_url='https://example.com/samsung-galaxy-s23.jpg',
        stock=100,
        category_id=1,
        user_id=1   
    )
    return JsonResponse({'message': 'Home Page'}, status=200)
"""

"""
    # Insert Multiple Records
    products = [
        Product(
            name='Apple iPhone 14', 
            description='Latest Apple flagship smartphone with advanced features.',
            price=1099.99,
            unit='pcs',
            img_url='https://example.com/iphone-14.jpg',
            stock=50,
            category_id=1,
            user_id=1
        ),
        Product(
            name='Dell XPS 13',
            description='High-performance laptop with sleek design and powerful features.',
            price=1299.99,
            unit='pcs',
            img_url='https://example.com/dell-xps-13.jpg',
            stock=20,
            category_id=1,
            user_id=1
        ),
        Product(
            name='Sony PlayStation 5',
            description='Next-generation gaming console with immersive gaming experience.',
            price=499.99,
            unit='pcs',
            img_url='https://example.com/playstation-5.jpg',
            stock=30,
            category_id=1,
            user_id=1
        )
    ]

    # Add more products as needed
    Product.objects.bulk_create(products)
    return JsonResponse({'message': 'All Product inserted successfully'}, status=200)
"""

# Product Insert & Delete Operations
@csrf_exempt
def product_add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name        = data.get('name')
            description = data.get('description', '')
            price       = data.get('price', 0)
            unit        = data.get('unit', 'pcs')
            img_url     = data.get('img_url', '')
            stock       = data.get('stock', 0)
            category_id = data.get('category_id')
            user_id     = data.get('user_id')
            user_id     = data.get('user_id')
            user_id     = data.get('user_id')
            if not all([name, category_id, user_id]):
                return JsonResponse({'error': 'Name, Category ID, and User ID are required.'}, status=400)
            category = Category.objects.get(id=category_id)
            product = Product.objects.create(name=name, description=description, price=price, unit=unit, img_url=img_url, stock=stock, category=category, user_id=user_id)
            return JsonResponse({'message': 'Product added successfully', 'product_id': product.id}, status=201)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def product_edit(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            product = Product.objects.get(id=id)
            product.name        = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.price       = data.get('price', product.price)
            product.unit        = data.get('unit', product.unit)
            product.img_url     = data.get('img_url', product.img_url)  
            product.stock       = data.get('stock', product.stock)
            category_id         = data.get('category_id')
            if category_id:
                category = Category.objects.get(id=category_id)
                product.category = category
            product.save()
            return JsonResponse({'message': 'Product updated successfully'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@csrf_exempt
def product_delete(request, id):
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
# Practice ORM
def practice_orm(request):
    # Advanced Filtering Examples
    # Not In Query
    res1 = Product.objects.exclude(price__in=[50, 100]).values()
    # Not Equal
    res2 = Product.objects.exclude(price=100).values()
    # Greater Than
    res3 = Product.objects.filter(price__gt=100).values()

    # Range Operators
    res1 = Product.objects.filter(price__range=[50, 100]).values()
    # Exact Match (Case Sensitive)
    res2 = Product.objects.filter(name__exact='Samsung Galaxy S23').values()
    # Exact Match (Case Insensitive)
    res3 = Product.objects.filter(name__iexact='samsung galaxy s23').values()
    # Ends With (Case Sensitive)
    res4 = Product.objects.filter(name__endswith='e').values()
    # Ends With (Case Insensitive)
    res5 = Product.objects.filter(name__iendswith='E').values()
    # Contains (Case Sensitive)
    res6 = Product.objects.filter(name__contains='Galaxy').values()
    # Contains (Case Insensitive)       
    res7 = Product.objects.filter(name__icontains='galaxy').values()
    # Starts With (Case Sensitive)
    res8 = Product.objects.filter(name__startswith='S').values()
    # Starts With (Case Insensitive)
    res9 = Product.objects.filter(name__istartswith='s').values()
    # Regex Match (Case Sensitive)
    res10 = Product.objects.filter(name__regex=r'^[A-Z]').values()
    # Regex Match (Case Insensitive)    
    res11 = Product.objects.filter(name__iregex=r'^[a-z]').values()
    # In
    res12 = Product.objects.filter(name__in=['Samsung Galaxy S23', 'Apple iPhone 14']).values()
    # Is Null
    res13 = Product.objects.filter(img_url__isnull=True).values()
    # Is Not Null
    res14 = Product.objects.filter(img_url__isnull=False).values()
    # AND Condition
    res15 = Product.objects.filter(price__gt=100, stock__lt=50).values()
    # OR Condition
    res16 = Product.objects.filter(Q(price__gt=100) | Q(stock__lt=50)).values()
    # F Expressions
    res17 = Product.objects.filter(stock__lt=F('price')).values()
    # Exists
    subquery = Category.objects.filter(id=OuterRef('category_id'), name__icontains='Electronics')
    res18 = Product.objects.annotate(category_exists=Exists(subquery)).filter(category_exists=True).values()
    # Subquery
    subquery = Category.objects.filter(name__icontains='Electronics').values('id')
    res18 = Product.objects.filter(category_id__in=Subquery(subquery)).values()
    

    # Contains (Case Sensitive)
    res19 = Product.objects.filter(name__contains='ss').values()

    # Contains (Case Insensitive)
    res20 = Product.objects.filter(name__icontains='SS').values()

    #Starts With (Case Sensitive)
    res21 = Product.objects.filter(name__startswith='S').values()

    #Starts With (Case Insensitive)
    res22 = Product.objects.filter(name__istartswith='s').values()

    res1 = Product.objects.filter(price=100).values()
    # Not Equal
    res2 = Product.objects.exclude(price=100).values()
    # Greater Than
    res3 = Product.objects.filter(price__gt=100).values()
    # Less Than
    res4 = Product.objects.filter(price__lt=100).values()
    # Greater Than or Equal
    res5 = Product.objects.filter(price__gte=100).values()
    # Less Than or Equal
    res6 = Product.objects.filter(price__lte=100).values()
    # In
    res7 = Product.objects.filter(price__in=[50, 100, 150]).values()
    # Between
    res8 = Product.objects.filter(price__range=[50, 150]).values()
    # Is Null
    res9 = Product.objects.filter(img_url__isnull=True).values()
    # Is Not Null
    res10 = Product.objects.filter(img_url__isnull=False).values()
    # Like
    res11 = Product.objects.filter(name__icontains='phone').values()
    # Starts With
    res12 = Product.objects.filter(name__istartswith='S').values()
    # Ends With
    res13 = Product.objects.filter(name__iendswith='e').values()
    # AND
    res14 = Product.objects.filter(price__gt=100, stock__lt=50).values()
    # OR
    res15 = Product.objects.filter(Q(price__gt=100) | Q(stock__lt=50)).values()
    # F Expressions
    res16 = Product.objects.filter(stock__lt=F('price')).values()
    # Exists
    subquery = Category.objects.filter(id=OuterRef('category_id'), name__icontains='Electronics')       
    res17 = Product.objects.annotate(category_exists=Exists(subquery)).filter(category_exists=True).values()
    # Subquery
    subquery = Category.objects.filter(name__icontains='Electronics').values('id')
    res18 = Product.objects.filter(category_id__in=Subquery(subquery)).values()

    # Conditional Expressions
    return JsonResponse({
        'res1': list(res1),
        'res2': list(res2),
        'res3': list(res3),
        'res4': list(res4),
        'res5': list(res5),
        'res6': list(res6),
        'res7': list(res7),
        'res8': list(res8),
        'res9': list(res9), 
        'res10': list(res10),
        'res11': list(res11),
        'res12': list(res12),
        'res13': list(res13),
        'res14': list(res14),
        'res15': list(res15),
        'res16': list(res16),
        'res17': list(res17),
        'res18': list(res18),
        'res19': list(res19),
        'res20': list(res20),
        'res21': list(res21),
        'res22': list(res22),
    
    }, status=200)
                                                                              

    #aggregation = Customer.objects.aggregate(total_customers=Count('id'), avg_id=Avg('id'), max_id=Max('id'), min_id=Min('id'), sum_id=Sum('id'))
    #return JsonResponse(aggregation, status=200)
    # return render(request, 'home.html')
    # Fetch all customers from the database
    """
    customers = Customer.objects.all()
    result = serialize('json', customers, fields=('id', 'name', 'email', 'phone', 'address'))
    return JsonResponse({'data': json.loads(result)}, status=200)
    """

    # Fetch single customer from the database
    """
    customer = Customer.objects.get(id=1)
    customer_data = {
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'address': customer.address
    }   
    return JsonResponse(customer_data, status=200)
    """

    # Fetch first customer from the database
    """
    customer = Customer.objects.first() # objects.last()
    customer_data = {
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'address': customer.address
    }
    return JsonResponse(customer_data, status=200)
    """

    # Fetch customers with filter from the database
    # name__incontains, name__startswith, name__endswith
    # name__contains=case-sensitive 
    # name__icontains=case-insensitive
    # customers = Customer.objects.filter(name__icontains='John')
    # customers = Customer.exclude(name__icontains='John')
    # customers = Customer.objects.all().order_by('-id')  #  .order_by('id')
    # customers = Customer.objects.all().order_by('name') # ASC name
    # customers = Customer.objects.all().order_by('-name') # DESC name
    # customers = Customer.objects.all()[0:5] # slicing limiting
    # customers = Customer.objects.all()[::-1] # reversing
    # customers = Customer.objects.count() # total count
    # customers = Customer.objects.values('name').distinct() # distinct values only
    # return JsonResponse({'data':list(customers)}, status=200)
 
    # Value list queryset
    """
    customers = Customer.objects.values_list('name', 'email') # flat=True for single field
    return JsonResponse({'data':list(customers)}, status=200)
    """

    # Query set chaining
    """
    customers = Customer.objects.filter(name__icontains='Zahid Hasan').order_by('-id')[0:5]
    result = serialize('json', customers, fields=('id', 'name', 'email', 'phone', 'address'))
    return JsonResponse({'data': json.loads(result)}, status=200)#
    """

    # Raw SQL Query
    """
    customers = Customer.objects.raw('SELECT * FROM website_customer WHERE name LIKE %s', ['%Ali Khan%'])
    result = serialize('json', customers, fields=('id', 'name', 'email', 'phone', 'address'))
    return JsonResponse({'data': json.loads(result)}, status=200)
    """

    """
    customers = Customer.objects.all().values('id', 'name', 'email', 'phone', 'address')
    query = str(customers.query)
    return JsonResponse({'data': list(customers), 'query': query}, status=200)
    """

# about page
def about(request):
    return render(request, 'about.html')

# projects page  
def projects(request):
    return render(request, 'projects.html')

# testimonial page
def testimonial(request):
    return render(request, 'testimonial.html')

# hire page
def hire(request):
    return render(request, 'hire.html')

# blog page
def contact(request):
    return render(request, 'contact.html')

# api plain text
def demo1(request):
    return HttpResponse('This is the blog page')

# api number response
def demo2(request):
    return HttpResponse(2000)

# api boolean response
def demo3(request):
    return HttpResponse(True)

# api json response
def demo4(request):
    data = {
        'name': 'John',
        'age': 30,
        'address': {
            'street': '123 Main St',
            'city': 'New York'
        }
    }
    return JsonResponse(data)

# api 404 response
def demo5(request):
    return HttpResponseNotFound('404 Not Found')

# api redirect response
def demo6(request):
    return HttpResponseRedirect('/api/demo4')

# with status code
def demo7(request):
    # 200 OK by default,
    # 201 Created
    # 202 Accepted
    # 203 Non-Authoritative Information
    # 204 No Content
    # 205 Reset Content
    # 206 Partial Content
    # 207 Multi-Status
    # 208 Already Reported
    # 226 IM Used
    # 300 Multiple Choices
    # 301 Moved Permanently
    # 302 Found
    # 303 See Other
    # 304 Not Modified
    # 305 Use Proxy
    # 307 Temporary Redirect
    # 308 Permanent Redirect
    # 400 Bad Request
    # 401 Unauthorized
    # 402 Payment Required
    # 403 Forbidden
    # 404 Not Found
    # 405 Method Not Allowed    
    # 406 Not Acceptable
    # 407 Proxy Authentication Required
    # 408 Request Timeout
    # 409 Conflict
    # 410 Gone
    # 411 Length Required
    # 412 Precondition Failed
    # 413 Payload Too Large
    # 414 URI Too Long
    # 415 Unsupported Media Type
    # 416 Range Not Satisfiable
    # 417 Expectation Failed
    # 418 I'm a teapot
    # 421 Misdirected Request
    # 422 Unprocessable Entity
    # 423 Locked
    # 424 Failed Dependency
    # 425 Too Early
    # 426 Upgrade Required
    # 428 Precondition Required
    # 429 Too Many Requests
    # 431 Request Header Fields Too Large
    # 451 Unavailable For Legal Reasons
    # 500 Internal Server Error
    # 501 Not Implemented
    # 502 Bad Gateway   
    # 503 Service Unavailable
    # 504 Gateway Timeout
    # 505 HTTP Version Not Supported
    # 506 Variant Also Negotiates
    # 507 Insufficient Storage
    # 508 Loop Detected
    # 509 Bandwidth Limit Exceeded
    # 510 Not Extended
    # 511 Network Authentication Required
    # 599 Network Connect Timeout Error
    return HttpResponse('Status Code Demo', status=201)

# with header
def demo8(request):
    response = HttpResponse('This response has a custom header')
    response['Custom-Header'] = 'Custom-Value'
    response['token'] = '123'
    response['auth-token'] = '12345'
    response['cookie'] = 'Custom-Cookie'
    return response

# with response cookie
def demo9(request):
    response = HttpResponse('This response has a cookie')
    response.set_cookie('cookie_name', 'cookie_value', max_age=3600)
    response.set_cookie('user_id', '12345', httponly=True)
    response.set_cookie('session_id', 'abcdef', secure=True)
    return response

# file download response
def download(request):
    # code to handle file download
    # file path
    file_path = os.path.join(settings.BASE_DIR, 'uploads/bill.pdf')

    # file name
    # The `file_name` variable in the `download` function is storing the base name of the file path.
    # It is extracted using the `os.path.basename()` function, which returns the last component of the
    # path. In this case, it is used to set the filename for the downloaded file in the response
    # headers.
    file_name = os.path.basename(file_path)

    # check if file exists
    if os.path.exists(file_path):
        # open the file in binary mode
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            return response 

# file binary rsponse
def binary_response(request):
    # code to handle file download
    # file path
    file_path = os.path.join(settings.BASE_DIR, 'uploads/bill.pdf')

    # check if file exists
    if os.path.exists(file_path):
        # open the file in binary mode
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

# Method GET, POST, PUT, DELETE, PATCH
@csrf_exempt
def demo10(request):
    if request.method == 'GET':
        return HttpResponse('This is a GET request')
    elif request.method == 'POST':
        return HttpResponse('This is a POST request')
    elif request.method == 'PUT':
        return HttpResponse('This is a PUT request')
    elif request.method == 'DELETE':
        return HttpResponse('This is a DELETE request')
    elif request.method == 'PATCH':
        return HttpResponse('This is a PATCH request')
    else:
        return HttpResponse('This is a unknown request')
    
# Method with URL Query Parameters
def demo11(request):
    name = request.GET.get('name', 'Guest')
    age = request.GET.get('age', '0')
    address = request.GET.get('address', 'Unknown')
    mobile = request.GET.get('mobile', '0000000000')

    return HttpResponse(f'Hello {name}, you are {age} years old. You live in {address}. Your mobile number is {mobile}.', status=200)

# Method with request header
def demo12(request):
    token1 = request.headers.get('token1', 'Not Provided')
    token2 = request.headers.get('token2', 'Not Provided')
    token3 = request.headers.get('token3', 'Not Provided')

    return HttpResponse(f'Token1: {token1}, Token2: {token2}, Token3: {token3}', status=200)

# Method with request body  JSON
@csrf_exempt
def demo13(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON', status=400)
        return JsonResponse(data, status=200)
    else:
        return JsonResponse('This is a GET request', status=200)
    

# Method with request body Form Data
@csrf_exempt
def demo14(request):
    if request.method == 'POST':
        data = request.POST.dict()
        return JsonResponse(data, status=200)
    
       # name    = request.POST.get('name', 'Guest')
       # age     = request.POST.get('age', '0')
       # address = request.POST.get('address', 'Unknown')
       # mobile  = request.POST.get('mobile', '0000000000')

       # return HttpResponse(f'Hello {name}, you are {age} years old. You live in {address}. Your mobile number is {mobile}.', status=200)
    else:
        return HttpResponse('This is a GET request', status=200)
    
# Multipart Form Data (File Upload)
@csrf_exempt
def demo15(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            file_name = file.name
            file_size = file.size
            file_type = file.content_type

            save_path = os.path.join(settings.BASE_DIR, 'uploads', file.name)
            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            return HttpResponse(f'File Uploaded SUccessfully! File Name: {file_name}, File Size: {file_size} bytes, File Type: {file_type}', status=200)
        else:
            return HttpResponse('No file uploaded', status=400) 
    else:
        return HttpResponse('This is a GET request', status=200)
    
# Catch Request Cookies
def demo16(request):
    Cookie_1 = request.COOKIES.get('Cookie_1', 'Not Provided')
    Cookie_2 = request.COOKIES.get('Cookie_2', 'Not Provided')
    Cookie_3 = request.COOKIES.get('Cookie_3', 'Not Provided')

    return HttpResponse(f'Cookie 1: {Cookie_1}, Cookie 2: {Cookie_2}, Cookie 3: {Cookie_3}', status=200)

# Combination of all
@csrf_exempt
def all_demo(request):
    if request.method == 'POST':
        # URL Query Parameters
        name = request.GET.get('name', 'Guest')
        age = request.GET.get('age', '0')

        # Request Headers
        token1 = request.headers.get('token1', 'Not Provided')

        # Request Body JSON
        try:
            body_data = json.loads(request.body)
        except json.JSONDecodeError:
            body_data = {}

        # Form Data
        form_data = request.POST.dict()

        # File Upload
        file_info = {}
        if 'file' in request.FILES:
            file = request.FILES['file']
            file_info = {
                'file_name': file.name,
                'file_size': file.size,
                'file_type': file.content_type
            }
            save_path = os.path.join(settings.BASE_DIR, 'uploads', file.name)
            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        response_data = {
            'query_params': {
                'name': name,
                'age': age
            },
            'headers': {
                'token1': token1
            },
            'body_json': body_data,
            'form_data': form_data,
            'file_info': file_info
        }

        return JsonResponse(response_data, status=200)
    else:
        return HttpResponse('This is a GET request', status=200)