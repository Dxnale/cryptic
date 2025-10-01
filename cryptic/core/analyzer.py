"""
Analizador principal de Cryptic para detección y verificación de datos sensibles.

Este módulo proporciona la interfaz principal para analizar datos,
identificar información sensible y verificar su estado de protección.
"""

from typing import List, Dict, Any
import re
from dataclasses import dataclass
from enum import Enum

from cryptic.core.hash_identifier import HashIdentifier, HashAnalysis
from cryptic.core.sensitive_detector import SensitiveDataDetector, SensitiveAnalysis


class DataSensitivity(Enum):
    """Niveles de sensibilidad de datos"""
    NONE = "No sensible"
    LOW = "Sensibilidad baja" 
    MEDIUM = "Sensibilidad media"
    HIGH = "Sensibilidad alta"
    CRITICAL = "Sensibilidad crítica"


class ProtectionStatus(Enum):
    """Estados de protección de datos"""
    PROTECTED = "Protegido"
    UNPROTECTED = "Sin protección"
    PARTIALLY_PROTECTED = "Parcialmente protegido"
    UNKNOWN = "Estado desconocido"


@dataclass
class DataAnalysis:
    """
    Resultado del análisis de datos sensibles.
    
    Attributes:
        original_data: Datos originales analizados
        sensitivity_level: Nivel de sensibilidad detectado
        protection_status: Estado de protección
        hash_analysis: Análisis de hash si aplica
        sensitive_analysis: Análisis de datos sensibles si aplica
        recommendations: Recomendaciones de seguridad
        confidence: Nivel de confianza en el análisis
        analysis_time_ms: Tiempo de procesamiento en milisegundos
    """
    original_data: str
    sensitivity_level: DataSensitivity
    protection_status: ProtectionStatus
    hash_analysis: HashAnalysis | None
    sensitive_analysis: SensitiveAnalysis | None
    recommendations: List[str]
    confidence: float
    analysis_time_ms: float


