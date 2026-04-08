---
type: output
created: 2026-04-08
topic:
  - harness-engineering
  - agentic-workflow
  - multi-agent-systems
  - coding-agents
related_wiki:
  - Harness Engineering
  - Agentic Workflow
status: active
promotion_candidate: false
publish: true
---

# 프롬프트에서 하네스까지, 그리고 코드 에이전트 오케스트라 - Jonas Kim과 Addy Osmani 글 상세 해설 (2026-04-08)

## 질문
- Jonas Kim - 프롬프트에서 하네스까지 — AI 에이전틱 패턴 4년의 기록 (Article, 2026-04-05)
- Addy Osmani - The Code Agent Orchestra - what makes multi-agent coding work (Article, 2026-03-26)

이 두 raw가 각각 무슨 말을 하고 있는지, 서로 어떻게 연결되는지 자세하게 설명해 달라는 요청.

## 답변 요약
두 글은 연결해서 읽을 수는 있지만, 결이 꽤 다르다.

Jonas Kim의 글은 코딩 에이전트만을 직접 다루는 글이라기보다, 2022년 이후 AI 개발 전반에서 agentic pattern이 어떻게 이동해 왔는지를 시계열적으로 정리한 긴 개념사에 가깝다. prompt engineering → context engineering → harness engineering으로 초점이 이동한 이유와 각 단계의 한계를 역사적으로 설명하는 글이다.

Addy Osmani의 글은 그보다 훨씬 직접적으로 코딩 에이전트 운영을 다룬다. 특히 단일 에이전트에서 subagents, Agent Teams, worktree, quality gates, AGENTS.md, reviewer, Ralph loop로 넘어가는 멀티 에이전트 코딩 패턴을 실무적으로 설명한다.

즉 이 둘은 정확히 같은 층위의 글은 아니다.
- Jonas Kim = 에이전틱 패턴 전반의 변화사를 다루는 시계열적/개념적 글
- Addy Osmani = 코딩 에이전트, 특히 멀티 에이전트 오케스트레이션을 다루는 실무 글

겹치는 지점은 분명히 있다. 다만 Jonas를 Addy처럼 곧바로 "멀티 에이전트 운영 글"로 읽으면 조금 빗나가고, 반대로 Addy를 Jonas처럼 "패러다임 변천사 글"로 읽어도 초점이 흐려진다.

## 핵심 포인트
- 프롬프트 엔지니어링은 끝난 것이 아니라 더 큰 시스템의 일부가 되었다.
- 컨텍스트 엔지니어링은 “무엇을 말할까”보다 “무엇을 보여줄까”에 대한 설계다.
- 하네스 엔지니어링은 “에이전트가 실패하지 않도록 둘러싼 시스템을 어떻게 만들까”에 대한 설계다.
- 멀티 에이전트 코딩의 병목은 생성이 아니라 검증이다.
- 사람의 역할은 코드를 직접 많이 쓰는 것에서, 스펙 작성·분해·품질 기준 설정·판단 유지로 이동한다.
- 좋은 멀티 에이전트 운영은 단순히 에이전트를 많이 띄우는 것이 아니라, 분업·격리·검증·기억 축적을 함께 설계하는 일이다.

## 근거
### 1. Jonas Kim 글의 중심 주장
이 글은 2022~2026년 사이 업계의 관심사가 세 단계로 이동했다고 본다.
- Prompt Engineering: 어떤 말을 해야 모델이 잘 반응하는가
- Context Engineering: 모델이 잘 풀 수 있도록 어떤 정보를 창 안에 넣어야 하는가
- Harness Engineering: 모델이 도구를 쓰고 여러 턴에 걸쳐 일할 때, 전체 시스템을 어떻게 설계해야 하는가

여기서 핵심 문장은 “엄밀함은 사라지지 않고 이동한다”이다. 즉 AI가 코드를 생성한다고 해서 엔지니어링 rigor가 사라지는 게 아니라, 그것이 프롬프트 작성에서 컨텍스트 구성, 다시 하네스 설계로 이동했다는 주장이다.

