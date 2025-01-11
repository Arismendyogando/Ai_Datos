import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    API_PORT = 8000
    API_HOST = "0.0.0.0"
    DEBUG = True
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".pdf", ".txt", ".xls", ".xlsx"]
    
    @property
    def GOOGLE_CREDENTIALS_PATH(self):
        """Get and validate Google credentials path"""
        path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "/home/user/analizer/gcp_credentials.json")
            
        if not Path(path).exists():
            raise FileNotFoundError(f"Google credentials file not found at {path}")
            
        try:
            with open(path) as f:
                credentials = json.load(f)
                
                # Validate required fields
                required_fields = [
                    'type', 'project_id', 'private_key_id', 
                    'private_key', 'client_email', 'client_id'
                ]
                for field in required_fields:
                    if field not in credentials:
                        raise ValueError(f"Missing required field in credentials: {field}")
                    
                # Validate private key format
                if not credentials['private_key'].startswith('-----BEGIN PRIVATE KEY-----'):
                    raise ValueError("Invalid private key format")
                    
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in Google credentials file")
            
        return path

    @property
    def GOOGLE_SCOPES(self):
        """Return minimal required scopes"""
        return [
            "https://www.googleapis.com/auth/cloud-platform.read-only",
            "https://www.googleapis.com/auth/cloud-vision"
        ]

config = Config()
