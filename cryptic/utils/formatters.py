"""
Utilidades para formateo, limpieza y análisis de datos.

Este módulo contiene funciones auxiliares para procesar y analizar
cadenas de texto, detectar conjuntos de caracteres, y realizar
operaciones de limpieza de datos.
"""

import re
import base64
from typing import Dict


def clean_hash(hash_string: str) -> str:
    """
    Limpia un hash removiendo espacios, tabs y saltos de línea.
    
    Args:
        hash_string: La cadena de hash a limpiar
        
    Returns:
        Hash limpio sin espacios en blanco
    """
    return hash_string.strip().replace(" ", "").replace("\n", "").replace("\t", "")


def is_base64(s: str) -> bool:
    """
    Verifica si el string es base64 válido.
    
    Args:
        s: Cadena a verificar
        
    Returns:
        True si es base64 válido, False en caso contrario
    """
    try:
        if len(s) % 4 == 0 and re.match(r"^[A-Za-z0-9+/]*={0,2}$", s):
            base64.b64decode(s)
            return True
    except Exception:
        pass
    return False


def analyze_charset(hash_string: str) -> Dict[str, bool]:
    """
    Analiza el conjunto de caracteres usado en el hash.
    
    Args:
        hash_string: Cadena a analizar
        
    Returns:
        Diccionario con análisis de conjuntos de caracteres
    """
    analysis = {
        "hex_lowercase": bool(re.match(r"^[0-9a-f]+$", hash_string)),
        "hex_uppercase": bool(re.match(r"^[0-9A-F]+$", hash_string)),
        "hex_mixed": bool(re.match(r"^[0-9a-fA-F]+$", hash_string)),
        "base64": is_base64(hash_string),
        "alphanumeric": bool(re.match(r"^[a-zA-Z0-9]+$", hash_string)),
        "has_special_chars": bool(re.search(r"[^a-zA-Z0-9]", hash_string)),
        "has_dollar_signs": "$" in hash_string,
        "has_dots": "." in hash_string,
        "has_slashes": "/" in hash_string or "\\" in hash_string,
    }
    return analysis


def analyze_format(hash_string: str) -> Dict[str, any]:
    """
    Analiza el formato y estructura del hash.
    
    Args:
        hash_string: Cadena a analizar
        
    Returns:
        Diccionario con análisis de formato
    """
    analysis = {
        "length": len(hash_string),
        "has_prefix": hash_string.startswith(("$", "*", "{", "0x")),
        "has_suffix": hash_string.endswith(("}", "=")),
        "segments": hash_string.split("$") if "$" in hash_string else [hash_string],
        "colon_separated": ":" in hash_string,
        "segments_count": len(hash_string.split("$")) if "$" in hash_string else 1,
    }

    # Analizar estructura de sal para hashes con formato $algo$cost$salt$hash
    if "$" in hash_string and len(analysis["segments"]) >= 3:
        analysis["salt_structure"] = {
            "algorithm": analysis["segments"][1] if len(analysis["segments"]) > 1 else None,
            "cost_factor": analysis["segments"][2] if len(analysis["segments"]) > 2 else None,
            "salt": analysis["segments"][3] if len(analysis["segments"]) > 3 else None,
            "hash": analysis["segments"][4] if len(analysis["segments"]) > 4 else None,
        }

    return analysis