### 2. Addy Osmani 글의 중심 주장
이 글은 단일 에이전트와의 pair programming에서 여러 에이전트를 병렬 조율하는 orchestration 시대로의 이동을 말한다.
- 한 에이전트는 컨텍스트 한계, 전문성 부족, 조정 부재라는 3개의 벽에 부딪힌다.
- subagents는 일부 문제를 해결한다.
- Agent Teams는 shared task list, dependency tracking, peer messaging, file locking 같은 coordination primitive를 제공한다.
- 그러나 에이전트를 많이 띄우는 것만으로는 부족하고, plan approval, hooks, reviewer, AGENTS.md, token budget, kill criteria 같은 quality gate가 필요하다.

여기서 핵심 문장은 “The bottleneck is no longer generation. It's verification.”이다.

## 세부 내용

## 1. Jonas Kim 글은 무엇을 말하나

### 1-1. 프롬프트 엔지니어링 시대의 흥분과 한계
Jonas는 Copilot과 ChatGPT가 등장했을 때 사람들이 “영어로 잘 말하면 소프트웨어를 만들 수 있다”고 믿게 된 순간을 짚는다. Chain-of-Thought, ReAct, Tree-of-Thought, Self-Refine, Reflection, Planning, Tool Use, Multi-Agent Collaboration 같은 패턴도 이 맥락에서 등장한다.

하지만 이 시기의 한계는 명확했다.
- 프롬프트가 좋아도 에이전트가 필요한 파일이나 규칙을 못 보면 틀린다.
- 같은 요청이라도 출력 편차가 심하다.
- 긴 작업에서는 프롬프트보다 에이전트가 실제로 접근한 정보가 더 중요해진다.
- “기존 코드를 재사용하라”라고 프롬프트에 써도, 컨텍스트에 그 코드가 없으면 소용이 없다.

즉 prompt engineering은 강력했지만, 실제 시스템 운영을 떠받치기엔 너무 얇은 층이었다는 것이다.

### 1-2. vibe coding의 숙취
Jonas 글에서 중요한 중간 장면이 vibe coding 비판이다. 그냥 AI가 만든 변경을 다 수락하고, 코드를 충분히 이해하지 않은 채 기능을 계속 늘리면 나중에 유지보수 불가능한 시스템이 생긴다.

여기서 메시지는 단순한 “AI 쓰지 마라”가 아니다. 핵심은 엄밀함의 위치를 잃으면 안 된다는 것이다.
- 규칙은 사람 머릿속이 아니라 코드나 시스템으로 강제되어야 한다.
- 실패는 즉각적이고 시끄럽게 드러나야 한다.
- 엔지니어는 타이핑보다 검증과 판단 쪽으로 이동해야 한다.

이 포인트는 Addy 글의 quality gates 논의와 거의 직결된다.

### 1-3. 컨텍스트 엔지니어링으로의 이동
Jonas는 2025년 이후 핵심 질문이 “어떻게 말할까”에서 “무엇을 넣을까”로 옮겨갔다고 본다.

여기서 중요한 개념들:
- stable prefix / variable suffix
- KV-cache hit rate
- Write / Select / Compress / Isolate
- 저장과 표현의 분리
- working context를 명시적 파이프라인으로 조립
- subagent에게 최소 권한의 컨텍스트만 전달

즉 좋은 에이전트는 문서를 많이 넣는 에이전트가 아니라, 필요한 것만 구조적으로 조립해서 보여주는 에이전트라는 점을 강조한다.

### 1-4. 그래도 컨텍스트만으로는 부족했다
Jonas 글이 중요한 이유는 context engineering도 최종 답은 아니라고 말하기 때문이다.
문제는 다음과 같다.
- 에이전트는 한 번의 호출이 아니라 여러 턴에 걸친 시스템이다.
- 도구 실패, 비용 폭주, 루프 반복, 보안 문제는 컨텍스트만 잘 넣는다고 해결되지 않는다.
- 완벽한 컨텍스트가 있어도, 그것을 소비하는 루프와 검증 시스템이 허술하면 실패한다.

그래서 나온 것이 harness engineering이다.

### 1-5. 하네스 엔지니어링의 핵심
Jonas는 에이전트 = 모델 + 하네스라는 관점을 소개한다. 하네스는 모델 외부의 모든 운영 시스템이다.

