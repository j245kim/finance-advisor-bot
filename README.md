# 금융 투자 성향 조사 웹 애플리케이션

이 프로젝트는 사용자의 금융 투자 성향 조사를 기반으로 투자 성향 점수를 계산하고, 이를 통해 사용자의 투자 유형을 알려주고 이에 적합한 금융 정보를 제공하는 웹 애플리케이션입니다. Django, HTML, CSS, JavaScript, TTS, Hugging Face LLM 모델, Google Translate API 등을 활용하여 만들어졌습니다.

## 주요 기능

- **투자 성향 조사**: 사용자에게 다양한 금융 관련 질문을 제공하고, 각 항목에 대해 점수를 계산합니다.
- **자동화된 피드백 제공**: 조사 결과를 바탕으로 사용자의 투자 성향에 맞는 정보를 제공하며, 외부 API를 통해 추가적인 피드백을 제공합니다.
- **음성 피드백**: Text-to-Speech (TTS) 기술을 사용하여 사용자에게 음성으로 피드백을 제공합니다.
- **다국어 지원**: Google Translate API를 통해 다양한 언어로 질문과 결과를 번역하여 다국적 사용자에게 서비스를 제공합니다.
- **Hugging Face LLM 모델**: 사용자의 응답에 맞는 세부적인 피드백을 제공하기 위해 Hugging Face의 언어 모델을 활용합니다.
- **실시간 데이터 전송**: 조사를 완료한 후, 계산된 데이터를 API로 전송하고, 서버에서 처리된 응답을 실시간으로 사용자에게 제공합니다.

## 기술 스택

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Text-to-Speech**: TTS (Text to Speech)
- **Language Model**: Hugging Face LLM
- **Translation**: Google Translate API
- **API 호출**: Fetch API

## 설치 및 실행

### 1. 클론

먼저, GitHub에서 프로젝트를 클론합니다:

```bash
git clone https://github.com/j245kim/finance-advisor-bot.git
cd finance-advisor-bot
```

cd myproject 이후
``` bash
python manage.py runserver
```

# 프론트엔드 
프론트엔드는 HTML, CSS, JavaScript를 사용하여 작성되었습니다. 프로젝트 폴더의 manage.py를 runserver 하면 설문조사를 시작할 수 있습니다.

# 외부 서비스 설정
**Google Translate API**: 구글 클라우드 플랫폼에서 번역 API 발급후 한국어를 Hugging face에 맞추어 바꾸는 용도입니다. <br>
**Hugging Face LLM 모델**: Hugging Face 무료 ai api 모델을 활용하여 사용자의 투자 성향에 맞는 피드백을 제공하도록 설정합니다.

## 사용법
**설문조사 시작**: 웹 페이지를 열면, 사용자가 나이, 수입원, 투자 경험 등 여러 금융 관련 질문을 받습니다.<br>
**결과 보기**: 조사를 완료하면, 자동으로 점수가 계산되어 사용자의 투자 성향에 맞는 결과를 제공하고, 이를 바탕으로 관련 피드백을 제공합니다.<br>
**음성 안내**: TTS 기술을 통해 ai한테 질문!

## 예시
설문 질문 예시:
- 나이는 어떻게 되십니까?
- 연간 수입은 어떻게 되십니까?
- 금융 자산의 비중은 어느 정도입니까?
- 투자 경험은 어떠한가요?

## 결과 예시:
- 투자 성향: 안정적인 수익을 원하지만, 원금 보장이 중요함.
- 추천 투자 유형: 안전한 투자, 예적금 수익률을 넘는 안정적인 투자
