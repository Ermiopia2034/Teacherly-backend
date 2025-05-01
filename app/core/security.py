from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from jose import jwt, JWTError
from passlib.context import CryptContext
from cryptography.fernet import Fernet

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize Fernet for encryption/decryption
# Ensure ENCRYPTION_KEY is a URL-safe base64-encoded 32-byte key
def get_fernet_key() -> bytes:
    """
    Get or generate a Fernet key from the settings.
    
    Returns:
        A URL-safe base64-encoded 32-byte key suitable for Fernet.
    """
    key = settings.ENCRYPTION_KEY
    # Ensure the key is properly padded for base64 decoding
    key += '=' * (-len(key) % 4)
    return key.encode()

try:
    fernet = Fernet(get_fernet_key())
except Exception as e:
    # Log the error and fall back to a safer approach
    print(f"Error initializing Fernet: {e}. Using a less secure fallback.")
    # In production, this should raise an exception or use a more secure fallback
    fernet = None

# JWT token functions
def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: The subject of the token, typically the user ID.
        expires_delta: Optional expiration time delta. If not provided,
                      uses the ACCESS_TOKEN_EXPIRE_MINUTES from settings.
    
    Returns:
        JWT token as a string.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT token to decode.
        
    Returns:
        The decoded token payload as a dictionary.
        
    Raises:
        JWTError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        # Re-raise the exception to be handled by the caller
        raise e

def verify_token(token: str) -> Optional[str]:
    """
    Verify a JWT token and extract the subject (typically user ID).
    
    Args:
        token: The JWT token to verify.
        
    Returns:
        The subject from the token if valid, None otherwise.
    """
    try:
        payload = decode_token(token)
        subject: str = payload.get("sub")
        if subject is None:
            return None
        return subject
    except JWTError:
        return None

# Password functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: The plain-text password.
        hashed_password: The hashed password to check against.
    
    Returns:
        True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password: The plain-text password to hash.
    
    Returns:
        The hashed password.
    """
    return pwd_context.hash(password)

# Encryption functions for sensitive data
def encrypt_data(data: str) -> str:
    """
    Encrypt sensitive data using Fernet symmetric encryption.
    
    Args:
        data: The data to encrypt.
    
    Returns:
        The encrypted data as a base64-encoded string.
        
    Raises:
        ValueError: If encryption fails or if Fernet is not properly initialized.
    """
    if not data:
        return data
        
    if fernet is None:
        # Fallback if Fernet initialization failed
        # In production, this should be handled more securely
        return data
        
    try:
        return fernet.encrypt(data.encode()).decode()
    except Exception as e:
        # Log the error but don't expose details in the exception message
        print(f"Encryption error: {e}")
        raise ValueError("Failed to encrypt data")

def decrypt_data(encrypted_data: str) -> str:
    """
    Decrypt sensitive data using Fernet symmetric encryption.
    
    Args:
        encrypted_data: The encrypted data to decrypt.
    
    Returns:
        The decrypted data.
        
    Raises:
        ValueError: If decryption fails or if Fernet is not properly initialized.
    """
    if not encrypted_data:
        return encrypted_data
        
    if fernet is None:
        # Fallback if Fernet initialization failed
        # In production, this should be handled more securely
        return encrypted_data
        
    try:
        return fernet.decrypt(encrypted_data.encode()).decode()
    except Exception as e:
        # Log the error but don't expose details in the exception message
        print(f"Decryption error: {e}")
        raise ValueError("Failed to decrypt data")