중요한 구조는 네 사분면이다.
- 결정론적 피드포워드: AGENTS.md, 규칙 문서, 코딩 가이드
- 결정론적 피드백: compiler, linter, type checker, tests
- 비결정론적 피드포워드: system prompt, 행동 제약
- 비결정론적 피드백: LLM reviewer, evaluator, semantic review

즉 하네스는 단지 프롬프트 파일이 아니라, 규칙·도구·검증·평가·권한·루프를 겹겹이 쌓는 방어 구조다.

### 1-6. Jonas 글의 가장 큰 가치
이 글의 진짜 가치는 유행어 설명이 아니라 “왜 업계의 중심이 이동했는가”를 서사적으로 이해하게 해준다는 점이다. 최근의 harness engineering 담론을 prompt/context 시대와 끊어진 신조어가 아니라, 앞선 실패를 흡수한 다음 단계로 보게 만든다.


## 2. Addy Osmani 글은 무엇을 말하나

### 2-1. conductor에서 orchestrator로
Addy는 예전에는 개발자가 AI 한 명과 대화하듯 일했다면, 이제는 여러 에이전트를 팀처럼 관리한다고 본다.
- conductor model: 단일 에이전트, 동기적, 대화창이 작업 공간
- orchestrator model: 여러 에이전트, 비동기적, 코드베이스 전체가 작업 공간

이 차이는 단순 UI 차이가 아니다. 개발자의 역할 자체를 바꾼다.
- 이제 중요한 것은 프롬프트 감각만이 아니라 스펙, 작업 분해, 체크포인트 설계, 결과 검증이다.

이 지점에서 Addy 글은 Jonas가 말한 하네스 시대의 인간 역할 변화를 실전 언어로 번역한다.

### 2-2. 왜 single-agent에 ceiling이 생기는가
Addy는 단일 에이전트가 세 가지 벽에 부딪힌다고 말한다.
- context overload
- no specialization
- no coordination

이 분석은 Jonas의 context/harness 논의와 정확히 맞물린다.
Jonas가 “한 에이전트에게 다 맡기면 결국 컨텍스트와 시스템 설계가 병목”이라고 했다면, Addy는 그 병목을 멀티 에이전트 운영의 관점에서 재정리한다.

### 2-3. subagents는 첫 번째 실전 패턴
Addy는 가장 먼저 시도할 멀티 에이전트 패턴으로 subagents를 제시한다.
예시 구조:
- Data Layer subagent
- Business Logic subagent
- API Routes subagent

여기서 중요한 포인트는 단순 병렬화가 아니라 dependency graph를 명시적으로 다루는 것이다.
- 독립 작업은 병렬 실행
- 의존 작업은 선행 결과가 준비될 때까지 대기
- parent orchestrator가 전체 그래프를 관리

이건 Hermes나 Claude Code 같은 도구를 사용할 때도 바로 적용 가능한 사고방식이다.

### 2-4. Agent Teams는 coordination primitive를 추가한다
subagents의 한계는 parent가 모든 조정을 수동으로 해야 한다는 점이다. Addy는 Agent Teams가 여기서 진짜 차이를 만든다고 본다.

핵심 메커니즘:
- shared task list
- dependency tracking
- peer-to-peer messaging
- file locking
- lead + teammates 구조

즉 여러 에이전트를 동시에 띄우는 것만으로는 멀티 에이전트가 아니고, 에이전트 사이의 조정 규칙이 있어야 진짜 orchestration이 된다는 것이다.

### 2-5. quality gates가 핵심이다
Addy 글의 제일 중요한 대목은 사실 멀티 에이전트 그 자체보다 quality gates다.

중요 패턴:
- plan approval: 코드 쓰기 전에 계획 검토
- hooks: TaskCompleted, TeammateIdle 같은 이벤트에 lint/test/security-scan 실행
- dedicated reviewer teammate: builder와 reviewer 분리
- AGENTS.md: 세션 간에 패턴과 함정을 축적
- token budgeting / kill criteria: stuck agent를 자동 중단

