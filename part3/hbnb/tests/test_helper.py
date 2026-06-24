#!/usr/bin/python3
import uuid

def unique_email(prefix="user"):
    return f"{prefix}.{uuid.uuid4().hex[:8]}@example.com"
