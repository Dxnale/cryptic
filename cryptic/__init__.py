"""
Cryptic - Biblioteca de Python para detección, verificación y sugerencia de encriptación de datos sensibles.

Este paquete proporciona herramientas para:
- Identificar tipos de hash criptográficos
- Detectar datos sensibles que requieren protección
- Analizar y reportar el estado de protección de datos
- Sugerir mejores prácticas de seguridad

Ejemplo de uso básico:
    >>> from cryptic import identify_hash, quick_identify
    >>> result = identify_hash("5d41402abc4b2a76b9719d911017c592")
    >>> print(quick_identify("*A4B6157319038724E3560894F7F932C8886EBFCF"))
    'MySQL5 (95.0%)'

Para más información, consulta la documentación completa.
"""

# Importar API pública
from cryptic.core.hash_identifier import HashIdentifier, HashType, HashAnalysis
from cryptic.core.analyzer import CrypticAnalyzer

# Funciones de conveniencia para compatibilidad con hash.py
def identify_hash(hash_string: str):
    """Identifica un hash y retorna análisis completo"""
    identifier = HashIdentifier()
    return identifier.identify(hash_string)

def quick_identify(hash_string: str) -> str:
    """Identificación rápida que retorna el tipo más probable"""
    identifier = HashIdentifier()
    hash_type, confidence = identifier.identify_best_match(hash_string)
    return f"{hash_type.value} ({confidence:.1%})"

def batch_identify(hash_list):
    """Identifica múltiples hashes en lote"""
    identifier = HashIdentifier()
    results = {}
    for hash_string in hash_list:
        results[hash_string] = identifier.identify_best_match(hash_string)
    return results

# Metadatos del paquete
__version__ = "1.0.0"
__author__ = "Los Leones Team"
__description__ = "Biblioteca para detección y verificación de encriptación de datos sensibles"

# API pública
__all__ = [
    "HashIdentifier",
    "HashType", 
    "HashAnalysis",
    "CrypticAnalyzer",
    "identify_hash",
    "quick_identify",
    "batch_identify",
]