이 부분이 바로 하네스 엔지니어링의 실무 버전이다. Jonas가 개념적으로 설명한 “피드포워드 + 피드백 + 시스템 설계”를 Addy는 운영 패턴으로 구체화한다.

### 2-6. Ralph loop와 공장 모델
Addy는 Ralph loop를 통해 stateless-but-iterative 패턴도 소개한다.
- Pick
- Implement
- Validate
- Commit
- Reset

핵심은 한 번의 거대한 프롬프트로 오래 밀어붙이지 않고, 작은 원자적 태스크 단위로 컨텍스트를 리셋하며 반복하는 것이다. 이것은 컨텍스트 오염과 누적 혼란을 막는 하네스 전략이다.

그리고 Addy는 전체를 “factory model”로 묶는다.
- Plan
- Spawn
- Monitor
- Verify
- Integrate
- Retro

이건 사실 “에이전트에게 코드를 맡긴다”가 아니라 “소프트웨어를 생산하는 공장을 설계한다”는 선언에 가깝다.


## 3. 두 글은 어떻게 연결되나

### 3-1. Jonas는 왜를 설명하고, Addy는 어떻게를 설명한다
Jonas 글만 읽으면 개념적으로는 명확해진다. 하지만 실제 현장에서 무엇을 해야 하는지까지는 추상적일 수 있다.
Addy 글은 그 공백을 메운다.

연결하면 이렇게 된다.
- Jonas: prompt → context → harness로 이동한 이유 설명
- Addy: harness 시대의 운영 단위가 단일 agent에서 orchestration으로 바뀌었음을 설명

### 3-2. 공통 메시지: 사람의 역할은 판단 쪽으로 이동한다
두 글 모두 사람이 해야 할 일을 다르게 본다.
사람이 할 일:
- 스펙 작성
- 아키텍처 판단
- 작업 분해
- 검증 기준 설정
- 품질 게이트 유지
- 장기 기억 문서 관리

사람이 에이전트에게 넘길 수 있는 일:
- 좁은 범위의 구현
- 반복 작업
- 보일러플레이트 생성
- 테스트 스캐폴딩
- 탐색적 시도

즉 “delegate the tasks, not the judgment”는 Addy의 표현이지만 Jonas 글의 논지와도 완전히 호응한다.

### 3-3. 공통 메시지: 병목은 생성이 아니라 검증이다
Jonas는 vibe coding의 실패를 통해 이를 보여주고,
Addy는 검증 인프라가 generation speed를 따라가지 못하는 상황을 직접 강조한다.

결국 멀티 에이전트 시대의 핵심 역량은
- 더 강한 모델 선택
- 더 멋진 프롬프트 문장
이 아니라,
- 검증 가능한 작업 단위 정의
- 테스트/린트/리뷰 자동화
- 잘못된 시도를 중단시키는 안전장치
- 문서 기반 장기 기억 축적
이다.

### 3-4. 공통 메시지: 문서가 하네스의 일부다
두 글 모두 암묵지를 싫어한다.
- Jonas: 보이지 않는 지식은 존재하지 않는 것과 같다.
- Addy: AGENTS.md, MODEL_ROUTING.md, tasks.json 같은 외부 문서가 세션 간 학습을 가능하게 한다.

즉 채팅창 안에만 있는 규칙은 운영 자산이 아니다. 저장소/볼트/리포 안에 읽을 수 있게 남아 있어야 한다.


## 4. 이 두 raw를 우리 위키 관점에서 어떻게 읽으면 좋나

### 4-1. Harness Engineering note의 배경과 실전 패턴이 동시에 보강된다
Jonas 글은 Harness Engineering 노트에 “왜 이 개념이 등장했는가”라는 역사적 배경을 준다.
Addy 글은 여기에 “실제로 어떤 운영 패턴이 하네스인가”를 채워 넣는다.

즉 Harness Engineering note를 읽을 때:
- Jonas = 패러다임 이동의 배경
- Addy = orchestration, quality gate, reviewer, AGENTS.md 같은 실천 패턴
으로 나눠 읽으면 좋다.

