"""
crypto_core.py - Two-Factor Authentication Core Implementation

This module implements HOTP (RFC 4226) and TOTP (RFC 6238) algorithms
from scratch without external libraries like pyotp.

Implements:
- Base32 encoding/decoding (RFC 4648)
- HOTP - HMAC-based One-Time Password (RFC 4226)
- TOTP - Time-based One-Time Password (RFC 6238)

Author: News Portal Development Team
License: MIT
"""

import hmac
import hashlib
import time
import secrets
import struct
from typing import Optional, Tuple


# ============================================================================
# Base32 Encoding/Decoding (RFC 4648)
# ============================================================================

class Base32:
    """
    Base32 encoding/decoding implementation according to RFC 4648.
    """
    
    # Standard Base32 alphabet (RFC 4648)
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    
    @classmethod
    def encode(cls, data: bytes) -> str:
        """
        Encode bytes to Base32 string.
        
        Args:
            data: Binary data to encode
            
        Returns:
            Base32 encoded string
            
        Example:
            >>> Base32.encode(b'Hello')
            'JBSWY3DP'
        """
        if not data:
            return ""
        
        result = []
        bits = 0
        value = 0
        
        for byte in data:
            # Add byte to the value buffer
            value = (value << 8) | byte
            bits += 8
            
            # Extract 5-bit chunks
            while bits >= 5:
                bits -= 5
                index = (value >> bits) & 0x1F
                result.append(cls.ALPHABET[index])
        
        # Handle remaining bits
        if bits > 0:
            index = (value << (5 - bits)) & 0x1F
            result.append(cls.ALPHABET[index])
        
        # Add padding
        while len(result) % 8 != 0:
            result.append('=')
        
        return ''.join(result)
    
    @classmethod
    def decode(cls, encoded: str) -> bytes:
        """
        Decode Base32 string to bytes.
        
        Args:
            encoded: Base32 encoded string
            
        Returns:
            Decoded binary data
            
        Raises:
            ValueError: If input contains invalid Base32 characters
            
        Example:
            >>> Base32.decode('JBSWY3DP')
            b'Hello'
        """
        if not encoded:
            return b""
        
        # Remove padding and convert to uppercase
        encoded = encoded.rstrip('=').upper()
        
        # Create reverse mapping
        decode_map = {char: idx for idx, char in enumerate(cls.ALPHABET)}
        
        result = []
        bits = 0
        value = 0
        
        for char in encoded:
            if char not in decode_map:
                raise ValueError(f"Invalid Base32 character: {char}")
            
            # Add 5 bits to the value buffer
            value = (value << 5) | decode_map[char]
            bits += 5
            
            # Extract 8-bit chunks
            if bits >= 8:
                bits -= 8
                result.append((value >> bits) & 0xFF)
        
        return bytes(result)


# ============================================================================
# HOTP - HMAC-based One-Time Password (RFC 4226)
# ============================================================================

class HOTP:
    """
    HOTP (HMAC-based One-Time Password) implementation according to RFC 4226.
    
    HOTP generates one-time passwords based on:
    - A shared secret key
    - A moving counter value
    """
    
    @staticmethod
    def generate(secret: bytes, counter: int, digits: int = 6) -> str:
        """
        Generate HOTP code.
        
        Args:
            secret: Shared secret key (bytes)
            counter: Moving counter value (integer)
            digits: Number of digits in OTP (default: 6)
            
        Returns:
            HOTP code as string (zero-padded to specified digits)
            
        Example:
            >>> secret = b'12345678901234567890'
            >>> HOTP.generate(secret, 0)
            '755224'
        """
        # Step 1: Generate HMAC-SHA-1 hash
        # Convert counter to 8-byte big-endian
        counter_bytes = struct.pack('>Q', counter)
        
        # Calculate HMAC-SHA-1
        hmac_hash = hmac.new(secret, counter_bytes, hashlib.sha1).digest()
        
        # Step 2: Dynamic Truncation
        otp = HOTP._dynamic_truncate(hmac_hash)
        
        # Step 3: Compute OTP value
        otp_value = otp % (10 ** digits)
        
        # Step 4: Return as zero-padded string
        return str(otp_value).zfill(digits)
    
    @staticmethod
    def _dynamic_truncate(hmac_hash: bytes) -> int:
        """
        Perform Dynamic Truncation as per RFC 4226 Section 5.3.
        
        The Dynamic Truncation extracts a 4-byte dynamic binary code
        from the 20-byte HMAC-SHA-1 result.
        
        Args:
            hmac_hash: 20-byte HMAC-SHA-1 hash
            
        Returns:
            31-bit integer value
        """
        # Get offset from the last nibble (4 bits) of the hash
        offset = hmac_hash[-1] & 0x0F
        
        # Extract 4 bytes starting at offset
        code = struct.unpack('>I', hmac_hash[offset:offset + 4])[0]
        
        # Mask the most significant bit (to get 31-bit number)
        code &= 0x7FFFFFFF
        
        return code
    
    @staticmethod
    def verify(secret: bytes, otp: str, counter: int, window: int = 1) -> bool:
        """
        Verify HOTP code with look-ahead window.
        
        Args:
            secret: Shared secret key
            otp: OTP code to verify
            counter: Current counter value
            window: Look-ahead window size (default: 1)
            
        Returns:
            True if OTP is valid, False otherwise
        """
        for i in range(window + 1):
            if HOTP.generate(secret, counter + i, len(otp)) == otp:
                return True
        return False


