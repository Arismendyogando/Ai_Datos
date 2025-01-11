#!/usr/bin/env python3
"""
GCP Credentials Rotation Script

This script automates the rotation of GCP service account credentials
and updates the environment configuration.

Usage:
    python3 rotate_gcp_credentials.py --project-id PROJECT_ID --service-account SERVICE_ACCOUNT_EMAIL
"""

import os
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

def rotate_credentials(project_id: str, service_account: str) -> dict:
    """Generate new GCP service account credentials"""
    key_name = f"{service_account}-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    key_path = Path("config") / "gcp_credentials" / key_name
    
    # Create directory if it doesn't exist
    key_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create new key using gcloud CLI
    create_cmd = [
        "gcloud", "iam", "service-accounts", "keys", "create",
        str(key_path),
        "--iam-account", service_account,
        "--project", project_id
    ]
    
    try:
        subprocess.run(create_cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create new credentials: {e}")

    # Load and validate new credentials
    with open(key_path, 'r') as f:
        credentials = json.load(f)
    
    return credentials, key_path

def update_env_file(key_path: Path):
    """Update .env file with new credentials path"""
    env_file = Path(".env")
    env_lines = []
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_lines = f.readlines()
    
    # Update or add GOOGLE_APPLICATION_CREDENTIALS
    new_line = f"GOOGLE_APPLICATION_CREDENTIALS={key_path}\n"
    updated = False
    
    for i, line in enumerate(env_lines):
        if line.startswith("GOOGLE_APPLICATION_CREDENTIALS="):
            env_lines[i] = new_line
            updated = True
            break
    
    if not updated:
        env_lines.append(new_line)
    
    with open(env_file, 'w') as f:
        f.writelines(env_lines)

def main():
    parser = argparse.ArgumentParser(description="Rotate GCP service account credentials")
    parser.add_argument("--project-id", required=True, help="GCP project ID")
    parser.add_argument("--service-account", required=True, help="Service account email")
    
    args = parser.parse_args()
    
    try:
        print("Rotating GCP credentials...")
        credentials, key_path = rotate_credentials(args.project_id, args.service_account)
        update_env_file(key_path)
        
        print(f"""
Successfully rotated credentials:
- New key created at: {key_path}
- Environment variables updated in .env
- Old keys should be deleted manually after verification
""")
        
    except Exception as e:
        print(f"Error rotating credentials: {e}")
        exit(1)

if __name__ == "__main__":
    main()
