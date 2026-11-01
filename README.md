# OmniChat Skills Hub (오픈소스 스킬 레포지토리)

OmniChat / Only Chat 데스크톱 클라이언트 및 AI 에이전트가 깃허브에서 직접 스킬(Skill)을 탐색, 다운로드, 핫 리로드(Hot-reload)할 수 있는 오픈소스 스킬 레지스트리입니다.

---

## 📦 포함된 핵심 스킬 (Included Skills)

### 1. `windows-firewall-silencer`
- **역할**: 대화 도중 "제발 이것 좀 그만 뜨게 해줘", "방화벽 팝업 꺼줘" 요청을 인식하여 Windows Defender 방화벽의 불필요한 네트워크 허용 알림 창을 완전히 박멸합니다.
- **해결 원리**:
  - 패키지 재빌드(v50, v51, v53 등)로 인한 경로 변경 시 발생하는 팝업 원천 차단
  - 실수로 생성된 `Block`(차단) 규칙 자동 정리
  - `InboundUserNotification` 시스템 전역 `Disable` 설정 및 QA 통신 포트 영구 개방
- **단축키**: `$windows-firewall-silencer`

---

## 🚀 OmniChat 깃허브 동기화 연동 방법

OmniChat 클라이언트는 다음 설정을 통해 본 레포지토리 또는 개인 깃허브 레포지토리에서 스킬을 자동으로 동기화합니다:

### 1. CLI 동기화 도구 사용
```bash
python scripts/sync_skills.py --repo delight0517/omnichat-skills
```

### 2. 로컬 스킬 폴더 자동 로드
다운로드된 스킬은 사용자 계정의 글로벌 스킬 디렉터리에 자동으로 적재되어 실시간 반영됩니다:
- Windows: `%USERPROFILE%\.my-codex\skills\` 또는 `%USERPROFILE%\.gemini\config\skills\`
- macOS: `~/.my-codex/skills/`

---

## 📜 라이선스
MIT License (Rogan Kim / GeunHu Kim & AI Architect)
