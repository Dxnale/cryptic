"""
Patrones de identificación para diferentes tipos de hash.

Este módulo contiene la definición de patrones utilizados para identificar
automáticamente diferentes tipos de algoritmos de hash basándose en
características como longitud, formato, prefijos y conjuntos de caracteres.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class HashType(Enum):
    """Enumeración de tipos de hash soportados"""

    MD5 = "MD5"
    SHA1 = "SHA-1"
    SHA224 = "SHA-224"
    SHA256 = "SHA-256"
    SHA384 = "SHA-384"
    SHA512 = "SHA-512"
    SHA3_224 = "SHA3-224"
    SHA3_256 = "SHA3-256"
    SHA3_384 = "SHA3-384"
    SHA3_512 = "SHA3-512"
    NTLM = "NTLM"
    LM = "LM"
    MYSQL = "MySQL"
    MYSQL5 = "MySQL5"
    WORDPRESS = "WordPress"
    BCRYPT = "bcrypt"
    SCRYPT = "scrypt"
    PBKDF2 = "PBKDF2"
    ARGON2 = "Argon2"
    CRC32 = "CRC32"
    ADLER32 = "Adler-32"
    WHIRLPOOL = "Whirlpool"
    RIPEMD160 = "RIPEMD-160"
    TIGER = "Tiger"
    GOST = "GOST"
    BLAKE2B = "BLAKE2b"
    BLAKE2S = "BLAKE2s"
    UNKNOWN = "Unknown"


@dataclass
class HashPattern:
    """Patrón de identificación de hash

    Parametros
    ----------
    hash_type: str
        Tipo de algoritmo de hash que representa este patrón
    length: int
        Longitud esperada del hash en caracteres (sin prefijos/sufijos)
    charset: str
        Conjunto de caracteres válidos (ej: "0-9a-f" para hexadecimal)
    regex: str
        Expresión regular para validar el formato del hash
    prefix: str | None
        Prefijo opcional que identifica el tipo (ej: "$2b$" para bcrypt)
    suffix: str | None
        Sufijo opcional que puede acompañar al hash
    confidence: float
        Nivel de confianza en la identificación (0.0-1.0)
    description: str
        Descripción legible del algoritmo y sus características
    """

    hash_type: HashType
    length: Optional[int]
    charset: str
    regex: str
    prefix: str | None = None
    suffix: str | None = None
    confidence: float = 1.0
    description: str = ""


def get_hash_patterns() -> List[HashPattern]:
    """Retorna la lista completa de patrones de hash configurados"""
    patterns = [
        HashPattern(
            hash_type=HashType.MD5,
            length=32,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{32}$",
            description="MD5 (128-bit)",
        ),
        HashPattern(
            hash_type=HashType.SHA1,
            length=40,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{40}$",
            description="SHA-1 (160-bit)",
        ),
        HashPattern(
            hash_type=HashType.SHA224,
            length=56,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{56}$",
            description="SHA-224 (224-bit)",
        ),
        HashPattern(
            hash_type=HashType.SHA256,
            length=64,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{64}$",
            description="SHA-256 (256-bit)",
        ),
        HashPattern(
            hash_type=HashType.SHA384,
            length=96,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{96}$",
            description="SHA-384 (384-bit)",
        ),
        HashPattern(
            hash_type=HashType.SHA512,
            length=128,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{128}$",
            description="SHA-512 (512-bit)",
        ),
        HashPattern(
            hash_type=HashType.NTLM,
            length=32,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{32}$",
            description="NTLM (Windows)",
            confidence=0.8,
        ),
        HashPattern(
            hash_type=HashType.LM,
            length=32,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{32}$",
            description="LM Hash (Windows legacy)",
            confidence=0.7,
        ),
        HashPattern(
            hash_type=HashType.MYSQL,
            length=16,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{16}$",
            description="MySQL (old format)",
        ),
        HashPattern(
            hash_type=HashType.MYSQL5,
            length=41,
            charset="0-9a-fA-F",
            regex=r"^\*[a-fA-F0-9]{40}$",
            prefix="*",
            description="MySQL5",
        ),
        HashPattern(
            hash_type=HashType.WORDPRESS,
            length=34,
            charset="a-zA-Z0-9./",
            regex=r"^\$P\$[a-zA-Z0-9./]{31,32}$",
            prefix="$P$",
            description="WordPress",
        ),
        HashPattern(
            hash_type=HashType.BCRYPT,
            length=None,
            charset="a-zA-Z0-9./",
            regex=r"^\$2[aby]?\$[0-9]{1,2}\$[a-zA-Z0-9./]{22,53}$",
            prefix="$2",
            description="bcrypt",
        ),
        HashPattern(
            hash_type=HashType.SCRYPT,
            length=None,
            charset="a-zA-Z0-9+/=",
            regex=r"^\$scrypt\$",
            prefix="$scrypt$",
            description="scrypt",
        ),
        HashPattern(
            hash_type=HashType.PBKDF2,
            length=None,
            charset="a-zA-Z0-9+/=$",
            regex=r"^\$pbkdf2",
            prefix="$pbkdf2",
            description="PBKDF2",
        ),
        HashPattern(
            hash_type=HashType.ARGON2,
            length=None,
            charset="a-zA-Z0-9+/=$",
            regex=r"^\$argon2[id]?\$",
            prefix="$argon2",
            description="Argon2",
        ),
        HashPattern(
            hash_type=HashType.CRC32,
            length=8,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{8}$",
            description="CRC32",
        ),
        HashPattern(
            hash_type=HashType.WHIRLPOOL,
            length=128,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{128}$",
            description="Whirlpool (512-bit)",
            confidence=0.9,
        ),
        HashPattern(
            hash_type=HashType.RIPEMD160,
            length=40,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{40}$",
            description="RIPEMD-160",
            confidence=0.8,
        ),
        HashPattern(
            hash_type=HashType.TIGER,
            length=48,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{48}$",
            description="Tiger (192-bit)",
        ),
        HashPattern(
            hash_type=HashType.BLAKE2B,
            length=128,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{128}$",
            description="BLAKE2b (512-bit)",
            confidence=0.8,
        ),
        HashPattern(
            hash_type=HashType.BLAKE2S,
            length=64,
            charset="0-9a-f",
            regex=r"^[a-f0-9]{64}$",
            description="BLAKE2s (256-bit)",
            confidence=0.8,
        ),
    ]

    return patterns
