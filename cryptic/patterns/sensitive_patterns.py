"""
Patrones de identificación para diferentes tipos de datos sensibles.

Este módulo contiene la definición de patrones utilizados para identificar
automáticamente diferentes tipos de información sensible como emails,
RUT chilenos, números de tarjetas de crédito, teléfonos, etc.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Callable
import re


class SensitiveDataType(Enum):
    """Enumeración de tipos de datos sensibles soportados"""
    
    EMAIL = "Email"
    RUT_CHILENO = "RUT Chileno"
    CREDIT_CARD = "Número de Tarjeta de Crédito"
    PHONE_CHILE = "Teléfono Chileno" 
    PHONE_INTERNATIONAL = "Teléfono Internacional"
    IP_ADDRESS = "Dirección IP"
    NOMBRE_PERSONA = "Nombre de Persona"
    URL = "URL"
    DNI_ARGENTINO = "DNI Argentino"
    CI_URUGUAYO = "Cédula de Identidad Uruguaya"
    UNKNOWN = "Desconocido"


@dataclass
class SensitivePattern:
    """Patrón de identificación de dato sensible
    
    Parámetros
    ----------
    data_type : SensitiveDataType
        Tipo de dato sensible que representa este patrón
    regex : str
        Expresión regular para identificar el patrón
    sensitivity_level : str
        Nivel de sensibilidad (CRITICAL, HIGH, MEDIUM, LOW)
    confidence : float
        Nivel de confianza en la identificación (0.0-1.0)
    description : str
        Descripción legible del tipo de dato
    validation_func : callable, opcional
        Función adicional de validación específica
    examples : List[str]
        Ejemplos válidos de este tipo de dato
    false_positive_patterns : List[str], opcional
        Patrones que ayudan a descartar falsos positivos
    """
    
    data_type: SensitiveDataType
    regex: str
    sensitivity_level: str
    confidence: float
    description: str
    validation_func: Optional[Callable] = None
    examples: List[str] = field(default_factory=list)
    false_positive_patterns: Optional[List[str]] = None


def validate_rut_chileno(rut: str) -> bool:
    """
    Valida que un RUT chileno tenga dígito verificador correcto.
    
    Args:
        rut: RUT a validar (ej: "12.345.678-9")
        
    Returns:
        True si el RUT es válido, False en caso contrario
    """
    # Limpiar el RUT
    rut_clean = re.sub(r'[.-]', '', rut.upper())
    
    if len(rut_clean) < 2:
        return False
        
    # Separar número y dígito verificador
    numero = rut_clean[:-1]
    dv = rut_clean[-1]
    
    try:
        int(numero)
    except ValueError:
        return False
    
    # Calcular dígito verificador usando algoritmo correcto
    multiplicador = 2
    suma = 0
    
    for digit in reversed(numero):
        suma += int(digit) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    
    resto = suma % 11
    dv_calculado = 'K' if resto == 1 else ('0' if resto == 0 else str(11 - resto))
    
    return dv == dv_calculado


def validate_credit_card(numero: str) -> bool:
    """
    Valida número de tarjeta de crédito usando algoritmo de Luhn.
    
    Args:
        numero: Número de tarjeta a validar
        
    Returns:
        True si es válido según Luhn, False en caso contrario
    """
    # Limpiar espacios y guiones
    numero_clean = re.sub(r'[\s-]', '', numero)
    
    if not numero_clean.isdigit() or len(numero_clean) < 13:
        return False
    
    # Algoritmo de Luhn
    total = 0
    reverse_digits = numero_clean[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Cada segundo dígito
            n *= 2
            if n > 9:
                n = n // 10 + n % 10
        total += n
    
    return total % 10 == 0


def validate_email_advanced(email: str) -> bool:
    """
    Validación avanzada de email que considera casos especiales.
    
    Args:
        email: Email a validar
        
    Returns:
        True si el email es válido, False en caso contrario
    """
    # Patrón básico pero robusto para emails
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False
    
    # Validaciones adicionales
    local, domain = email.split('@')
    
    # Local part no debe empezar o terminar con punto
    if local.startswith('.') or local.endswith('.'):
        return False
        
    # No debe tener puntos consecutivos
    if '..' in local or '..' in domain:
        return False
    
    # Domain debe tener al menos un punto
    if '.' not in domain:
        return False
        
    return True


def get_sensitive_patterns() -> List[SensitivePattern]:
    """Retorna la lista completa de patrones de datos sensibles"""
    
    patterns = [
        # EMAIL
        SensitivePattern(
            data_type=SensitiveDataType.EMAIL,
            regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            sensitivity_level="HIGH",
            confidence=0.95,
            description="Dirección de correo electrónico",
            validation_func=validate_email_advanced,
            examples=[
                "usuario@ejemplo.com",
                "test.email+tag@dominio.co.uk",
                "nombre_apellido@empresa.cl"
            ],
            false_positive_patterns=[
                r'.*@example\.(com|org|net)$',  # Emails de ejemplo
                r'.*@test\.(com|org|net)$',     # Emails de testing
            ]
        ),
        
        # RUT CHILENO (con mayor especificidad)
        SensitivePattern(
            data_type=SensitiveDataType.RUT_CHILENO,
            regex=r'\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b',  # Requiere guión obligatorio
            sensitivity_level="CRITICAL", 
            confidence=0.98,
            description="RUT o RUN chileno (Rol Único Tributario/Nacional)",
            validation_func=validate_rut_chileno,
            examples=[
                "12.345.678-5",
                "1.234.567-K", 
                "12345678-5",
                "1234567-K"
            ],
            false_positive_patterns=[
                r'00\.000\.000-0',  # RUT inválido
            ]
        ),
        
        # NÚMEROS DE TARJETA DE CRÉDITO
        SensitivePattern(
            data_type=SensitiveDataType.CREDIT_CARD,
            regex=r'\b(?:\d{4}[-\s]?){3}\d{4}\b|\b\d{13,19}\b',
            sensitivity_level="CRITICAL",
            confidence=0.99,
            description="Número de tarjeta de crédito",
            validation_func=validate_credit_card,
            examples=[
                "4111 1111 1111 1111",
                "5555-5555-5555-4444", 
                "4111111111111111",
                "378282246310005"
            ],
            false_positive_patterns=[
                r'0000[-\s]?0000[-\s]?0000[-\s]?0000',  # Número de prueba
                r'1111[-\s]?1111[-\s]?1111[-\s]?1111',  # Otro número de prueba
            ]
        ),
        
        # TELÉFONOS CHILENOS
        SensitivePattern(
            data_type=SensitiveDataType.PHONE_CHILE,
            regex=r'\b(?:\+56[-\s]?)?(?:[2-9]\d{8}|[2-9][-\s]?\d{4}[-\s]?\d{4}|[2-9][-\s]?\d{3}[-\s]?\d{4})\b',
            sensitivity_level="MEDIUM",
            confidence=0.90,
            description="Número de teléfono chileno",
            examples=[
                "+56912345678",
                "912345678", 
                "22123456",
                "9 1234 5678"
            ]
        ),
        
        # TELÉFONOS INTERNACIONALES
        SensitivePattern(
            data_type=SensitiveDataType.PHONE_INTERNATIONAL,
            regex=r'\+\d{1,3}[-\s]?(?:\d[-\s]?){6,14}\d',
            sensitivity_level="MEDIUM", 
            confidence=0.85,
            description="Número de teléfono internacional",
            examples=[
                "+1 555 123 4567",
                "+44 20 1234 5678",
                "+34 91 123 4567"
            ]
        ),
        
        # DIRECCIONES IP
        SensitivePattern(
            data_type=SensitiveDataType.IP_ADDRESS,
            regex=r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            sensitivity_level="MEDIUM",
            confidence=0.92,
            description="Dirección IP v4",
            examples=[
                "192.168.1.1",
                "10.0.0.1", 
                "172.16.0.1"
            ],
            false_positive_patterns=[
                r'127\.0\.0\.1',      # Localhost
                r'0\.0\.0\.0',        # Dirección nula
            ]
        ),
        
        # NOMBRES DE PERSONAS (BÁSICO)
        SensitivePattern(
            data_type=SensitiveDataType.NOMBRE_PERSONA,
            regex=r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*\b',
            sensitivity_level="HIGH",
            confidence=0.75,  # Menor confianza porque puede tener falsos positivos
            description="Posible nombre de persona",
            examples=[
                "Juan Pérez",
                "María José González",
                "Pedro Pablo Martínez Silva"
            ],
            false_positive_patterns=[
                r'Lorem Ipsum',
                r'Dolor Sit',
                r'Test User',
                r'John Doe',
                r'Jane Doe'
            ]
        ),
        
        # URLs
        SensitivePattern(
            data_type=SensitiveDataType.URL,
            regex=r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w)*)?)?',
            sensitivity_level="LOW",
            confidence=0.95,
            description="URL o dirección web",
            examples=[
                "https://www.ejemplo.com",
                "http://localhost:8080/api",
                "https://api.service.com/v1/users?id=123"
            ]
        ),
        
        # DNI ARGENTINO (sin guión, para diferenciarlo del RUT)
        SensitivePattern(
            data_type=SensitiveDataType.DNI_ARGENTINO,
            regex=r'\b(?:\d{1,2}\.?\d{3}\.?\d{3}(?!-)|(?<!\d)\d{7,8}(?!\d))\b',
            sensitivity_level="CRITICAL",
            confidence=0.87,  # Ligeramente mayor confianza
            description="DNI Argentino",
            examples=[
                "12.345.678",
                "1.234.567",
                "12345678"
            ]
        ),
        
        # CÉDULA URUGUAYA (más específica: exactamente 8 dígitos con último dígito)
        SensitivePattern(
            data_type=SensitiveDataType.CI_URUGUAYO,
            regex=r'\b\d{1}\.?\d{3}\.?\d{3}-\d{1}\b',  # Requiere guión obligatorio
            sensitivity_level="CRITICAL", 
            confidence=0.88,
            description="Cédula de Identidad Uruguaya",
            examples=[
                "1.234.567-8",
                "1234567-8"
            ]
        )
    ]
    
    return patterns


def get_patterns_by_type(data_type: SensitiveDataType) -> List[SensitivePattern]:
    """
    Retorna patrones filtrados por tipo de dato.
    
    Args:
        data_type: Tipo de dato sensible a filtrar
        
    Returns:
        Lista de patrones que coinciden con el tipo
    """
    all_patterns = get_sensitive_patterns()
    return [p for p in all_patterns if p.data_type == data_type]


def get_patterns_by_sensitivity(sensitivity_level: str) -> List[SensitivePattern]:
    """
    Retorna patrones filtrados por nivel de sensibilidad.
    
    Args:
        sensitivity_level: Nivel de sensibilidad (CRITICAL, HIGH, MEDIUM, LOW)
        
    Returns:
        Lista de patrones que coinciden con el nivel
    """
    all_patterns = get_sensitive_patterns()
    return [p for p in all_patterns if p.sensitivity_level == sensitivity_level]


# Cache para compilar regex una sola vez
_COMPILED_PATTERNS: Optional[Dict[str, re.Pattern]] = None


def get_compiled_patterns() -> Dict[str, re.Pattern]:
    """
    Retorna patrones regex compilados para mejor rendimiento.
    
    Returns:
        Diccionario con patrones compilados indexados por tipo de dato
    """
    global _COMPILED_PATTERNS
    
    if _COMPILED_PATTERNS is None:
        _COMPILED_PATTERNS = {}
        patterns = get_sensitive_patterns()
        
        for pattern in patterns:
            key = f"{pattern.data_type.value}"
            _COMPILED_PATTERNS[key] = re.compile(pattern.regex, re.IGNORECASE)
    
    return _COMPILED_PATTERNS