class CrypticAnalyzer:
    """
    Analizador principal de Cryptic.
    
    Combina identificación de hashes con detección de datos sensibles
    para proporcionar un análisis completo de seguridad de datos.
    """
    
    def __init__(self) -> None:
        """Inicializa el analizador con sus componentes"""
        self.hash_identifier = HashIdentifier()
        self.sensitive_detector = SensitiveDataDetector()
    
    def analyze_data(self, data: str) -> DataAnalysis:
        """
        Analiza una cadena de datos para determinar sensibilidad y protección.
        
        Args:
            data: Datos a analizar
            
        Returns:
            DataAnalysis con el resultado completo del análisis
        """
        import time
        start_time = time.time()
        
        # Realizar análisis de hash (incluyendo búsqueda dentro de textos mixtos)
        hash_analysis = self._identify_hash_within_text(data)
        sensitive_analysis = self.sensitive_detector.detect(data)
        
        # Determinar nivel de sensibilidad combinando ambos análisis
        sensitivity_level = self._determine_sensitivity_level(hash_analysis, sensitive_analysis)
        
        # Determinar estado de protección
        protection_status = self._determine_protection_status(hash_analysis, sensitive_analysis)
        
        # Generar recomendaciones combinadas
        recommendations = self._generate_combined_recommendations(
            hash_analysis, sensitive_analysis, protection_status
        )
        
        # Calcular confianza general
        confidence = self._calculate_overall_confidence(hash_analysis, sensitive_analysis)
        
        analysis_time = (time.time() - start_time) * 1000  # Convertir a ms
        
        return DataAnalysis(
            original_data=data,
            sensitivity_level=sensitivity_level,
            protection_status=protection_status,
            hash_analysis=hash_analysis,
            sensitive_analysis=sensitive_analysis,
            recommendations=recommendations,
            confidence=confidence,
            analysis_time_ms=analysis_time
        )

    def _identify_hash_within_text(self, data: str) -> HashAnalysis:
        """
        Intenta identificar hashes tanto si el dato completo es un hash
        como si el hash aparece embebido dentro de un texto más largo.

        Estrategia:
        1) Intentar identificar el string completo como hash.
        2) Si no hay coincidencias, escanear posibles tokens dentro del texto
           y elegir el de mayor confianza.
        """
        # 1) Intento directo sobre el dato completo
        best_analysis = self.hash_identifier.identify(data)
        if best_analysis.possible_types:
            return best_analysis

        # 2) Escaneo de posibles tokens dentro del texto
        # Captura secuencias típicas de hashes (hex largas) y formatos con prefijos ($, *)
        candidate_tokens = re.findall(r"[\$\*]?[A-Za-z0-9./=]{16,}", data)

        best_top_confidence = -1.0
        best_local_analysis: HashAnalysis | None = None

        for token in candidate_tokens:
            local_analysis = self.hash_identifier.identify(token)
            if local_analysis.possible_types:
                top_conf = local_analysis.possible_types[0][1]
                if top_conf > best_top_confidence:
                    best_top_confidence = top_conf
                    best_local_analysis = local_analysis

        return best_local_analysis if best_local_analysis is not None else best_analysis
    
    def analyze_batch(self, data_list: List[str]) -> List[DataAnalysis]:
        """
        Analiza múltiples cadenas de datos.
        
        Args:
            data_list: Lista de datos a analizar
            
        Returns:
            Lista de DataAnalysis para cada entrada
        """
        return [self.analyze_data(data) for data in data_list]
    
    def generate_report(self, analysis_results: List[DataAnalysis]) -> Dict[str, Any]:
        """
        Genera un reporte resumen de los análisis.
        
        Args:
            analysis_results: Lista de resultados de análisis
            
        Returns:
            Diccionario con estadísticas y resumen
        """
        total_items = len(analysis_results)
        protected_count = sum(1 for a in analysis_results if a.protection_status == ProtectionStatus.PROTECTED)
        unprotected_count = sum(1 for a in analysis_results if a.protection_status == ProtectionStatus.UNPROTECTED)
        
        # Estadísticas por tipo de hash
        hash_types: Dict[str, int] = {}
        for analysis in analysis_results:
            if analysis.hash_analysis and analysis.hash_analysis.possible_types:
                hash_type = analysis.hash_analysis.possible_types[0][0].value
                hash_types[hash_type] = hash_types.get(hash_type, 0) + 1
        
        # Recomendaciones generales
        recommendations = []
        if unprotected_count > 0:
            recommendations.append(f"Se encontraron {unprotected_count} elementos sin protección")
        if protected_count == total_items:
            recommendations.append("Todos los elementos analizados están protegidos")
            
        return {
            "total_analyzed": total_items,
            "protected": protected_count,
            "unprotected": unprotected_count,
            "protection_rate": protected_count / total_items if total_items > 0 else 0,
            "hash_types_detected": hash_types,
            "recommendations": recommendations,
            "timestamp": None,  # TODO: Agregar timestamp en futuras versiones
        }
    
    def print_analysis(self, analysis: DataAnalysis, detailed: bool = False) -> None:
        """
        Imprime el resultado de un análisis de forma legible.
        
        Args:
            analysis: Resultado del análisis
            detailed: Si mostrar información detallada
        """
        print(f"Cryptic Analysis for: {analysis.original_data}")
        print("=" * 60)
        print(f"Sensitivity Level: {analysis.sensitivity_level.value}")
        print(f"Protection Status: {analysis.protection_status.value}")
        print(f"Confidence: {analysis.confidence:.1%}")
        print(f"Analysis Time: {analysis.analysis_time_ms:.1f}ms")
        
        if analysis.hash_analysis and detailed:
            print("\nHash Analysis:")
            print(f"  Length: {analysis.hash_analysis.length}")
            print(f"  Cleaned Hash: {analysis.hash_analysis.cleaned_hash}")
            
            if analysis.hash_analysis.possible_types:
                print("  Possible Types:")
                for hash_type, confidence in analysis.hash_analysis.possible_types[:3]:
                    print(f"    {hash_type.value}: {confidence:.1%}")
        
        if analysis.sensitive_analysis and analysis.sensitive_analysis.matches and detailed:
            print("\nSensitive Data Analysis:")
            print(f"  Total Matches: {analysis.sensitive_analysis.total_matches}")
            print(f"  Highest Sensitivity: {analysis.sensitive_analysis.highest_sensitivity}")
            print(f"  Detection Time: {analysis.sensitive_analysis.analysis_time_ms:.1f}ms")
            
            print("  Matches Found:")
            for match in analysis.sensitive_analysis.matches[:5]:  # Mostrar máximo 5
                validation_status = "✓ Validated" if match.is_validated else "⚠ Not validated"
                print(f"    {match.data_type.value}: {match.matched_text} ({match.confidence:.1%}) [{validation_status}]")
        
        if analysis.recommendations:
            print("\nRecommendations:")
            for i, rec in enumerate(analysis.recommendations, 1):
                print(f"  {i}. {rec}")
        
        print()
    
    def _determine_sensitivity_level(self, hash_analysis: HashAnalysis, 
                                   sensitive_analysis: SensitiveAnalysis) -> DataSensitivity:
        """
        Determina el nivel de sensibilidad combinando análisis de hash y datos sensibles.
        
        Args:
            hash_analysis: Resultado del análisis de hash
            sensitive_analysis: Resultado del análisis de datos sensibles
            
        Returns:
            Nivel de sensibilidad determinado
        """
        # Mapeo de niveles de sensibilidad del detector a enum
        sensitivity_mapping = {
            'CRITICAL': DataSensitivity.CRITICAL,
            'HIGH': DataSensitivity.HIGH,
            'MEDIUM': DataSensitivity.MEDIUM,
            'LOW': DataSensitivity.LOW,
            'NONE': DataSensitivity.NONE
        }
        
        # Si hay datos sensibles detectados, usar el mayor nivel
        if sensitive_analysis.matches:
            detected_level = sensitive_analysis.highest_sensitivity
            return sensitivity_mapping.get(detected_level, DataSensitivity.NONE)
        
        # Si es un hash, asumir sensibilidad media (datos que fueron protegidos)
        if hash_analysis.possible_types:
            return DataSensitivity.MEDIUM
        
        # Sin detecciones específicas
        return DataSensitivity.NONE
    
    def _determine_protection_status(self, hash_analysis: HashAnalysis,
                                   sensitive_analysis: SensitiveAnalysis) -> ProtectionStatus:
        """
        Determina el estado de protección de los datos.
        
        Args:
            hash_analysis: Resultado del análisis de hash
            sensitive_analysis: Resultado del análisis de datos sensibles
            
        Returns:
            Estado de protección determinado
        """
        has_hash = hash_analysis.possible_types
        has_sensitive = sensitive_analysis.matches
        
        if has_hash and not has_sensitive:
            # Es un hash sin datos sensibles detectados = PROTEGIDO
            return ProtectionStatus.PROTECTED
        
        if has_sensitive and not has_hash:
            # Datos sensibles sin hash = SIN PROTECCIÓN
            return ProtectionStatus.UNPROTECTED
        
        if has_hash and has_sensitive:
            # Ambos presentes = PARCIALMENTE PROTEGIDO (datos mixtos)
            return ProtectionStatus.PARTIALLY_PROTECTED
        
        # No hay detecciones claras
        return ProtectionStatus.UNKNOWN
    
    def _generate_combined_recommendations(self, hash_analysis: HashAnalysis,
                                         sensitive_analysis: SensitiveAnalysis,
                                         protection_status: ProtectionStatus) -> List[str]:
        """
        Genera recomendaciones combinando ambos tipos de análisis.
        
        Args:
            hash_analysis: Resultado del análisis de hash
            sensitive_analysis: Resultado del análisis de datos sensibles
            protection_status: Estado de protección determinado
            
        Returns:
            Lista de recomendaciones específicas
        """
        recommendations = []
        
        # Recomendaciones basadas en estado de protección
        if protection_status == ProtectionStatus.PROTECTED:
            if hash_analysis.possible_types:
                hash_type = hash_analysis.possible_types[0][0].value
                recommendations.append(f"✅ Datos identificados como hash {hash_type}")
                recommendations.append("Los datos parecen estar correctamente protegidos")
        
        elif protection_status == ProtectionStatus.UNPROTECTED:
            recommendations.append("⚠️  ATENCIÓN: Se detectaron datos sensibles sin protección")
            recommendations.append("Es crítico implementar medidas de protección inmediatamente")
        
        elif protection_status == ProtectionStatus.PARTIALLY_PROTECTED:
            recommendations.append("⚠️  DATOS MIXTOS: Se detectaron tanto hashes como datos sensibles")
            recommendations.append("Revise que todos los datos sensibles estén apropiadamente protegidos")
        
        # Agregar recomendaciones específicas de datos sensibles
        if sensitive_analysis.recommendations:
            recommendations.append("--- Recomendaciones específicas por tipo de dato ---")
            recommendations.extend(sensitive_analysis.recommendations)
        
        # Recomendaciones de rendimiento si aplica
        if sensitive_analysis.analysis_time_ms > 50:  # Umbral de 50ms
            recommendations.append(f"⏱️  Tiempo de análisis: {sensitive_analysis.analysis_time_ms:.1f}ms")
            if sensitive_analysis.analysis_time_ms > 100:
                recommendations.append("Considere optimizar el texto o usar análisis en lotes para mejor rendimiento")
        
        # Si no hay recomendaciones específicas, dar una general
        if not recommendations:
            recommendations.append("No se detectaron patrones específicos conocidos")
            recommendations.append("Considere verificar manualmente si los datos requieren protección")
        
        return recommendations
    
    def _calculate_overall_confidence(self, hash_analysis: HashAnalysis,
                                    sensitive_analysis: SensitiveAnalysis) -> float:
        """
        Calcula la confianza general del análisis.
        
        Args:
            hash_analysis: Resultado del análisis de hash
            sensitive_analysis: Resultado del análisis de datos sensibles
            
        Returns:
            Nivel de confianza entre 0.0 y 1.0
        """
        confidences = []
        
        # Confianza del análisis de hash
        if hash_analysis.possible_types:
            hash_confidence = hash_analysis.possible_types[0][1]
            confidences.append(hash_confidence)
        
        # Confianza promedio de detecciones sensibles
        if sensitive_analysis.matches:
            sensitive_confidences = [match.confidence for match in sensitive_analysis.matches]
            avg_sensitive_confidence = sum(sensitive_confidences) / len(sensitive_confidences)
            confidences.append(avg_sensitive_confidence)
        
        if confidences:
            return sum(confidences) / len(confidences)

        # Sin detecciones: devolver una confianza mínima si el texto parece
        # no sensible, pero 0.0 si contiene palabras críticas como 'password'.
        lowered = hash_analysis.raw_hash.lower()
        if any(flag in lowered for flag in ["password", "passwd", "contraseña"]):
            return 0.0
        return 0.15