### 4-2. Agentic Workflow note는 단일 루프에서 팀 운영으로 확장된다
Agentic Workflow 를 단순히 “에이전트가 자료를 읽고 요약하고 연결하는 흐름”으로만 보면 약간 얇다.
이 두 글을 넣으면 다음이 추가된다.
- workflow는 이제 단일 agent loop가 아니라 multi-agent orchestration일 수 있다.
- workflow 설계의 핵심은 분해, 격리, 공유 상태, 검증 루프다.
- workflow는 결국 context management + harness design + human judgment allocation 문제다.

### 4-3. 우리한테 바로 적용 가능한 포인트
Hermes나 개인 위키 운영 관점에서 특히 바로 적용 가능한 것들:
- 큰 작업은 subagent 식으로 분해해서 독립/의존 관계를 먼저 설계하기
- 결과물은 항상 파일/노트/로그로 외부화하기
- “작업 완료” 전에 micro-check를 quality gate로 두기
- 반복 패턴은 skill 또는 AGENTS.md 성격의 문서로 누적하기
- 채팅으로만 규칙을 전달하지 말고 볼트 안 문서로 남기기
- output 생성 뒤 index / hub / log 업데이트를 습관화하기


## 5. 두 글의 차이를 한눈에 정리
| 항목 | Jonas Kim 글 | Addy Osmani 글 |
| --- | --- | --- |
| 질문 | 왜 업계가 prompt에서 harness로 이동했는가 | 멀티 에이전트 코딩을 실제로 어떻게 운영할 것인가 |
| 성격 | 역사 서사, 개념 지도 | 실무 운영 가이드, 패턴 카탈로그 |
| 핵심 메시지 | 엄밀함은 사라지지 않고 이동한다 | 생성보다 검증이 병목이다 |
| 주요 단위 | prompt, context, harness | subagent, team, reviewer, hook, worktree |
| 인간 역할 | 의도 명시, 환경 설계, 검증 | spec 작성, 분해, 승인, 리뷰 |
| 실무 가치 | 큰 그림 이해 | 바로 적용할 운영 패턴 획득 |

## 적용
이 두 글을 같이 읽으면 다음과 같은 실전 질문을 세울 수 있다.
- 지금 내가 고치려는 문제는 프롬프트 문제인가, 컨텍스트 문제인가, 하네스 문제인가?
- 단일 에이전트로 충분한가, 아니면 분업 구조가 필요한가?
- 품질 게이트가 없는 병렬화만 하고 있지는 않은가?
- 내가 팀/에이전트에게 주는 규칙은 채팅 속 암묵지인가, 아니면 문서화된 운영 자산인가?
- output과 wiki를 어떻게 연결해 다음 세션의 컨텍스트 품질을 높일 것인가?

## 다음 액션
- Harness Engineering 에 Jonas의 역사적 이동 구조와 Addy의 quality gate/orchestration 패턴을 더 구조적으로 흡수할 수 있다.
- Agentic Workflow 를 단일 agent 중심 정의에서 multi-agent orchestration 관점까지 확장해볼 수 있다.
- 필요하면 다음 단계로 “우리 Hermes 워크플로에 맞는 하네스/오케스트레이션 원칙”을 별도 output 또는 project note로 정리할 수 있다.

## 후속 질문
- 우리 작업에서 single-agent면 충분한 일과 multi-agent가 필요한 일을 어떻게 나눌까?
- AGENTS.md에 넣을 규칙과 skill로 빼둘 절차는 어떻게 구분할까?
- Hermes용 quality gate를 최소 세트로 정의하면 무엇이 들어가야 할까?
- Ralph loop 같은 패턴을 위키/리서치 작업에도 적용할 수 있을까?

## Related
- Jonas Kim - 프롬프트에서 하네스까지 — AI 에이전틱 패턴 4년의 기록 (Article, 2026-04-05)
- Addy Osmani - The Code Agent Orchestra - what makes multi-agent coding work (Article, 2026-03-26)
- Harness Engineering
- Agentic Workflow
- [[코딩 에이전트의 6가지 핵심 구성요소 상세 해설 (2026-04-06)]]
- [[코딩 에이전트는 모델보다 하네스가 중요하다 - Components of A Coding Agent 정리 (2026-04-06)]]
- 하네스 엔지니어링 리서치 (2026-04-04)
