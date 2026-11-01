# Only Chat Skills Hub (공식 오픈소스 스킬 레포지토리)

**Only Chat** (`delight0517/only-chat`) 데스크톱 워크스페이스 클라이언트와 AI 에이전트가 GitHub에서 직접 스킬(Skill)을 탐색, 다운로드, 핫 리로드(Hot-reload)할 수 있는 오픈소스 스킬 레지스트리입니다.

---

## 📦 포함된 핵심 스킬 (Included Skills)

### 1. `windows-firewall-silencer`
- **역할**: Only Chat과 대화 도중 "제발 이것 좀 그만 뜨게 해줘", "방화벽 팝업 꺼줘" 요청을 즉시 인식하여 Windows Defender 방화벽의 불필요한 네트워크 허용 알림 창을 완전히 박멸합니다.
- **해결 원리**:
  - 패키지 재빌드(v50, v51, v53 등)로 인한 경로 변경 시 발생하는 팝업 원천 차단
  - 실수로 생성된 `Block`(차단) 규칙 자동 정리
  - `InboundUserNotification` 시스템 전역 `Disable` 설정 및 QA 통신 포트 영구 개방
- **단축키**: `$windows-firewall-silencer`

---

## 🚀 Only Chat ↔ 깃허브 연동 동기화 방법

Only Chat 클라이언트는 사용자 계정의 글로벌 스킬 디렉터리(`%USERPROFILE%\.my-codex\skills`)를 감시하여 스킬 변경을 **무중단 핫 리로드**합니다.

### 1. CLI 동기화 도구 사용
```bash
python scripts/sync_skills.py --repo delight0517/only-chat-skills
```

### 2. 자동 반영 경로
동기화된 스킬은 즉시 Only Chat의 `SkillManager`에 실시간 로드됩니다:
- Windows: `%USERPROFILE%\.my-codex\skills\`
- macOS: `~/.my-codex/skills/`

---

## 📜 라이선스
MIT License (Rogan Kim / GeunHu Kim & AI Architect)
