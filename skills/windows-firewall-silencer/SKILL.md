---
name: windows-firewall-silencer
description: >-
  Detects and permanently silences annoying Windows Security & Windows Defender Firewall prompt popups
  ("Do you want to allow public and private networks to access this app?", "Windows Firewall has blocked some features of...").
  Automatically identifies when repeated builds (e.g. Unreal Engine Pixel Streaming, Python servers, Node daemons)
  trigger security prompts, deletes conflicting Block rules, grants firewall exemptions, or silences InboundUserNotification
  system-wide so user workflows are never interrupted.
triggers:
  - "그만 뜨게 해줘"
  - "방화벽 팝업 꺼줘"
  - "이것 좀 그만 뜨게"
  - "방화벽 허용해줘"
  - "windows security 팝업"
  - "방화벽 알림 끄기"
  - "unrealgame 방화벽"
  - "네트워크 허용 팝업"
---

# Windows Firewall Silencer ($windows-firewall-silencer)

Detects and permanently eliminates repetitive **Windows Security / Windows Defender Firewall network access dialogs** ("Do you want to allow public and private networks to access this app?").

When the user says:
- *"제발 이것 좀 그만 뜨게 해줄래?"*
- *"방화벽 팝업 계속 뜨는데 영구 허용해줘"*
- *"네트워크 허용 창 안 뜨게 해줘"*

The agent MUST activate this skill immediately to diagnose and permanently resolve the root cause.

---

## 1. Root Cause Diagnosis & Workflow

When an app or build keeps popping up the Windows Firewall dialog:

1. **Changing Build Paths**: 
   When AI agents or build pipelines rebuild apps with changing version paths (e.g. `package-v50`, `package-v51`, `package-v53`), Windows treats each binary path as an entirely new application and pops up the firewall prompt every time.
2. **Ghost "Block" Rules**:
   If the user accidentally hit *Cancel* or closed the window previously, Windows permanently adds a `Block` rule. Any subsequent run triggers notifications or outright network failure.
3. **Repeated Inbound User Notifications**:
   Windows Firewall default configuration prompts the user whenever an unknown executable binds to a listening port.

---

## 2. Fast Resolution Actions

### Strategy A: Silence All Inbound User Notification Prompts (Permanent Fix)
To prevent ANY repetitive popup whenever builds change versions or ports:
```cmd
netsh advfirewall set allprofiles settings inboundusernotification disable
```
*Note: This keeps Windows Firewall protection completely intact while turning off the nagging user prompt.*

### Strategy B: Remove Ghost Block Rules & Allow Port Ranges
If a development workflow requires listening ports (e.g., Pixel Streaming, Node, Vite, Flask, Unreal QA):
```cmd
:: 1. Delete conflicting block rules
netsh advfirewall firewall delete rule name="<AppName>.exe"

:: 2. Allow port ranges directly
netsh advfirewall firewall add rule name="Dev_QA_Ports_TCP" dir=in action=allow protocol=TCP localport=80,3000,5173,8080,8555,8888,7777 profile=any
netsh advfirewall firewall add rule name="Dev_QA_Ports_UDP" dir=in action=allow protocol=UDP localport=8555,8888,7777 profile=any
```

### Strategy C: UAC-Elevated One-Click Native Runner
When running from an un-elevated agent shell, generate a self-elevating native launcher that triggers a single clean UAC prompt:
```bat
@echo off
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B
)
if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )

netsh advfirewall set allprofiles settings inboundusernotification disable
echo [Done] Windows Firewall popup notifications permanently silenced!
timeout /t 3
exit
```

---

## 3. Verification Command
Always verify that the notification state is successfully set to `Disable`:
```cmd
netsh advfirewall show allprofiles | findstr /i "InboundUserNotification"
```
Expected output:
```
InboundUserNotification               Disable
InboundUserNotification               Disable
InboundUserNotification               Disable
```
