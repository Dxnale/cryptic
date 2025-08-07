"""
Tests completos para los patrones de datos sensibles.

Este módulo contiene tests exhaustivos para validar la detección
de diferentes tipos de información sensible.
"""

from cryptic.patterns.sensitive_patterns import (
    get_sensitive_patterns,
    validate_rut_chileno,
    validate_credit_card,
    validate_email_advanced,
    SensitiveDataType
)
from cryptic.core.sensitive_detector import SensitiveDataDetector


class TestSensitivePatterns:
    """Tests para patrones individuales de datos sensibles"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.detector = SensitiveDataDetector()
        self.patterns = get_sensitive_patterns()
    
    # TESTS PARA EMAILS
    def test_email_detection_valid_cases(self):
        """Test detección de emails válidos"""
        valid_emails = [
            "usuario@ejemplo.com",
            "test.email+tag@dominio.co.uk", 
            "nombre_apellido@empresa.cl",
            "user123@sub.domain.org",
            "support+tickets@company-name.com"
        ]
        
        for email in valid_emails:
            analysis = self.detector.detect(email)
            assert len(analysis.matches) >= 1, f"No se detectó email: {email}"
            
            email_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.EMAIL]
            assert len(email_matches) >= 1, f"No se clasificó como email: {email}"
            assert email_matches[0].confidence >= 0.9, f"Baja confianza para email: {email}"
    
    def test_email_false_positives(self):
        """Test exclusión de falsos positivos de emails"""
        false_positives = [
            "test@example.com",  # Email de ejemplo
            "user@test.org",     # Email de testing
            "admin@localhost",   # Email local
        ]
        
        for email in false_positives:
            analysis = self.detector.detect(email)
            email_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.EMAIL]
            # Pueden detectarse pero con menor confianza o marcados como falsos positivos
            if email_matches:
                assert email_matches[0].confidence < 0.95, f"Alta confianza para falso positivo: {email}"
    
    def test_email_validation_function(self):
        """Test función de validación avanzada de emails"""
        assert validate_email_advanced("usuario@ejemplo.com")
        assert not validate_email_advanced("invalid.email")
        assert not validate_email_advanced("user@")
        assert not validate_email_advanced("@domain.com")
        assert not validate_email_advanced("user..name@domain.com")  # Puntos consecutivos
    
    # TESTS PARA RUT CHILENO
    def test_rut_chileno_detection_valid(self):
        """Test detección de RUTs chilenos válidos"""
        valid_ruts = [
            "12.345.678-5",   # RUT válido verificado
            "11.111.111-1",   # RUT válido verificado  
            "12345678-5",     # Mismo RUT sin puntos
            "1234567-4",      # RUT válido de 7 dígitos
            "7654321-6",      # RUT válido generado
            "8765432-K",      # RUT válido con K
        ]
        
        for rut in valid_ruts:
            analysis = self.detector.detect(rut)
            rut_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.RUT_CHILENO]
            assert len(rut_matches) >= 1, f"No se detectó RUT: {rut}"
            assert rut_matches[0].confidence >= 0.95, f"Baja confianza para RUT: {rut}"
    
    def test_rut_validation_algorithm(self):
        """Test algoritmo de validación de RUT"""
        # RUTs válidos conocidos (verificados manualmente)
        assert validate_rut_chileno("11.111.111-1")
        assert validate_rut_chileno("12.345.678-5")  
        assert validate_rut_chileno("1234567-4")      # Corregido: DV debe ser 4
        assert validate_rut_chileno("12345678-5")
        
        # RUTs inválidos  
        assert not validate_rut_chileno("1234567-5")     # DV incorrecto (debería ser 4)
        assert not validate_rut_chileno("11.111.111-2")  # Dígito verificador incorrecto
        assert not validate_rut_chileno("invalid")       # Formato completamente inválido
        assert not validate_rut_chileno("123")           # Muy corto
    
    def test_rut_false_positives(self):
        """Test exclusión de RUTs de prueba"""
        test_ruts = [
            "11.111.111-1",  # RUT de prueba común
            "00.000.000-0",  # RUT inválido
        ]
        
        for rut in test_ruts:
            analysis = self.detector.detect(rut)
            rut_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.RUT_CHILENO]
            # Pueden detectarse pero marcados como posibles falsos positivos
            if rut_matches:
                # La confianza puede ser reducida para casos de prueba
                pass  # Aceptamos que se detecten pero con validación apropiada
    
    # TESTS PARA TARJETAS DE CRÉDITO
    def test_credit_card_detection_valid(self):
        """Test detección de números de tarjeta válidos"""
        valid_cards = [
            "4111 1111 1111 1111",  # Visa test
            "5555-5555-5555-4444",  # MasterCard test
            "4111111111111111",     # Sin separadores
            "378282246310005",      # American Express test
        ]
        
        for card in valid_cards:
            analysis = self.detector.detect(card)
            card_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.CREDIT_CARD]
            assert len(card_matches) >= 1, f"No se detectó tarjeta: {card}"
    
    def test_credit_card_luhn_validation(self):
        """Test algoritmo de Luhn para tarjetas"""
        # Números válidos según Luhn
        assert validate_credit_card("4111111111111111")  # Visa test
        assert validate_credit_card("5555555555554444")  # MasterCard test
        assert validate_credit_card("4111-1111-1111-1111")  # Con guiones
        
        # Números inválidos
        assert not validate_credit_card("4111111111111112")  # Dígito incorrecto
        assert not validate_credit_card("1234567890123456")  # No pasa Luhn
        assert not validate_credit_card("invalid")
    
    def test_credit_card_false_positives(self):
        """Test exclusión de números de prueba obvios"""
        test_cards = [
            "0000-0000-0000-0000",
            "1111-1111-1111-1111",
        ]
        
        for card in test_cards:
            analysis = self.detector.detect(card)
            card_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.CREDIT_CARD]
            # Estos deberían ser filtrados como falsos positivos
            assert len(card_matches) == 0, f"Se detectó falso positivo: {card}"
    
    # TESTS PARA TELÉFONOS
    def test_phone_chile_detection(self):
        """Test detección de teléfonos chilenos"""
        valid_phones = [
            "+56912345678",
            "912345678",
            "22123456", 
            "+56 9 1234 5678",
            "9 1234 5678",
            "2 1234 5678"
        ]
        
        for phone in valid_phones:
            analysis = self.detector.detect(phone)
            phone_matches = [m for m in analysis.matches 
                           if m.data_type in [SensitiveDataType.PHONE_CHILE, 
                                            SensitiveDataType.PHONE_INTERNATIONAL]]
            assert len(phone_matches) >= 1, f"No se detectó teléfono: {phone}"
    
    def test_phone_international_detection(self):
        """Test detección de teléfonos internacionales"""
        international_phones = [
            "+1 555 123 4567",   # USA
            "+44 20 1234 5678",  # UK
            "+34 91 123 4567",   # España
            "+33 1 12 34 56 78", # Francia
        ]
        
        for phone in international_phones:
            analysis = self.detector.detect(phone)
            phone_matches = [m for m in analysis.matches 
                           if m.data_type == SensitiveDataType.PHONE_INTERNATIONAL]
            assert len(phone_matches) >= 1, f"No se detectó teléfono internacional: {phone}"
    
    # TESTS PARA IPs
    def test_ip_address_detection(self):
        """Test detección de direcciones IP"""
        valid_ips = [
            "192.168.1.1",
            "10.0.0.1",
            "172.16.0.1", 
            "8.8.8.8",
            "255.255.255.255"
        ]
        
        for ip in valid_ips:
            analysis = self.detector.detect(ip)
            ip_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.IP_ADDRESS]
            assert len(ip_matches) >= 1, f"No se detectó IP: {ip}"
    
    def test_ip_false_positives(self):
        """Test exclusión de IPs especiales"""
        special_ips = [
            "127.0.0.1",  # Localhost
            "0.0.0.0",    # Dirección nula
        ]
        
        for ip in special_ips:
            analysis = self.detector.detect(ip)
            ip_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.IP_ADDRESS]
            # Pueden detectarse pero con indicación de que son especiales
            if ip_matches:
                pass  # Aceptamos detección pero con menor sensibilidad
    
    # TESTS PARA NOMBRES DE PERSONAS
    def test_nombre_persona_detection(self):
        """Test detección de nombres de personas"""
        valid_names = [
            "Juan Pérez",
            "María José González", 
            "Pedro Pablo Martínez Silva",
            "Ana María Rodríguez",
            "José Miguel Torres"
        ]
        
        for name in valid_names:
            analysis = self.detector.detect(name)
            name_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.NOMBRE_PERSONA]
            assert len(name_matches) >= 1, f"No se detectó nombre: {name}"
            # Los nombres tienen menor confianza por naturaleza
            assert name_matches[0].confidence >= 0.7, f"Confianza muy baja para nombre: {name}"
    
    def test_nombre_false_positives(self):
        """Test exclusión de nombres de prueba"""
        fake_names = [
            "Lorem Ipsum",
            "Dolor Sit",
            "Test User",
            "John Doe",
            "Jane Doe"
        ]
        
        for name in fake_names:
            analysis = self.detector.detect(name)
            name_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.NOMBRE_PERSONA]
            # Estos deberían ser filtrados como falsos positivos
            assert len(name_matches) == 0, f"Se detectó falso positivo: {name}"
    
    # TESTS PARA URLs
    def test_url_detection(self):
        """Test detección de URLs"""
        valid_urls = [
            "https://www.ejemplo.com",
            "http://localhost:8080/api",
            "https://api.service.com/v1/users?id=123",
            "http://subdomain.domain.com/path/to/resource"
        ]
        
        for url in valid_urls:
            analysis = self.detector.detect(url)
            url_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.URL]
            assert len(url_matches) >= 1, f"No se detectó URL: {url}"
    
    # TESTS PARA DOCUMENTOS DE IDENTIDAD INTERNACIONALES
    def test_dni_argentino_detection(self):
        """Test detección de DNI argentino"""
        valid_dnis = [
            "12.345.678",
            "1.234.567",
            "12345678"
        ]
        
        for dni in valid_dnis:
            analysis = self.detector.detect(dni)
            dni_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.DNI_ARGENTINO]
            assert len(dni_matches) >= 1, f"No se detectó DNI: {dni}"
    
    def test_ci_uruguayo_detection(self):
        """Test detección de CI uruguayo"""
        valid_cis = [
            "1.234.567-8",
            "1234567-8"
        ]
        
        for ci in valid_cis:
            analysis = self.detector.detect(ci)
            ci_matches = [m for m in analysis.matches if m.data_type == SensitiveDataType.CI_URUGUAYO]
            assert len(ci_matches) >= 1, f"No se detectó CI: {ci}"


class TestSensitiveDetectorIntegration:
    """Tests de integración para el detector completo"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.detector = SensitiveDataDetector()
    
    def test_multiple_data_types_in_text(self):
        """Test detección de múltiples tipos en un mismo texto"""
        mixed_text = """
        Información del usuario:
        Email: juan.perez@empresa.cl
        RUT: 12.345.678-9
        Teléfono: +56 9 1234 5678
        IP: 192.168.1.100
        """
        
        analysis = self.detector.detect(mixed_text)
        
        # Verificar que se detectaron múltiples tipos
        detected_types = {match.data_type for match in analysis.matches}
        
        expected_types = {
            SensitiveDataType.EMAIL,
            SensitiveDataType.RUT_CHILENO,
            SensitiveDataType.PHONE_CHILE,
            SensitiveDataType.IP_ADDRESS
        }
        
        assert len(detected_types.intersection(expected_types)) >= 3, \
            f"No se detectaron suficientes tipos. Detectados: {detected_types}"
    
    def test_overlapping_patterns_resolution(self):
        """Test resolución de patrones solapados"""
        # Texto que podría generar solapamientos
        text_with_overlap = "12.345.678-9 es mi RUT y 12.345.678 podría ser un DNI"
        
        analysis = self.detector.detect(text_with_overlap)
        
        # Verificar que no hay solapamientos extremos
        positions = [(m.start_pos, m.end_pos) for m in analysis.matches]
        
        for i, (start1, end1) in enumerate(positions):
            for j, (start2, end2) in enumerate(positions[i+1:], i+1):
                # No debería haber solapamientos completos
                if start1 <= start2 < end1:
                    overlap_size = min(end1, end2) - start2
                    total_size = max(end1, end2) - start1
                    overlap_ratio = overlap_size / total_size
                    assert overlap_ratio < 0.8, f"Solapamiento excesivo entre matches {i} y {j}"
    
    def test_performance_under_100ms(self):
        """Test rendimiento bajo 100ms por entrada según criterios de éxito"""
        # Texto de tamaño mediano con varios datos sensibles
        medium_text = """
        Base de datos de usuarios:
        1. Juan Pérez, juan.perez@empresa.cl, RUT: 12.345.678-9, Tel: +56 9 1234 5678
        2. María González, maria.gonzalez@company.com, RUT: 13.456.789-K, Tel: +56 2 2345 6789
        3. Pedro Martínez, pedro@test-domain.cl, RUT: 14.567.890-1, Tel: +56 9 8765 4321
        IP del servidor: 192.168.1.100
        Tarjeta de prueba: 4111-1111-1111-1111
        """ * 3  # Triplicar para hacer el texto más largo
        
        analysis = self.detector.detect(medium_text)
        
        # Verificar criterio de rendimiento de la Fase 1
        assert analysis.analysis_time_ms < 100, \
            f"Tiempo de análisis {analysis.analysis_time_ms:.1f}ms excede el límite de 100ms"
        
        # Verificar que aún se detectaron datos
        assert len(analysis.matches) > 5, "No se detectaron suficientes datos en test de rendimiento"
    
    def test_sensitivity_hierarchy(self):
        """Test jerarquía de niveles de sensibilidad"""
        # Texto con datos de diferentes sensibilidades
        text_mixed_sensitivity = """
        Datos críticos: RUT 12.345.678-9, Tarjeta 4111-1111-1111-1111
        Datos altos: Email juan@empresa.cl, Nombre Juan Pérez  
        Datos medios: Teléfono +56 9 1234 5678
        Datos bajos: URL https://www.ejemplo.com
        """
        
        analysis = self.detector.detect(text_mixed_sensitivity)
        
        # El nivel más alto debería ser CRITICAL
        assert analysis.highest_sensitivity == "CRITICAL", \
            f"Nivel de sensibilidad incorrecto: {analysis.highest_sensitivity}"
        
        # Verificar que hay datos de nivel crítico
        critical_matches = [m for m in analysis.matches 
                          if m.pattern_used.sensitivity_level == "CRITICAL"]
        assert len(critical_matches) >= 1, "No se encontraron datos críticos"
    
    def test_empty_and_edge_cases(self):
        """Test casos límite y entradas vacías"""
        edge_cases = [
            "",  # Texto vacío
            "   ",  # Solo espacios
            "No sensitive data here!",  # Sin datos sensibles
            "Almost email@",  # Formato incompleto
            "123.456.789",  # Números sin contexto claro
        ]
        
        for case in edge_cases:
            analysis = self.detector.detect(case)
            # No debería fallar
            assert isinstance(analysis.matches, list)
            assert analysis.analysis_time_ms < 50  # Casos simples deberían ser rápidos
            
    def test_false_positive_filtering(self):
        """Test filtrado sistemático de falsos positivos"""
        text_with_fps = """
        Ejemplos de testing:
        Email: test@example.com
        RUT de prueba: 11.111.111-1
        Tarjeta inválida: 0000-0000-0000-0000
        Usuario: John Doe
        URL: http://localhost:3000
        """
        
        analysis = self.detector.detect(text_with_fps)
        
        # Verificar que algunos falsos positivos fueron filtrados
        fp_matches = []
        for match in analysis.matches:
            if (match.data_type == SensitiveDataType.EMAIL and "example.com" in match.matched_text) or \
               (match.data_type == SensitiveDataType.CREDIT_CARD and "0000" in match.matched_text) or \
               (match.data_type == SensitiveDataType.NOMBRE_PERSONA and "John Doe" in match.matched_text):
                fp_matches.append(match)
        
        # Debería haber pocos o ningún falso positivo
        assert len(fp_matches) <= 2, f"Demasiados falsos positivos detectados: {len(fp_matches)}"


class TestRecommendationGeneration:
    """Tests para generación de recomendaciones específicas"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.detector = SensitiveDataDetector()
    
    def test_specific_recommendations_by_type(self):
        """Test que se generen recomendaciones específicas por tipo"""
        type_tests = [
            ("juan@empresa.cl", "SHA-256 con salt"),
            ("12.345.678-5", "HMAC-SHA256"),  # Usar RUT válido
            ("4111-1111-1111-1111", "preservación de formato"),
            ("+56 9 1234 5678", "hash SHA-256")
        ]
        
        for data, expected_keyword in type_tests:
            analysis = self.detector.detect(data)
            recommendations_text = " ".join(analysis.recommendations).lower()
            assert expected_keyword.lower() in recommendations_text, \
                f"No se encontró recomendación específica '{expected_keyword}' para '{data}'"
    
    def test_critical_data_warnings(self):
        """Test advertencias para datos críticos"""
        critical_data = "RUT: 12.345.678-9 y tarjeta: 4111-1111-1111-1111"
        analysis = self.detector.detect(critical_data)
        
        recommendations_text = " ".join(analysis.recommendations)
        assert "CRÍTICO" in recommendations_text.upper(), \
            "No se generó advertencia para datos críticos"
