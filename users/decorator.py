import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from django.http    import JsonResponse

from mycodetrip.config  import SECRET_KEY
from users.models       import User

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers["Authorization"]
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms="HS256")
            user         = User.objects.get(id=payload.get("id", 0))
            request.user = user
            
        except KeyError:
            return JsonResponse({"message":"NO_TOKEN"}, status=400)

        except DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

        except ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper
