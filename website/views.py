from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
import os
from config import settings
from django.views.decorators.csrf import csrf_exempt
import json

# home page
def home(request):
    return render(request, 'home.html')

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