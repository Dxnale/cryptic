"""
Tests de integración para CrypticAnalyzer con detección de datos sensibles.

Este módulo valida que el CrypticAnalyzer integre correctamente
la detección de hashes y datos sensibles.
"""

from cryptic.core.analyzer import CrypticAnalyzer, DataSensitivity, ProtectionStatus
from cryptic.patterns.sensitive_patterns import SensitiveDataType


class TestCrypticAnalyzerIntegration:
    """Tests de integración para el analizador principal"""

    def setup_method(self):
        """Setup para cada test"""
        self.analyzer = CrypticAnalyzer()

    def test_analyze_hash_only(self):
        """Test análisis de solo hash (comportamiento previo)"""
        hash_md5 = "5d41402abc4b2a76b9719d911017c592"  # MD5 de "hello"
        analysis = self.analyzer.analyze_data(hash_md5)

        # Verificar estructura básica
        assert analysis.original_data == hash_md5
        assert analysis.protection_status == ProtectionStatus.PROTECTED
        assert analysis.sensitivity_level == DataSensitivity.MEDIUM
        assert analysis.hash_analysis is not None
        assert analysis.sensitive_analysis is not None
        assert analysis.confidence > 0.7
        assert analysis.analysis_time_ms > 0

        # Verificar que se identificó como hash
        assert len(analysis.hash_analysis.possible_types) > 0
        assert "MD5" in analysis.hash_analysis.possible_types[0][0].value

        # No debería detectar datos sensibles (es un hash)
        assert len(analysis.sensitive_analysis.matches) == 0

    def test_analyze_sensitive_data_only(self):
        """Test análisis de solo datos sensibles (nuevo comportamiento)"""
        email = "juan.perez@empresa.cl"
        analysis = self.analyzer.analyze_data(email)

        # Verificar detección de datos sensibles
        assert analysis.protection_status == ProtectionStatus.UNPROTECTED
        assert analysis.sensitivity_level == DataSensitivity.HIGH
        assert analysis.sensitive_analysis is not None
        assert len(analysis.sensitive_analysis.matches) >= 1

        # Verificar que se detectó como email
        email_matches = [m for m in analysis.sensitive_analysis.matches if m.data_type == SensitiveDataType.EMAIL]
        assert len(email_matches) >= 1
        assert email_matches[0].matched_text == email

        # No debería detectar como hash
        assert len(analysis.hash_analysis.possible_types) == 0

    def test_analyze_critical_sensitive_data(self):
        """Test análisis de datos de sensibilidad crítica"""
        rut = "12.345.678-9"
        analysis = self.analyzer.analyze_data(rut)

        # Verificar nivel crítico
        assert analysis.sensitivity_level == DataSensitivity.CRITICAL
        assert analysis.protection_status == ProtectionStatus.UNPROTECTED

        # Verificar detección específica de RUT
        rut_matches = [m for m in analysis.sensitive_analysis.matches if m.data_type == SensitiveDataType.RUT_CHILENO]
        assert len(rut_matches) >= 1
        assert "CRÍTICO" in " ".join(analysis.recommendations).upper()

    def test_analyze_mixed_data(self):
        """Test análisis de datos mixtos (hash + sensibles)"""
        mixed_data = "User: juan@empresa.cl, Hash: 5d41402abc4b2a76b9719d911017c592"
        analysis = self.analyzer.analyze_data(mixed_data)

        # Debería detectar como parcialmente protegido
        assert analysis.protection_status == ProtectionStatus.PARTIALLY_PROTECTED

        # Debería tener tanto análisis de hash como sensibles
        assert analysis.hash_analysis is not None
        assert len(analysis.hash_analysis.possible_types) > 0
        assert analysis.sensitive_analysis is not None
        assert len(analysis.sensitive_analysis.matches) > 0

        # La sensibilidad debería basarse en los datos sensibles (más alta)
        assert analysis.sensitivity_level.value != DataSensitivity.NONE.value

    def test_analyze_no_detection(self):
        """Test análisis sin detecciones específicas"""
        plain_text = "Just some plain text without sensitive information"
        analysis = self.analyzer.analyze_data(plain_text)

        assert analysis.protection_status == ProtectionStatus.UNKNOWN
        assert analysis.sensitivity_level == DataSensitivity.NONE
        assert len(analysis.hash_analysis.possible_types) == 0
        assert len(analysis.sensitive_analysis.matches) == 0
        assert analysis.confidence <= 0.2  # Baja confianza sin detecciones

    def test_batch_analysis_mixed_types(self):
        """Test análisis en lote con tipos mixtos"""
        test_data = [
            "5d41402abc4b2a76b9719d911017c592",  # Hash MD5
            "juan.perez@empresa.cl",  # Email
            "12.345.678-9",  # RUT
            "plain text",  # Sin detecciones
            "4111-1111-1111-1111",  # Tarjeta
        ]

        results = self.analyzer.analyze_batch(test_data)

        assert len(results) == 5

        # Verificar cada resultado específico
        assert results[0].protection_status == ProtectionStatus.PROTECTED  # Hash
        assert results[1].protection_status == ProtectionStatus.UNPROTECTED  # Email
        assert results[2].protection_status == ProtectionStatus.UNPROTECTED  # RUT
        assert results[3].protection_status == ProtectionStatus.UNKNOWN  # Plain text
        assert results[4].protection_status == ProtectionStatus.UNPROTECTED  # Tarjeta

        # Verificar niveles de sensibilidad
        assert results[0].sensitivity_level == DataSensitivity.MEDIUM  # Hash (protegido)
        assert results[1].sensitivity_level == DataSensitivity.HIGH  # Email
        assert results[2].sensitivity_level == DataSensitivity.CRITICAL  # RUT
        assert results[3].sensitivity_level == DataSensitivity.NONE  # Plain text
        assert results[4].sensitivity_level == DataSensitivity.CRITICAL  # Tarjeta

    def test_recommendation_generation_integration(self):
        """Test generación integrada de recomendaciones"""
        test_cases = [
            # (datos, expectativas_en_recomendaciones)
            ("5d41402abc4b2a76b9719d911017c592", ["MD5", "protegidos"]),
            ("juan@empresa.cl", ["ATENCIÓN", "sin protección", "SHA-256"]),
            ("12.345.678-9", ["CRÍTICO", "HMAC-SHA256"]),
            ("4111-1111-1111-1111", ["preservación de formato", "PCI DSS"]),
        ]

        for data, expected_keywords in test_cases:
            analysis = self.analyzer.analyze_data(data)
            recommendations_text = " ".join(analysis.recommendations).lower()

            for keyword in expected_keywords:
                assert keyword.lower() in recommendations_text, (
                    f"Keyword '{keyword}' no encontrada en recomendaciones para '{data}'"
                )

    def test_confidence_calculation_integration(self):
        """Test cálculo integrado de confianza"""
        test_cases = [
            # (datos, confianza_mínima_esperada)
            ("5d41402abc4b2a76b9719d911017c592", 0.8),  # Hash con alta confianza
            ("juan.perez@empresa.cl", 0.9),  # Email válido
            ("12.345.678-9", 0.95),  # RUT con validación
            ("maybe_not_sensitive", 0.15),  # Sin detecciones claras
        ]

        for data, min_confidence in test_cases:
            analysis = self.analyzer.analyze_data(data)
            assert analysis.confidence >= min_confidence, (
                f"Confianza {analysis.confidence:.2f} menor que esperada {min_confidence} para '{data}'"
            )

    def test_performance_integration(self):
        """Test rendimiento del análisis integrado"""
        # Datos complejos que activen múltiples detectores
        complex_data = """
        Información completa del usuario:
        Nombre: Juan Pérez González
        Email: juan.perez@empresa.cl
        RUT: 12.345.678-9
        Teléfono: +56 9 1234 5678
        IP: 192.168.1.100
        Tarjeta: 4111-1111-1111-1111
        Hash anterior: 5d41402abc4b2a76b9719d911017c592
        URL perfil: https://empresa.cl/users/juan.perez
        """

        analysis = self.analyzer.analyze_data(complex_data)

        # Verificar criterio de rendimiento (<100ms)
        assert analysis.analysis_time_ms < 100, f"Análisis integrado tomó {analysis.analysis_time_ms:.1f}ms (límite: 100ms)"

        # Verificar que detectó múltiples tipos
        assert len(analysis.sensitive_analysis.matches) >= 5, (
            f"Solo se detectaron {len(analysis.sensitive_analysis.matches)} elementos en datos complejos"
        )

        # Verificar nivel crítico por presencia de RUT y tarjeta
        assert analysis.sensitivity_level == DataSensitivity.CRITICAL

    def test_error_handling_and_edge_cases(self):
        """Test manejo de errores y casos límite"""
        edge_cases = [
            "",  # Texto vacío
            "   \n\t   ",  # Solo espacios y saltos
            "A" * 10000,  # Texto muy largo sin patrones
            "Email: @domain.com",  # Formato inválido
            "RUT: 00.000.000-0",  # RUT técnicamente inválido
        ]

        for case in edge_cases:
            # No debería fallar con excepciones
            analysis = self.analyzer.analyze_data(case)

            # Verificar estructura básica mantenida
            assert isinstance(analysis.recommendations, list)
            assert isinstance(analysis.confidence, float)
            assert 0 <= analysis.confidence <= 1
            assert analysis.analysis_time_ms >= 0
            assert analysis.sensitive_analysis is not None
            assert analysis.hash_analysis is not None

    def test_generate_report_with_sensitive_data(self):
        """Test generación de reportes con datos sensibles"""
        test_data = ["juan@empresa.cl", "5d41402abc4b2a76b9719d911017c592", "12.345.678-9", "plain text"]

        analyses = self.analyzer.analyze_batch(test_data)
        report = self.analyzer.generate_report(analyses)

        # Verificar estructura del reporte
        assert "total_analyzed" in report
        assert "protected" in report
        assert "unprotected" in report
        assert "protection_rate" in report
        assert "recommendations" in report

        # Verificar estadísticas
        assert report["total_analyzed"] == 4
        assert report["protected"] >= 1  # Al menos el hash
        assert report["unprotected"] >= 2  # Email y RUT mínimo

        # Verificar que las recomendaciones mencionan datos sensibles
        recommendations_text = " ".join(report["recommendations"])
        assert len(recommendations_text) > 0

    def test_print_analysis_detailed_with_sensitive(self):
        """Test impresión detallada con datos sensibles"""
        import io
        import sys

        # Datos que tengan tanto hash como sensibles
        mixed_data = "User juan@empresa.cl with hash 5d41402abc4b2a76b9719d911017c592"
        analysis = self.analyzer.analyze_data(mixed_data)

        # Capturar salida
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        try:
            self.analyzer.print_analysis(analysis, detailed=True)
            output = buffer.getvalue()
        finally:
            sys.stdout = old_stdout

        # Verificar que incluye información de datos sensibles
        assert "Sensitive Data Analysis" in output
        assert "Total Matches" in output
        assert "Hash Analysis" in output
        assert analysis.original_data in output

        # Verificar formato de tiempo
        assert "Analysis Time" in output
        assert "ms" in output
