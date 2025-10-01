"""
Identificador de algoritmos de hash usando técnicas heurísticas.

Este módulo contiene la lógica principal para identificar diferentes tipos
de hash basándose en patrones, longitudes, formatos y otras características.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Any

from cryptic.patterns.hash_patterns import HashType, HashPattern, get_hash_patterns
from cryptic.utils.formatters import clean_hash, analyze_charset, analyze_format


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
    format_analysis: Dict[str, Any]
        Análisis de formato (tiene prefijo, estructura, etc.)
    """

    possible_types: List[Tuple[HashType, float]]
    raw_hash: str
    cleaned_hash: str
    length: int
    charset_analysis: Dict[str, bool]
    format_analysis: Dict[str, Any]


class HashIdentifier:
    """Identificador de algoritmos de hash usando técnicas heurísticas"""

    def __init__(self) -> None:
        """Inicializa el identificador cargando los patrones de hash"""
        self.patterns = get_hash_patterns()

    def _calculate_confidence(self, pattern: HashPattern, hash_analysis: HashAnalysis) -> float:
        """
        Calcula el nivel de confianza para un patrón dado.
        
        Args:
            pattern: Patrón de hash a evaluar
            hash_analysis: Análisis del hash objetivo
            
        Returns:
            Nivel de confianza (0.0-1.0)
        """
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

        # Ajustar confianza basado en características adicionales
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
        """
        Identifica el tipo de hash y proporciona análisis detallado.
        
        Args:
            hash_string: Hash a identificar
            
        Returns:
            HashAnalysis con tipos posibles y análisis detallado
        """
        cleaned_hash = clean_hash(hash_string)
        charset_analysis = analyze_charset(cleaned_hash)
        format_analysis = analyze_format(cleaned_hash)

        possible_types = []

        # Evaluar cada patrón
        for pattern in self.patterns:
            confidence = self._calculate_confidence(
                pattern,
                HashAnalysis(
                    possible_types=[],
                    raw_hash=hash_string,
                    cleaned_hash=cleaned_hash,
                    length=len(cleaned_hash),
                    charset_analysis=charset_analysis,
                    format_analysis=format_analysis,
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
        """
        Retorna la mejor coincidencia con su confianza.
        
        Args:
            hash_string: Hash a identificar
            
        Returns:
            Tupla con (HashType, confianza)
        """
        analysis = self.identify(hash_string)
        if analysis.possible_types:
            return analysis.possible_types[0]
        return (HashType.UNKNOWN, 0.0)

    def print_analysis(self, hash_string: str, detailed: bool = False) -> None:
        """
        Imprime un análisis detallado del hash.
        
        Args:
            hash_string: Hash a analizar
            detailed: Si incluir análisis detallado de formato y charset
        """
        analysis = self.identify(hash_string)

        print(f"Hash Analysis for: {hash_string}")
        print("=" * 50)
        print(f"Cleaned Hash: {analysis.cleaned_hash}")
        print(f"Length: {analysis.length}")

        if detailed:
            print("\nCharset Analysis:")
            for key, value in analysis.charset_analysis.items():
                if value:
                    print(f"  ✓ {key.replace('_', ' ').title()}")

            print("\nFormat Analysis:")
            for key, value in analysis.format_analysis.items():
                if isinstance(value, bool) and value:
                    print(f"  ✓ {key.replace('_', ' ').title()}")
                elif not isinstance(value, bool) and value:
                    print(f"  • {key.replace('_', ' ').title()}: {value}")

        print("\nPossible Hash Types:")
        if analysis.possible_types:
            for hash_type, confidence in analysis.possible_types[:5]:  # Top 5
                print(f"  {hash_type.value:15} - Confidence: {confidence:.2%}")
        else:
            print("  No matches found")

        print()