# ============================================================================
# TOTP - Time-based One-Time Password (RFC 6238)
# ============================================================================

class TOTP:
    """
    TOTP (Time-based One-Time Password) implementation according to RFC 6238.
    
    TOTP generates one-time passwords based on:
    - A shared secret key
    - Current time (divided into time steps)
    """
    
    DEFAULT_PERIOD = 30  # 30 seconds time step
    
    @staticmethod
    def generate(secret: bytes, digits: int = 6, period: int = DEFAULT_PERIOD,
                 timestamp: Optional[int] = None) -> str:
        """
        Generate TOTP code.
        
        Args:
            secret: Shared secret key (bytes)
            digits: Number of digits in OTP (default: 6)
            period: Time step in seconds (default: 30)
            timestamp: Unix timestamp (default: current time)
            
        Returns:
            TOTP code as string
            
        Example:
            >>> secret = b'12345678901234567890'
            >>> TOTP.generate(secret)
            '287082'  # Will vary based on current time
        """
        # Get current timestamp if not provided
        if timestamp is None:
            timestamp = int(time.time())
        
        # Calculate time step counter (T = (Current Unix time - T0) / X)
        # T0 = 0 (Unix epoch), X = period (default 30 seconds)
        counter = timestamp // period
        
        # Use HOTP with time-based counter
        return HOTP.generate(secret, counter, digits)
    
    @staticmethod
    def verify(secret: bytes, otp: str, period: int = DEFAULT_PERIOD,
               window: int = 1, timestamp: Optional[int] = None) -> bool:
        """
        Verify TOTP code with time window.
        
        Args:
            secret: Shared secret key
            otp: OTP code to verify
            period: Time step in seconds (default: 30)
            window: Number of time steps to check before/after current time
            timestamp: Unix timestamp (default: current time)
            
        Returns:
            True if OTP is valid, False otherwise
            
        Note:
            A window of 1 allows codes from previous and next time step,
            providing tolerance for clock skew.
        """
        if timestamp is None:
            timestamp = int(time.time())
        
        counter = timestamp // period
        
        # Check current time step and surrounding window
        for i in range(-window, window + 1):
            if HOTP.generate(secret, counter + i, len(otp)) == otp:
                return True
        
        return False
    
    @staticmethod
    def get_provisioning_uri(secret: bytes, account_name: str, 
                            issuer: str = "News Portal",
                            digits: int = 6, period: int = DEFAULT_PERIOD) -> str:
        """
        Generate provisioning URI for QR code.
        
        Format: otpauth://totp/ISSUER:ACCOUNT?secret=SECRET&issuer=ISSUER
        
        Args:
            secret: Shared secret key
            account_name: User's account identifier (email/username)
            issuer: Service name
            digits: Number of digits (default: 6)
            period: Time period (default: 30)
            
        Returns:
            otpauth:// URI string
            
        Example:
            >>> secret = b'12345678901234567890'
            >>> TOTP.get_provisioning_uri(secret, 'user@example.com')
            'otpauth://totp/News%20Portal:user@example.com?secret=...'
        """
        from urllib.parse import quote
        
        # Encode secret to Base32
        secret_b32 = Base32.encode(secret).rstrip('=')  # Remove padding
        
        # Build URI - encode issuer and account separately, keep : unencoded
        label = f"{quote(issuer, safe='')}:{quote(account_name, safe='')}"
        params = f"secret={secret_b32}&issuer={quote(issuer, safe='')}&digits={digits}&period={period}"
        
        return f"otpauth://totp/{label}?{params}"


