#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Only Chat GitHub Skill Sync Tool
Syncs skills from delight0517/only-chat-skills directly into Only Chat's SkillManager.
"""

import os
import sys
import subprocess
import zipfile
import io
import shutil
import urllib.request
from pathlib import Path

DEFAULT_REPO = "delight0517/only-chat-skills"
TARGET_DIRS = [
    Path.home() / ".my-codex" / "skills",
    Path.home() / ".gemini" / "config" / "skills",
]

def fetch_zip_bytes(repo):
    # Strategy 1: Public archive URL
    url = f"https://codeload.github.com/{repo}/zip/refs/heads/main"
    headers = {"User-Agent": "OnlyChat-SkillSync/1.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read()
    except Exception as e:
        print(f"[*] Direct download fallback: {e}")

    # Strategy 2: gh CLI
    try:
        res = subprocess.run(["gh", "api", f"repos/{repo}/zipball/main"], capture_output=True, check=True)
        return res.stdout
    except Exception as e:
        print(f"[-] gh api download failed: {e}")
        return None

def fetch_and_install_skills(repo=DEFAULT_REPO):
    print(f"[*] Connecting to GitHub repository: {repo}...")
    zip_data = fetch_zip_bytes(repo)
    if not zip_data:
        print("[-] Unable to fetch skills package from GitHub.")
        return False

    print("[*] Unpacking skills archive into Only Chat skill registry...")
    with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
        root_dir = z.namelist()[0].split('/')[0]
        skill_prefix = f"{root_dir}/skills/"
        
        extracted_skills = set()
        for item in z.namelist():
            if item.startswith(skill_prefix) and not item.endswith('/'):
                rel_path = item[len(skill_prefix):]
                skill_name = rel_path.split('/')[0]
                extracted_skills.add(skill_name)

        print(f"[+] Found {len(extracted_skills)} skills: {', '.join(extracted_skills)}")

        for target_dir in TARGET_DIRS:
            target_dir.mkdir(parents=True, exist_ok=True)
            for item in z.namelist():
                if item.startswith(skill_prefix) and not item.endswith('/'):
                    rel_path = item[len(skill_prefix):]
                    out_path = target_dir / rel_path
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(item) as src, open(out_path, "wb") as dst:
                        shutil.copyfileobj(src, dst)
            print(f"[+] Synced skills to: {target_dir}")

    print("[*] All skills loaded into Only Chat successfully!")
    return True

if __name__ == "__main__":
    repo_arg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_REPO
    fetch_and_install_skills(repo_arg)
