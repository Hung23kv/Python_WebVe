from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_name'):
            messages.error(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('login')  # Redirect to your login URL
        
        if request.session.get('role') != 'admin':
            messages.error(request, 'Bạn không có quyền truy cập trang này!')
            return redirect('home')  # Redirect to home page
            
        return view_func(request, *args, **kwargs)
    return wrapper