# ============================================================================
# Utility Functions
# ============================================================================

class TwoFactorUtils:
    """
    Utility functions for Two-Factor Authentication.
    """
    
    @staticmethod
    def generate_secret(length: int = 20) -> bytes:
        """
        Generate cryptographically secure random secret.
        
        Args:
            length: Length of secret in bytes (default: 20)
            
        Returns:
            Random secret bytes
        """
        return secrets.token_bytes(length)
    
    @staticmethod
    def generate_secret_base32(length: int = 20) -> str:
        """
        Generate secret and return as Base32 string.
        
        Args:
            length: Length of secret in bytes (default: 20)
            
        Returns:
            Base32 encoded secret
        """
        secret = TwoFactorUtils.generate_secret(length)
        return Base32.encode(secret)
    
    @staticmethod
    def generate_backup_codes(count: int = 10, length: int = 8) -> list:
        """
        Generate backup recovery codes.
        
        Args:
            count: Number of backup codes to generate
            length: Length of each code (default: 8)
            
        Returns:
            List of backup codes (format: XXXX-XXXX)
        """
        codes = []
        for _ in range(count):
            # Generate random hex string
            code = secrets.token_hex(length // 2).upper()
            # Format as XXXX-XXXX
            formatted = f"{code[:4]}-{code[4:8]}"
            codes.append(formatted)
        return codes


# ============================================================================
# Testing & Validation
# ============================================================================

def _run_tests():
    """
    Run basic tests to validate implementation.
    """
    print("=" * 70)
    print("CRYPTO_CORE - Two-Factor Authentication Implementation Tests")
    print("=" * 70)
    
    # Test 1: Base32 Encoding/Decoding
    print("\n[TEST 1] Base32 Encoding/Decoding")
    test_data = b"Hello World!"
    encoded = Base32.encode(test_data)
    decoded = Base32.decode(encoded)
    print(f"  Original: {test_data}")
    print(f"  Encoded:  {encoded}")
    print(f"  Decoded:  {decoded}")
    print(f"  [PASS]" if test_data == decoded else "  [FAIL]")
    
    # Test 2: HOTP (RFC 4226 Test Vectors)
    print("\n[TEST 2] HOTP (RFC 4226 Test Vectors)")
    secret = b"12345678901234567890"
    expected_codes = ["755224", "287082", "359152", "969429", "338314"]
    
    for counter, expected in enumerate(expected_codes):
        code = HOTP.generate(secret, counter)
        status = "[OK]" if code == expected else "[FAIL]"
        print(f"  Counter {counter}: {code} (expected: {expected}) {status}")
    
    # Test 3: TOTP
    print("\n[TEST 3] TOTP")
    secret = TwoFactorUtils.generate_secret()
    secret_b32 = Base32.encode(secret)
    print(f"  Secret (Base32): {secret_b32}")
    
    # Generate codes for current time
    current_code = TOTP.generate(secret)
    print(f"  Current TOTP: {current_code}")
    
    # Verify the code
    is_valid = TOTP.verify(secret, current_code)
    print(f"  Verification: {'[PASS]' if is_valid else '[FAIL]'}")
    
    # Test 4: Provisioning URI
    print("\n[TEST 4] Provisioning URI")
    uri = TOTP.get_provisioning_uri(secret, "user@example.com", "Test Service")
    print(f"  URI: {uri[:80]}...")
    
    # Test 5: Backup Codes
    print("\n[TEST 5] Backup Codes Generation")
    backup_codes = TwoFactorUtils.generate_backup_codes(5)
    print(f"  Generated {len(backup_codes)} backup codes:")
    for i, code in enumerate(backup_codes, 1):
        print(f"    {i}. {code}")
    
    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    # Run tests when executed directly
    _run_tests()
