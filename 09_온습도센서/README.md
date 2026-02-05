# 온습도 센서(DHT11/DHT22) 강의자료 (Markdown)

> 대상: 고등/입문 실습  
> 보드 기준: ESP32(3.3V)  
> 센서: DHT11 또는 DHT22(AM2302)

---

## 0. 한 줄 요약
- **온도**: 내부의 온도 센서(반도체/서미스터 계열)로 측정  
- **습도**: 습기(수분)량에 따라 **센서 내부 정전용량(C)** 이 변하는 원리를 이용  
- DHT 센서는 내부에서 측정/보정 후 **디지털 신호(단선 통신)** 로 값을 보내준다.

---

## 1. 학습 목표
- 센서를 ESP32에 배선하고, 라이브러리로 온습도를 읽을 수 있다.
---

## 2. 준비물
- ESP32 DevKit 1개
- DHT11 온습도 센서
- 점퍼선, 브레드보드
- (옵션) LED + 저항(220Ω), 버저(Active 추천)

---

## 4. 내부 원리(그림 설명용)
### 4.1 습도(정전용량 방식)
- 센서 내부에는 전극 2장 + 수분을 머금는 재료(폴리머)가 있고, 이게 **캐패시터**처럼 동작한다.
- 습도 ↑ → 재료가 물을 더 머금음 → **유전율(ε) 증가** → **용량(C) 증가**
- 내부 회로는 이 C 변화를 직접 재는 대신,
  - **RC 충전시간**(시간이 늘어남) 또는
  - **발진 주파수**(주파수가 감소)  
  같은 “시간/주파수 변화”로 측정해서 %RH로 변환한다.

### 4.2 온도(온도 센서)
- 내부 온도 센서 값을 읽고 보정하여 °C로 변환해 함께 출력한다.

---

## 5. 핀맵/배선
### 5.1 DHT 모듈(3핀) 기준
- **VCC** → ESP32 **3.3V**
- **GND** → ESP32 **GND**
- **DATA** → ESP32 **GPIO 4** (예시)

> 모듈형은 보통 **풀업저항이 내장**되어 있어 배선이 쉽다.

### 5.2 DHT “단품(4핀)” 주의
- 단품은 DATA에 **풀업저항(보통 4.7k~10kΩ)** 이 필요할 수 있음.
- 실습은 가능하면 모듈형 사용 권장.

---

## 6. 실습 1: 온습도 값 읽기(Serial 출력)
### 목표
- 2초마다 온도/습도를 읽어서 시리얼 모니터에 출력한다.
- 읽기 실패 시(타임아웃/NaN) 재시도 또는 오류 메시지를 출력한다.

---

### 6.1 Arduino IDE(ESP32) 예제 코드
> 라이브러리: `DHT sensor library`(Adafruit) + `Adafruit Unified Sensor` 설치 권장

```cpp
#include <DHT.h>

#define DHTPIN 4       // DATA 연결 핀
#define DHTTYPE DHT11  // DHT11이면 DHT11, DHT22면 DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  delay(2000); // DHT는 너무 자주 읽으면 실패할 수 있음

  float h = dht.readHumidity();
  float t = dht.readTemperature(); // 섭씨

  if (isnan(h) || isnan(t)) {
    Serial.println("[ERROR] Failed to read from DHT sensor!");
    return;
  }

  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" % | Temperature: ");
  Serial.print(t);
  Serial.println(" C");
}
