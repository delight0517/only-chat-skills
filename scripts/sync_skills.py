#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OmniChat / Only Chat GitHub Skill Sync Tool
Syncs skills from delight0517/omnichat-skills directly into local OmniChat skill engines.
"""

import os
import sys
import json
import urllib.request
import zipfile
import io
import shutil
from pathlib import Path

DEFAULT_REPO = "delight0517/omnichat-skills"
TARGET_DIRS = [
    Path.home() / ".my-codex" / "skills",
    Path.home() / ".gemini" / "config" / "skills",
]

def fetch_and_install_skills(repo=DEFAULT_REPO):
    print(f"[*] Connecting to GitHub repository: {repo}...")
    api_url = f"https://api.github.com/repos/{repo}/zipball/main"
    req = urllib.request.Request(api_url, headers={"User-Agent": "OmniChat-SkillSync/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
    except Exception as e:
        print(f"[-] Failed to fetch repository from GitHub: {e}")
        return False

    print("[*] Unpacking skills archive...")
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        # Find root folder in zip
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

    print("[*] All skills loaded into OmniChat successfully!")
    return True

if __name__ == "__main__":
    repo_arg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_REPO
    fetch_and_install_skills(repo_arg)
