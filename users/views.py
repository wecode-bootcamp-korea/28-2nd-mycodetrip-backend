import json
import jwt
import datetime
import pytz

import requests
from django.http import JsonResponse
from django.views import View

from users.models import User
from mycodetrip.config import SECRET_KEY

class AuthorizationView(View):
    def post(self, request):
        # 1. frontend로부터 access token을 받음
        access_token = request.headers["Authorization"]

        # 2. access token 이용해 카카오로부터 유저 정보 받아옴
        headers = {
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "Authorization": f'Bearer {access_token}'
        }
        response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)
        response.raise_for_status()
        response = response.json()

        kakao_id = response["id"]
        nickname = response["properties"]["nickname"]
        email = response["properties"].get("account_email")

        # 3. 회원가입 or 로그인
        user, is_created = User.objects.get_or_create(
            kakao_id=kakao_id,
            nickname=nickname,
            email=email
        )

        now = datetime.datetime.now(pytz.utc)

        payload = {
            "id": user.id,
            "exp": now + datetime.timedelta(days=7),
            "iat": now,
        }
        access_token = jwt.encode(payload, SECRET_KEY, "HS256")

        return JsonResponse({"access_token": access_token}, status=200)
