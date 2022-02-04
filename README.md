# mycodetrip 프로젝트

<img width=300 src=https://user-images.githubusercontent.com/50139787/151123589-b350ebe0-8857-409b-8a98-ccab343717a0.png>

마이코드트립은 마이리얼트립을 모티브로해 항공권 구매로직에 집중하여 클론코딩을 진행했습니다. 항공권 조건 검색, 항공권 리스트 조회, 원하는 조건으로 항공권 필터링, 항공권 선택 후 구매, 구매한 항공권은 마이페이지 확인 등 하나의 플로우를 구현했습니다.

<br>

## 🚀 개발 인원 및 기간

- 개발 기간 : 2022/1/10 ~ 2022/1/21 (2주간)
- 개발 인원 : 프론트엔드 4명, 백엔드 2명
- [프론트 github 링크](https://github.com/wecode-bootcamp-korea/28-2nd-mycodetrip-frontend)

<br>

## 📍 데모 영상

![마이코드트립_gif](https://user-images.githubusercontent.com/50139787/151123373-4772373a-3449-4cf8-9dbd-b348a2231f1d.gif)

<br>

## 🛠️ 기술스택

- Language : `python`
- Framework : `Django`
- Database : `MySQL`
- Infra : `AWS`(EC2, RDS, ECR), `Docker`, `docker-compose`

<br>

## 💡 ERD

<img width="1148" alt="스크린샷 2022-01-13 오후 9 32 35" src="https://user-images.githubusercontent.com/50139787/150078505-d0166c76-1749-4fa1-91db-6d11a1767278.png">

## 📝 구현 기능 명세

### 이찬주

> Mission 1 | 모델링

- 도착도시, 출발도시 처럼 한 테이블을 두번 참조하게 될 경우 related name을 주었음.
- 프론트로부터 받은 naive 날짜 객체를 timzone 정보를 더해서 aware 객체로 비교할 것.
- 항공 시간(flight time)은 timedelta 초 단위로 값 저장함.

> Mission 2 | DB 구축
- 항공편을 장거리, 중거리, 단거리로 나눠 datetime과 random 라이브러리를 활용해 DB 자동 생성함. 

> Mission 3 | 소셜 로그인
![OAuth2](https://user-images.githubusercontent.com/50139787/151287882-51c7fc71-df99-4f19-a4a5-9c017c7a0a0a.jpg)
[블로그 바로가기 >> Auth2.0를 이용해 소셜 로그인을 구현하기](https://velog.io/@evnif/OAuth2.0-social-login)

> Mission 4 | 항공권 리스트 페이지

- 선택 쿼리 파라미터 조건들을 통해 시간대, 항공사 등의 리스트 필터링을 `Q` 객체로 구현

> Mission 5 | 구매내역 조회 가능한 마이 페이지

- REST하게 엔드포인트를 구성하고 각 목적에 맞는 메소드를 활용해 자원을 관리. 장고 ORM을 활용해 적절한 쿼리 생성함.

> Mission 6 | AWS 서버에 Docker로 배포

- aws EC2 인스턴스와 RDB 데이터베이스를 통해 배포.
- docker-compose로 빌드한 이미지를 AWS ECR에 올리고 EC2서버에서 pull 받아서 컨테이너를 띄움

<br>

### 이민석

> Mission 1 | 모델 작성

- 모델링 작성 후 models.py와 diagram 작성

> Mission 2 | 오더 페이지

- random digits를 이용한 주문번호 생성 (랜덤에 적합한 uuid4로 변경)
- passengers를 리스트 형태로 받아서 한 번의 요청에 여러 정보 저장

> Mission 3 | 메인 페이지

- 여러 번 참조를 거치는 방식이 아닌 annotate를 이용하여 원하는 filter를 사용한 column을 생성하여 참조
- order_by("?")를 사용하여 같은 출력에 대한 이미지를 랜덤으로 출력
- request 값에 따라 다른 API호출하도록 구성

<br>

## Postman
- 포스트맨을 이용해 API 문서화를 진행했습니다.
- 이번 프로젝트에서 쿼리파라미터(출발도시, 도착날짜, 출발날짜, 도착날짜 등)로 많은 값들을 받아야했기 때문에 API 문서화가 굉장히 중요했습니다.
- 프론트엔드와 소통시 문서를 통해 1차적으로 커뮤니케이션 비용을 줄일 수 있었습니다.

![스크린샷 2022-01-27 오후 12 32 17](https://user-images.githubusercontent.com/50139787/151287237-813620eb-d397-40cb-a065-88bd4a99efe1.png)


## Trello

- 트렐로를 이용해 모든 업무들을 세분화 시켜 하나의 티켓으로 만들었습니다.
- 팀원들과 공유해야할 내용은 공지 탭을 통해 단일화하였습니다.
- 전체 프로세스를 네 가지 카테고리로 나눠서 각각의 티켓을 과정에 따라 하나씩 이동 시키며 프로젝트의 모든 일정과 업무를 관리했습니다.
- 각자 데일리 스탠드업 미팅 로그를 작성하고 10~20분내로 짧게 진행상황을 점검했습니다.
![스크린샷 2022-01-27 오후 12 28 00](https://user-images.githubusercontent.com/50139787/151286910-460cd449-4f9c-4932-961c-aaa0d8d77db8.png)
<br>

## Reference

- 이 프로젝트는 마이리얼트립 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무 수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
