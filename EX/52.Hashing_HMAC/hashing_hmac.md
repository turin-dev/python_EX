# 52장 – 해싱과 메시지 인증

암호화 해시 함수와 메시지 인증 코드(MAC)는 데이터 무결성과 진위를 확인하는 데 필수적인 도구다. 파이썬의 `hashlib` 모듈은 여러 보안 해시 알고리즘에 대한 공통 인터페이스를 제공하고, `hmac` 모듈은 HMAC(Hash‑based Message Authentication Code)의 표준 구현을 제공한다. 이들 모듈을 사용하면 임의의 바이트 스트림에 대한 다이제스트를 생성하고 이를 안전하게 비교할 수 있다【796865090320013†L74-L97】【650517981507635†L51-L118】.

## `hashlib`를 이용한 해싱

SHA‑256, SHA‑3, BLAKE2와 같은 해시 함수는 데이터의 고유한 신원값인 고정 길이 다이제스트를 생성한다. `hashlib` 모듈은 각 알고리즘에 대한 생성자를 제공하며, 해시 객체를 만들어 `update()`로 데이터를 공급하고 `digest()`(바이트) 또는 `hexdigest()`(16진수 문자열)로 다이제스트를 가져올 수 있다【796865090320013†L74-L97】. 예를 들면 다음과 같다:

```python
import hashlib

# 문자열의 SHA‑256 해시를 계산한다
message = "Hello, world!".encode("utf‑8")
sha256 = hashlib.sha256()
sha256.update(message)
digest = sha256.hexdigest()
print(digest)

# hashlib.new()를 사용한 간편한 호출
digest2 = hashlib.new("sha256", message).hexdigest()
print(digest2)
```

스트림이나 큰 파일을 해시할 때는 `update()`를 반복 호출하여 청크를 점진적으로 공급한다. `hexdigest()`는 사람이 읽을 수 있는 16진수 문자열을 반환하고, 원시 바이트가 필요할 때는 `digest()`를 사용한다. 모듈은 SHA‑512, SHA3‑256, BLAKE2b, MD5 등의 알고리즘도 제공하지만, 보안이 중요한 상황에서는 MD5와 같은 구식 알고리즘을 피해야 한다【796865090320013†L74-L97】.

## `hmac`을 이용한 메시지 인증

HMAC는 비밀 키를 해시 함수와 결합해 메시지 인증 코드를 생성한다. 파이썬의 `hmac` 모듈은 RFC 2104를 구현하며, 고정된 다이제스트 크기를 가진 해시 함수라면 어떤 것이든 선택해 사용할 수 있다【650517981507635†L51-L60】. HMAC을 계산하려면 `hmac.new(key, msg, digestmod)`를 호출하는데, 여기서 `key`는 비밀 키이고 `msg`는 초기 메시지다. 이후 `update()`로 추가 데이터를 공급하고 `digest()`나 `hexdigest()`로 결과를 얻을 수 있다【650517981507635†L56-L99】.

```python
import hmac
import hashlib

secret = b"super‑secret‑key"
message = b"The quick brown fox jumps over the lazy dog"

mac = hmac.new(secret, message, hashlib.sha256)
print(mac.hexdigest())

# 추가 데이터를 업데이트한다
mac.update(b" extra data")
print(mac.hexdigest())
```

두 다이제스트를 안전하게 비교하려면 `hmac.compare_digest(a, b)`를 사용한다. 이 함수는 시간차 공격을 줄이기 위해 상수 시간 비교를 수행한다【650517981507635†L101-L118】.

## 요약

파일, 비밀번호, 메시지의 안전한 다이제스트를 계산할 때는 `hashlib`을 사용하라. 항상 SHA‑256이나 SHA‑3처럼 최신 알고리즘을 선택한다. 인증이 필요할 때는 비밀 키와 함께 `hmac`을 사용해 메시지가 변조되지 않았음을 확인한다. 다이제스트를 `==`로 비교하는 대신, 보안을 위해 `compare_digest()`를 사용하는 것이 좋다【650517981507635†L101-L118】.