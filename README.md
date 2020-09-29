# 소프트웨어공학 프로젝트 서버

### 소개
창업정보 공유 웹서비스 소프트웨어입니다. <br/>
팀: 최세홍(팀장), 김재훈, 백동우, 김경남

### 서버 실행 명령어
```
# 깃 허브에서 소스코드를 다운로드 받습니다.
git clone git@github.com:kimja7045/software-engineering-server.git

# 받은 프로젝트 폴더 경로로 이동합니다.
software_engineering_server

# 프로젝트 내의 가상환경을 만들어줍니다.
python -m venvvenv

# 가상환경을 활성화해줍니다.
. venv/bin/activate         - mac
.venv\Scripts\activate     - window

# 프로젝트에 사용된 모든 패키지를 간편하게 설치하기 위해 다음 명령어를 입력합니다. 
pip install -r requirements.txt

# 데이터베이스에 변경이 있으므로 이를 반영해주는 migrate 명령어를 입력합니다.
python manage.py migrate

# 웹 서버를 실행합니다.
python manage.py runserver
```
