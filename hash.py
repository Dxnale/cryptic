import re
import base64
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


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
    length: int
    charset: str
    regex: str
    prefix: str | None = None
    suffix: str | None = None
    confidence: float = 1.0
    description: str = ""


@dataclass
class HashAnalysis:
    """Resultado del análisis de hash

    Parametros
    -----------------
    possible_types: List[Tuple[HashType, float]]
        Lista de tipos posibles con su nivel de confianza
    raw_hash: str
        Hash original sin procesar tal como se recibió
    cleaned_hash: str
        Hash limpio sin espacios, prefijos o caracteres no válidos
    length: int
        Longitud del hash limpio en caracteres
    charset_analysis: Dict[str, bool]
        Análisis de conjuntos de caracteres (hex, base64, etc.)
    format_analysis: Dict[str, any]
        Análisis de formato (tiene prefijo, estructura, etc.)
    """

    possible_types: List[Tuple[HashType, float]]
    raw_hash: str
    cleaned_hash: str
    length: int
    charset_analysis: Dict[str, bool]
    format_analysis: Dict[str, any]


class HashIdentifier:
    """Identificador de algoritmos de hash usando técnicas heurísticas"""

    def __init__(self):
        self.patterns = self._initialize_patterns()

    def _initialize_patterns(self) -> List[HashPattern]:
        """Inicializa los patrones de identificación"""
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
                length=40,
                charset="0-9a-f",
                regex=r"^\*[a-f0-9]{40}$",
                prefix="*",
                description="MySQL5",
            ),
            HashPattern(
                hash_type=HashType.WORDPRESS,
                length=31,
                charset="a-zA-Z0-9./",
                regex=r"^\$P\$[a-zA-Z0-9./]{31}$",
                prefix="$P$",
                description="WordPress",
            ),
            HashPattern(
                hash_type=HashType.BCRYPT,
                length=60,
                charset="a-zA-Z0-9./",
                regex=r"^\$2[aby]?\$[0-9]{2}\$[a-zA-Z0-9./]{53}$",
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

    def _clean_hash(self, hash_string: str) -> str:
        return hash_string.strip().replace(" ", "").replace("\n", "").replace("\t", "")

    def _analyze_charset(self, hash_string: str) -> Dict[str, bool]:
        """Analiza el conjunto de caracteres usado en el hash"""
        analysis = {
            "hex_lowercase": bool(re.match(r"^[0-9a-f]+$", hash_string)),
            "hex_uppercase": bool(re.match(r"^[0-9A-F]+$", hash_string)),
            "hex_mixed": bool(re.match(r"^[0-9a-fA-F]+$", hash_string)),
            "base64": self._is_base64(hash_string),
            "alphanumeric": bool(re.match(r"^[a-zA-Z0-9]+$", hash_string)),
            "has_special_chars": bool(re.search(r"[^a-zA-Z0-9]", hash_string)),
            "has_dollar_signs": "$" in hash_string,
            "has_dots": "." in hash_string,
            "has_slashes": "/" in hash_string or "\\" in hash_string,
        }
        return analysis

    def _is_base64(self, s: str) -> bool:
        """Verifica si el string parece ser base64"""
        try:
            if len(s) % 4 == 0 and re.match(r"^[A-Za-z0-9+/]*={0,2}$", s):
                base64.b64decode(s)
                return True
        except Exception as _:
            pass
        return False

    def _analyze_format(self, hash_string: str) -> Dict[str, any]:
        """Analiza el formato del hash"""
        analysis = {
            "length": len(hash_string),
            "has_prefix": hash_string.startswith(("$", "*", "{", "0x")),
            "has_suffix": hash_string.endswith(("}", "=")),
            "segments": hash_string.split("$") if "$" in hash_string else [hash_string],
            "colon_separated": ":" in hash_string,
            "segments_count": len(hash_string.split("$")) if "$" in hash_string else 1,
        }

        # Analizar estructura de sal
        if "$" in hash_string and len(analysis["segments"]) >= 3:
            analysis["salt_structure"] = {
                "algorithm": analysis["segments"][1]
                if len(analysis["segments"]) > 1
                else None,
                "cost_factor": analysis["segments"][2]
                if len(analysis["segments"]) > 2
                else None,
                "salt": analysis["segments"][3]
                if len(analysis["segments"]) > 3
                else None,
                "hash": analysis["segments"][4]
                if len(analysis["segments"]) > 4
                else None,
            }

        return analysis

    def _calculate_confidence(
        self, pattern: HashPattern, hash_analysis: HashAnalysis
    ) -> float:
        """Calcula la confianza de que el hash coincida con el patrón"""
        confidence = pattern.confidence
        hash_string = hash_analysis.cleaned_hash

        # Verificar longitud exacta si se especifica
        if pattern.length and len(hash_string) != pattern.length:
            return 0.0

        # Verificar regex
        if not re.match(pattern.regex, hash_string, re.IGNORECASE):
            return 0.0

        # Verificar prefijo
        if pattern.prefix and not hash_string.startswith(pattern.prefix):
            return 0.0

        # Verificar sufijo
        if pattern.suffix and not hash_string.endswith(pattern.suffix):
            return 0.0

        # Ajustar confianza basado en caracter�sticas adicionales
        if pattern.hash_type == HashType.MYSQL5 and hash_string.startswith("*"):
            confidence = 0.95
        elif pattern.hash_type == HashType.BCRYPT and hash_string.startswith("$2"):
            confidence = 0.95
        elif pattern.hash_type == HashType.WORDPRESS and hash_string.startswith("$P$"):
            confidence = 0.95
        elif pattern.hash_type == HashType.ARGON2 and hash_string.startswith("$argon2"):
            confidence = 0.95

        # Penalizar hashes con longitudes comunes (como MD5/NTLM)
        if pattern.length == 32 and pattern.hash_type in [
            HashType.MD5,
            HashType.NTLM,
            HashType.LM,
        ]:
            if not hash_analysis.format_analysis.get("has_prefix", False):
                confidence *= 0.8  # Reducir confianza si no hay contexto adicional

        return confidence

    def identify(self, hash_string: str) -> HashAnalysis:
        """Identifica el tipo de hash usando técnicas heurísticas"""
        cleaned_hash = self._clean_hash(hash_string)
        charset_analysis = self._analyze_charset(cleaned_hash)
        format_analysis = self._analyze_format(cleaned_hash)

        possible_types = []

        for pattern in self.patterns:
            confidence = self._calculate_confidence(
                pattern,
                HashAnalysis(
                    [],
                    hash_string,
                    cleaned_hash,
                    len(cleaned_hash),
                    charset_analysis,
                    format_analysis,
                ),
            )

            if confidence > 0:
                possible_types.append((pattern.hash_type, confidence))

        # Ordenar por confianza (mayor a menor)
        possible_types.sort(key=lambda x: x[1], reverse=True)

        return HashAnalysis(
            possible_types=possible_types,
            raw_hash=hash_string,
            cleaned_hash=cleaned_hash,
            length=len(cleaned_hash),
            charset_analysis=charset_analysis,
            format_analysis=format_analysis,
        )

    def identify_best_match(self, hash_string: str) -> Tuple[HashType, float]:
        """Retorna la mejor coincidencia con su confianza"""
        analysis = self.identify(hash_string)
        if analysis.possible_types:
            return analysis.possible_types[0]
        return (HashType.UNKNOWN, 0.0)

    def print_analysis(self, hash_string: str, detailed: bool = False):
        """Imprime un análisis detallado del hash"""
        analysis = self.identify(hash_string)

        print(f"Hash Analysis for: {hash_string}")
        print("=" * 50)
        print(f"Cleaned Hash: {analysis.cleaned_hash}")
        print(f"Length: {analysis.length}")

        if detailed:
            print("\nCharset Analysis:")
            for key, value in analysis.charset_analysis.items():
                if value:
                    print(f"  \u2713 {key.replace('_', ' ').title()}")

            print("\nFormat Analysis:")
            for key, value in analysis.format_analysis.items():
                if isinstance(value, bool) and value:
                    print(f"  \u2713 {key.replace('_', ' ').title()}")
                elif not isinstance(value, bool) and value:
                    print(f"  \u2022 {key.replace('_', ' ').title()}: {value}")

        print("\nPossible Hash Types:")
        if analysis.possible_types:
            for hash_type, confidence in analysis.possible_types[:5]:  # Top 5
                print(f"  {hash_type.value:15} - Confidence: {confidence:.2%}")
        else:
            print("  No matches found")

        print()


# Funciones de utilidad
def quick_identify(hash_string: str) -> str:
    """Identificación rápida que retorna el tipo más probable"""
    identifier = HashIdentifier()
    hash_type, confidence = identifier.identify_best_match(hash_string)
    return f"{hash_type.value} ({confidence:.1%})"


def batch_identify(hash_list: List[str]) -> Dict[str, Tuple[HashType, float]]:
    """Identifica múltiples hashes en lote"""
    identifier = HashIdentifier()
    results = {}

    for hash_string in hash_list:
        results[hash_string] = identifier.identify_best_match(hash_string)

    return results


# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del identificador
    identifier = HashIdentifier()

    # Ejemplos de hashes para probar
    test_hashes = [
        "5d41402abc4b2a76b9719d911017c592",  # MD5
        "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",  # SHA-1
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # SHA-256
        "*A4B6157319038724E3560894F7F932C8886EBFCF",  # MySQL5
        "$2b$10$N9qo8uLOickgx2ZMRZoMye",  # bcrypt (parcial)
        "$P$B123456789abcdef123456789abcdef",  # WordPress (ejemplo)
        "09e8ce87a6dcf7c4",  # CRC32 ejemplo
    ]

    print("Hash Identifier - Pruebas")
    print("=" * 40)

    for test_hash in test_hashes:
        identifier.print_analysis(test_hash, detailed=False)
