"""
Analizador principal de Cryptic para detección y verificación de datos sensibles.

Este módulo proporciona la interfaz principal para analizar datos,
identificar información sensible y verificar su estado de protección.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

from cryptic.core.hash_identifier import HashIdentifier, HashAnalysis


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
        recommendations: Recomendaciones de seguridad
        confidence: Nivel de confianza en el análisis
    """
    original_data: str
    sensitivity_level: DataSensitivity
    protection_status: ProtectionStatus
    hash_analysis: HashAnalysis | None
    recommendations: List[str]
    confidence: float


class CrypticAnalyzer:
    """
    Analizador principal de Cryptic.
    
    Combina identificación de hashes con detección de datos sensibles
    para proporcionar un análisis completo de seguridad de datos.
    """
    
    def __init__(self):
        """Inicializa el analizador con sus componentes"""
        self.hash_identifier = HashIdentifier()
    
    def analyze_data(self, data: str) -> DataAnalysis:
        """
        Analiza una cadena de datos para determinar sensibilidad y protección.
        
        Args:
            data: Datos a analizar
            
        Returns:
            DataAnalysis con el resultado completo del análisis
        """
        # Por ahora, solo analizamos hashes (implementación actual)
        # TODO: Agregar detección de datos sensibles en futuras iteraciones
        
        hash_analysis = self.hash_identifier.identify(data)
        
        # Determinar estado de protección basado en identificación de hash
        if hash_analysis.possible_types:
            protection_status = ProtectionStatus.PROTECTED
            sensitivity_level = DataSensitivity.MEDIUM  # Asumimos que los hashes son datos sensibles
            recommendations = [
                f"Datos identificados como hash {hash_analysis.possible_types[0][0].value}",
                "Los datos parecen estar hasheados correctamente"
            ]
            confidence = hash_analysis.possible_types[0][1]
        else:
            protection_status = ProtectionStatus.UNKNOWN
            sensitivity_level = DataSensitivity.NONE
            recommendations = [
                "No se pudo identificar el formato de los datos",
                "Considere verificar si contiene información sensible"
            ]
            confidence = 0.0
            
        return DataAnalysis(
            original_data=data,
            sensitivity_level=sensitivity_level,
            protection_status=protection_status,
            hash_analysis=hash_analysis,
            recommendations=recommendations,
            confidence=confidence
        )
    
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
        hash_types = {}
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
    
    def print_analysis(self, analysis: DataAnalysis, detailed: bool = False):
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
        
        if analysis.hash_analysis and detailed:
            print("\nHash Analysis:")
            print(f"  Length: {analysis.hash_analysis.length}")
            print(f"  Cleaned Hash: {analysis.hash_analysis.cleaned_hash}")
            
            if analysis.hash_analysis.possible_types:
                print("  Possible Types:")
                for hash_type, confidence in analysis.hash_analysis.possible_types[:3]:
                    print(f"    {hash_type.value}: {confidence:.1%}")
        
        if analysis.recommendations:
            print("\nRecommendations:")
            for i, rec in enumerate(analysis.recommendations, 1):
                print(f"  {i}. {rec}")
        
        print()
