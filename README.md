# Do It Django 블로그 프로젝트

Django로 만든 개인 블로그입니다.

## 설치 및 실행

### 1. 가상환경 생성 및 활성화
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. 패키지 설치
```bash
pip install django pillow django-extensions ipython
```

### 3. 마이그레이션
```bash
python manage.py migrate
```

### 4. 관리자 계정 생성
```bash
python manage.py createsuperuser
```

### 5. 서버 실행
```bash
python manage.py runserver
```

## 주요 URL

| URL | 설명 |
|-----|------|
| `/` | 홈(랜딩 페이지) |
| `/blog/` | 블로그 포스트 목록 |
| `/blog/<pk>/` | 포스트 상세 |
| `/blog/create/` | 포스트 작성 |
| `/blog/category/<slug>/` | 카테고리별 포스트 |
| `/about_me/` | 소개 페이지 |
| `/admin/` | 관리자 페이지 |

## 앱 구성

- **blog** : 포스트, 카테고리 관리
- **single_pages** : 랜딩 페이지, 소개 페이지

## Django 쉘 (IPython 연동)

```bash
python manage.py shell_plus
```
