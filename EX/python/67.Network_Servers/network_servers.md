# 제67장 – 네트워크 서버 구축

파이썬 표준 라이브러리에는 소켓과 상위 수준 프로토콜을 활용해 네트워크 서버를 구현할 수 있는 모듈이 포함되어 있습니다. `socket` 모듈은 BSD 소켓 API에 대한 저수준 인터페이스를 제공하며, C 시스템 호출을 파이썬 객체 메서드로 변환합니다【634526119538162†L67-L86】. 이 위에 `socketserver`와 `http.server`는 TCP와 HTTP 서버를 쉽게 구축할 수 있는 기본 클래스를 제공합니다. 또한 `ftplib`, `smtplib`, `email` 등과 같은 모듈을 사용하면 FTP 서버와 상호작용하고, SMTP를 통해 이메일을 보내며, MIME 메시지를 구성할 수 있습니다.

## `socketserver`로 TCP 서버 작성

`socketserver`는 동기식 TCP 및 UDP 서버를 위한 기본 클래스를 제공합니다. 서버를 만들려면 `BaseRequestHandler`를 상속하여 `handle()` 메서드를 재정의한 후, `TCPServer` 인스턴스를 생성하고 `serve_forever()`를 호출합니다.

```python
import socketserver

class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        print("Received", data)
        self.request.sendall(data)

if __name__ == "__main__":
    with socketserver.TCPServer(("localhost", 8000), EchoHandler) as server:
        print("Echo server running on port 8000")
        server.serve_forever()
```

## 간단한 HTTP 서버

`http.server` 모듈은 간단한 정적 콘텐츠 제공에 적합한 기본 HTTP 서버를 제공합니다. `http.server.SimpleHTTPRequestHandler`는 현재 디렉터리의 파일을 서비스합니다. 명령줄에서 `python -m http.server 8000`을 실행하거나 프로그램에서 `HTTPServer`를 직접 인스턴스화하여 서버를 시작할 수 있습니다.

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler

httpd = HTTPServer(("localhost", 8080), SimpleHTTPRequestHandler)
print("Serving HTTP on port 8080…")
httpd.serve_forever()
```

## FTP 및 이메일 프로토콜

* **`ftplib`** – FTP 서버에 연결하여 디렉터리를 나열하고 파일을 다운로드 또는 업로드합니다. 일반 FTP를 위한 `FTP` 클래스와 TLS 암호화를 위한 `FTP_TLS` 클래스가 있습니다.
* **`smtplib`** – SMTP를 통해 이메일을 보냅니다. `SMTP` 인스턴스를 생성한 뒤 연결하고, `sendmail()` 메서드에 발신자, 수신자 목록과 메시지를 전달합니다.
* **`email`** – MIME 메시지를 구성합니다. `email.message.EmailMessage` 클래스를 사용하여 헤더와 첨부 파일을 가진 구조화된 이메일을 생성할 수 있습니다.

## 요약

BSD 소켓 호출을 파이썬 메서드로 변환한 `socket` 모듈과 그 위의 `socketserver`를 사용하여 사용자 정의 네트워크 서버를 구현할 수 있습니다【634526119538162†L67-L86】. 단순한 파일 제공을 위해서는 `http.server`가 손쉽게 HTTP 서버를 제공하며, `ftplib`와 `smtplib` 같은 프로토콜별 모듈을 사용하면 외부 라이브러리 없이 FTP와 이메일과 상호작용할 수 있습니다.