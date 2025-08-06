"""
Cryptic - Biblioteca de Python para detección, verificación y sugerencia de encriptación de datos sensibles.

Este paquete proporciona herramientas para:
- Identificar tipos de hash criptográficos
- Detectar datos sensibles que requieren protección
- Analizar y reportar el estado de protección de datos
- Sugerir mejores prácticas de seguridad

Ejemplo de uso básico:
    >>> from cryptic import HashIdentifier, CrypticAnalyzer
    >>> identifier = HashIdentifier()
    >>> analysis = identifier.identify("5d41402abc4b2a76b9719d911017c592")
    >>> print(f"{analysis.possible_types[0][0].value} ({analysis.possible_types[0][1]:.1%})")
    'MD5 (80.0%)'
    
    >>> analyzer = CrypticAnalyzer()
    >>> result = analyzer.analyze_data("some_sensitive_data")
    >>> analyzer.print_analysis(result)

Para más información, consulta la documentación completa.
"""

# Importar API pública
from cryptic.core.hash_identifier import HashIdentifier, HashType, HashAnalysis
from cryptic.core.analyzer import CrypticAnalyzer

# Metadatos del paquete
__version__ = "0.1.0"
__author__ = "Los Leones Team"
__description__ = "Biblioteca para detección y verificación de encriptación de datos sensibles"

# API pública - Solo clases principales
__all__ = [
    "HashIdentifier",
    "HashType", 
    "HashAnalysis",
    "CrypticAnalyzer",
]
