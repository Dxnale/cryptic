# 🔐 Cryptic
[![PyPI version](https://badge.fury.io/py/cryptic.svg)](https://badge.fury.io/py/cryptic)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/Dxnale/cryptic/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Dxnale/cryptic/actions/workflows/tests.yml)
## ✨ Características

- **🔍 Detección de datos sensibles**: Identifica emails, RUTs chilenos, números de tarjetas de crédito, teléfonos, IPs y más
- **🔒 Análisis de protección**: Evalúa si los datos están adecuadamente protegidos (hasheados/cifrados)
- **🚀 CLI intuitiva**: Interfaz de línea de comandos para análisis rápidos
- **📈 Reportes detallados**: Genera reportes en JSON, YAML y CSV
- **🎯 Alta precisión**: Algoritmos de validación avanzados con baja tasa de falsos positivos

## 📦 Instalación

```bash
pip install cryptic
```

O desde el código fuente:

```bash
git clone https://github.com/Dxnale/cryptic.git
cd cryptic
pip install -e .
```

## 🚀 Uso rápido

### CLI

```bash
# Analizar una cadena individual
cryptic analyze "juan.perez@empresa.cl"

# Verificar archivo CSV
cryptic verify datos.csv --column=email

# Procesamiento por lotes con reporte
cryptic batch usuarios.csv --output=reporte.json
```

### Python API

```python
from cryptic import CrypticAnalyzer

analyzer = CrypticAnalyzer()

# Análisis individual
result = analyzer.analyze_data("12.345.678-5")
print(f"Sensibilidad: {result.sensitivity_level.value}")
print(f"Estado: {result.protection_status.value}")

# Análisis por lotes
data = ["user@example.com", "$2b$10$...", "plain_password"]
results = analyzer.analyze_batch(data)
report = analyzer.generate_report(results)
```

## 📋 Tipos de datos detectados

| Tipo | Descripción | Precisión |
|------|-------------|-----------|
| **Email** | Direcciones de correo electrónico | 95%+ |
| **RUT Chileno** | Números de identificación chilenos | 98%+ |
| **Tarjeta de crédito** | Números de tarjetas (Visa, MC, Amex) | 99%+ |
| **Teléfono** | Números telefónicos nacionales/internacionales | 85%+ |
| **Dirección IP** | Direcciones IPv4 válidas | 92%+ |
| **Hash** | MD5, SHA-1, SHA-256, bcrypt, etc. | 80%+ |

## 📊 Ejemplo de salida

```bash
$ cryptic analyze "12.345.678-5"

🔒 12.345.678-5
   Estado: Sin protección
   Sensibilidad: Sensibilidad crítica
   Confianza: 98.0%

💡 Recomendaciones:
   1. Use HMAC-SHA256 según Ley 19.628 de Protección de Datos
   2. Implemente controles de acceso adecuados

⏱️  Tiempo de análisis: 2.3ms
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles sobre cómo contribuir al proyecto.

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🔗 Enlaces útiles

- **Documentación**: [Ver documentación completa](docs/)
- **Issues**: [Reportar bugs o solicitar features](https://github.com/Dxnale/cryptic/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/Dxnale/cryptic/discussions)

---

**¿Encontraste útil esta librería?** ⭐ ¡Dale una estrella al proyecto!
