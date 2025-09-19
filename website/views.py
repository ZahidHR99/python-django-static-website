from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect, HttpResponseNotFound

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

