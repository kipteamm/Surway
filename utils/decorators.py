from django.shortcuts import redirect
from django.http import HttpRequest

from authentication.models import User


def requires_login(view_func):
    def _wrapped_view(request: HttpRequest, *args, **kwargs):

        if User.objects.filter(token=request.COOKIES.get('au_id')).exists():
            user = User.objects.get(token=request.COOKIES.get('au_id'))

            request.user = user # type: ignore

            return view_func(request, *args, **kwargs)
        
        else:
            next = request.get_full_path()

            if next:
                next = f'?next={next}'

            return redirect(f'/login{next}')

    return _wrapped_view