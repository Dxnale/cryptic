"""
Detector de datos sensibles para el proyecto Cryptic.

Este módulo proporciona funcionalidades para detectar diferentes tipos de
información sensible utilizando patrones regex y validaciones específicas.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import re
import time

from cryptic.patterns.sensitive_patterns import (
    get_sensitive_patterns, 
    get_compiled_patterns,
    SensitivePattern,
    SensitiveDataType
)


@dataclass
class SensitiveMatch:
    """
    Representa una coincidencia de dato sensible encontrada.
    
    Attributes:
        data_type: Tipo de dato sensible detectado
        matched_text: Texto que coincidió con el patrón  
        start_pos: Posición inicial en el texto original
        end_pos: Posición final en el texto original
        confidence: Nivel de confianza en la detección (0.0-1.0)
        is_validated: Si pasó validación adicional (si aplica)
        pattern_used: Patrón que generó la coincidencia
    """
    data_type: SensitiveDataType
    matched_text: str
    start_pos: int
    end_pos: int
    confidence: float
    is_validated: bool
    pattern_used: SensitivePattern


@dataclass  
class SensitiveAnalysis:
    """
    Resultado del análisis de datos sensibles.
    
    Attributes:
        original_text: Texto original analizado
        matches: Lista de coincidencias encontradas
        highest_sensitivity: Mayor nivel de sensibilidad detectado
        total_matches: Número total de coincidencias
        analysis_time_ms: Tiempo de procesamiento en milisegundos
        recommendations: Recomendaciones de seguridad específicas
    """
    original_text: str
    matches: List[SensitiveMatch]
    highest_sensitivity: str
    total_matches: int
    analysis_time_ms: float
    recommendations: List[str]


class SensitiveDataDetector:
    """
    Detector principal de datos sensibles.
    
    Utiliza patrones regex y validaciones específicas para identificar
    información sensible como emails, RUTs, tarjetas de crédito, etc.
    """
    
    def __init__(self) -> None:
        """Inicializa el detector con los patrones configurados"""
        self.patterns = get_sensitive_patterns()
        self.compiled_patterns = get_compiled_patterns()
        self._sensitivity_hierarchy = {
            'CRITICAL': 4,
            'HIGH': 3, 
            'MEDIUM': 2,
            'LOW': 1,
            'NONE': 0
        }
    
    def detect(self, text: str) -> SensitiveAnalysis:
        """
        Detecta datos sensibles en un texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            SensitiveAnalysis con resultados de la detección
        """
        start_time = time.time()
        matches = []
        
        # Procesar cada patrón
        for pattern in self.patterns:
            pattern_matches = self._find_pattern_matches(text, pattern)
            matches.extend(pattern_matches)
        
        # Eliminar duplicados y solapamientos  
        matches = self._remove_overlapping_matches(matches)
        
        # Determinar mayor sensibilidad
        highest_sensitivity = self._get_highest_sensitivity(matches)
        
        # Generar recomendaciones
        recommendations = self._generate_recommendations(matches)
        
        analysis_time = (time.time() - start_time) * 1000  # Convertir a ms
        
        return SensitiveAnalysis(
            original_text=text,
            matches=matches,
            highest_sensitivity=highest_sensitivity,
            total_matches=len(matches),
            analysis_time_ms=analysis_time,
            recommendations=recommendations
        )
    
    def _find_pattern_matches(self, text: str, pattern: SensitivePattern) -> List[SensitiveMatch]:
        """
        Busca coincidencias de un patrón específico en el texto.
        
        Args:
            text: Texto donde buscar
            pattern: Patrón a buscar
            
        Returns:
            Lista de SensitiveMatch encontradas
        """
        matches = []
        # Para la mayoría de los patrones usamos búsqueda case-insensitive,
        # excepto para nombres de personas, donde la capitalización importa
        # para reducir falsos positivos.
        if pattern.data_type.name == "NOMBRE_PERSONA":
            compiled_regex = re.compile(pattern.regex)
        else:
            compiled_regex = re.compile(pattern.regex, re.IGNORECASE)
        
        for match in compiled_regex.finditer(text):
            matched_text = match.group()
            
            # Verificar si es un falso positivo conocido
            if self._is_false_positive(matched_text, pattern):
                continue
            
            # Aplicar validación específica si existe
            is_validated = True
            confidence = pattern.confidence
            
            if pattern.validation_func:
                is_validated = pattern.validation_func(matched_text)
                # Conservamos la confianza base aun si no valida; el flag
                # is_validated permitirá a los consumidores tomar decisiones.
            
            matches.append(SensitiveMatch(
                data_type=pattern.data_type,
                matched_text=matched_text,
                start_pos=match.start(),
                end_pos=match.end(), 
                confidence=confidence,
                is_validated=is_validated,
                pattern_used=pattern
            ))
        
        return matches
    
    def _is_false_positive(self, text: str, pattern: SensitivePattern) -> bool:
        """
        Verifica si un texto coincide con patrones de falsos positivos.
        
        Args:
            text: Texto a verificar
            pattern: Patrón que generó la coincidencia
            
        Returns:
            True si es probablemente un falso positivo
        """
        if not pattern.false_positive_patterns:
            return False
        
        for fp_pattern in pattern.false_positive_patterns:
            if re.match(fp_pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _remove_overlapping_matches(self, matches: List[SensitiveMatch]) -> List[SensitiveMatch]:
        """
        Elimina coincidencias solapadas, manteniendo la de mayor confianza.
        
        Args:
            matches: Lista de coincidencias a procesar
            
        Returns:
            Lista filtrada sin solapamientos
        """
        if not matches:
            return matches
        
        # Ordenar por posición y luego por confianza (descendente)
        sorted_matches = sorted(matches, key=lambda x: (x.start_pos, -x.confidence))
        
        filtered: List[SensitiveMatch] = []
        
        for match in sorted_matches:
            if not filtered:
                filtered.append(match)
                continue

            last = filtered[-1]
            overlaps = match.start_pos < last.end_pos

            if not overlaps:
                filtered.append(match)
                continue

            # Si se solapan y son de distinto tipo, conservamos ambas coincidencias
            if match.data_type != last.data_type:
                filtered.append(match)
                continue

            # Si se solapan y son del mismo tipo, conservar la de mayor confianza
            if match.confidence > last.confidence:
                filtered[-1] = match
        
        return filtered
    
    def _get_highest_sensitivity(self, matches: List[SensitiveMatch]) -> str:
        """
        Determina el mayor nivel de sensibilidad entre las coincidencias.
        
        Args:
            matches: Lista de coincidencias
            
        Returns:
            String con el nivel más alto de sensibilidad
        """
        if not matches:
            return 'NONE'
        
        max_level = 'NONE'
        max_value = 0
        
        for match in matches:
            level = match.pattern_used.sensitivity_level
            value = self._sensitivity_hierarchy.get(level, 0)
            if value > max_value:
                max_value = value
                max_level = level
        
        return max_level
    
    def _generate_recommendations(self, matches: List[SensitiveMatch]) -> List[str]:
        """
        Genera recomendaciones específicas basadas en los datos detectados.
        
        Args:
            matches: Lista de coincidencias encontradas
            
        Returns:
            Lista de recomendaciones de seguridad
        """
        recommendations = []
        
        if not matches:
            return ["No se detectaron datos sensibles específicos"]
        
        # Agrupar por tipo de dato
        by_type: Dict[SensitiveDataType, List[SensitiveMatch]] = {}
        for match in matches:
            data_type = match.data_type
            if data_type not in by_type:
                by_type[data_type] = []
            by_type[data_type].append(match)
        
        # Generar recomendaciones específicas por tipo
        for data_type, type_matches in by_type.items():
            count = len(type_matches)
            recommendations.extend(
                self._get_recommendations_for_type(data_type, count)
            )
        
        # Recomendaciones generales
        total_critical = sum(1 for m in matches if m.pattern_used.sensitivity_level == 'CRITICAL')
        total_high = sum(1 for m in matches if m.pattern_used.sensitivity_level == 'HIGH')
        
        if total_critical > 0:
            recommendations.insert(0, 
                f"⚠️  CRÍTICO: Se encontraron {total_critical} datos de sensibilidad crítica que requieren protección inmediata")
        
        if total_high > 0:
            recommendations.append(
                f"Se detectaron {total_high} datos de alta sensibilidad que deben ser protegidos")
        
        return recommendations
    
    def _get_recommendations_for_type(self, data_type: SensitiveDataType, count: int) -> List[str]:
        """
        Genera recomendaciones específicas para un tipo de dato.
        
        Args:
            data_type: Tipo de dato sensible
            count: Cantidad de coincidencias de este tipo
            
        Returns:
            Lista de recomendaciones específicas
        """
        recs = []
        
        if data_type == SensitiveDataType.EMAIL:
            recs.append(f"📧 {count} email(s) detectado(s): Use hash SHA-256 con salt para pseudonimización")
            recs.append("Considere cifrado simétrico si necesita recuperar el email original")
        
        elif data_type == SensitiveDataType.RUT_CHILENO:
            recs.append(f"🆔 {count} RUT(s) chileno(s) detectado(s): Use HMAC-SHA256 para pseudonimización reversible")
            recs.append("CRÍTICO: RUTs deben ser protegidos según Ley 19.628 de Protección de Datos")
        
        elif data_type == SensitiveDataType.CREDIT_CARD:
            recs.append(f"💳 {count} número(s) de tarjeta detectado(s): Use cifrado de preservación de formato (FPE)")
            recs.append("CRÍTICO: Cumplir con estándares PCI DSS para manejo de datos de tarjetas")
        
        elif data_type == SensitiveDataType.PHONE_CHILE or data_type == SensitiveDataType.PHONE_INTERNATIONAL:
            recs.append(f"📞 {count} teléfono(s) detectado(s): Use hash SHA-256 o cifrado AES-256")
            recs.append("Considere enmascaramiento parcial (ej: +56 9 ****1234)")
        
        elif data_type == SensitiveDataType.IP_ADDRESS:
            recs.append(f"🌐 {count} IP(s) detectada(s): Anonimice últimos octetos o use hash")
            recs.append("Para análisis, considere agregación por rangos de red")
        
        elif data_type == SensitiveDataType.NOMBRE_PERSONA:
            recs.append(f"👤 {count} posible(s) nombre(s) detectado(s): Use técnicas de pseudonimización")
            recs.append("Considere tokens únicos o iniciales + hash del nombre completo")
        
        elif data_type in [SensitiveDataType.DNI_ARGENTINO, SensitiveDataType.CI_URUGUAYO]:
            recs.append(f"🆔 {count} documento(s) de identidad detectado(s): Use hash criptográfico fuerte")
            recs.append("CRÍTICO: Documentos de identidad requieren máxima protección")
        
        elif data_type == SensitiveDataType.URL:
            recs.append(f"🔗 {count} URL(s) detectada(s): Revise si contienen información sensible en parámetros")
            recs.append("Considere limpiar o cifrar parámetros sensibles en URLs")
        
        return recs
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estadísticas sobre los patrones configurados.
        
        Returns:
            Diccionario con estadísticas del detector
        """
        pattern_stats = {}
        for pattern in self.patterns:
            level = pattern.sensitivity_level
            if level not in pattern_stats:
                pattern_stats[level] = 0
            pattern_stats[level] += 1
        
        return {
            'total_patterns': len(self.patterns),
            'patterns_by_sensitivity': pattern_stats,
            'supported_types': [p.data_type.value for p in self.patterns],
            'patterns_with_validation': sum(1 for p in self.patterns if p.validation_func is not None)
        }
