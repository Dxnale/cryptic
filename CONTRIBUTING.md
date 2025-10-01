# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a **Cryptic**! Todas las contribuciones son bienvenidas, ya sean reportes de bugs, mejoras de documentación, nuevas características o correcciones de código.

## 🚀 Cómo contribuir

### 1. Preparación del entorno

1. **Fork** el proyecto en GitHub
2. **Clona** tu fork localmente:
   ```bash
   git clone https://github.com/tuusuario/cryptic.git
   cd cryptic
   ```
3. **Crea un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
4. **Instala las dependencias**:
   ```bash
   pip install -e ".[dev]"
   ```

### 2. Desarrollo

1. **Crea una rama** para tu contribución:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   # o
   git checkout -b fix/correccion-bug
   ```

2. **Haz tus cambios** siguiendo estas guías:
   - Sigue el estilo de código existente (PEP 8)
   - Agrega tests para nuevas funcionalidades
   - Actualiza la documentación si es necesario
   - Asegúrate de que todos los tests pasan

3. **Ejecuta los tests**:
   ```bash
   pytest
   ```

4. **Verifica el código** con herramientas de calidad:
   ```bash
   # Formateo automático
   black cryptic/ tests/

   # Verificación de tipos (opcional)
   mypy cryptic/

   # Linting
   flake8 cryptic/ tests/
   ```

### 3. Commit y Push

1. **Haz commit** de tus cambios:
   ```bash
   git add .
   git commit -m "feat: agregar nueva funcionalidad de detección de X"
   ```

   Usa prefijos descriptivos en tus commits:
   - `feat:` - Nueva funcionalidad
   - `fix:` - Corrección de bug
   - `docs:` - Cambios en documentación
   - `test:` - Agregar o modificar tests
   - `refactor:` - Refactorización de código
   - `chore:` - Tareas de mantenimiento

2. **Push** a tu fork:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

### 4. Pull Request

1. Abre un **Pull Request** desde GitHub
2. Describe claramente:
   - ¿Qué problema resuelve?
   - ¿Cómo se implementó la solución?
   - ¿Se agregaron tests?
   - ¿Hay algún cambio importante que mencionar?

3. Espera la revisión del código

## 📋 Tipos de contribuciones

### 🐛 Reportar bugs

Si encuentras un bug, por favor abre un [issue](https://github.com/Dxnale/cryptic/issues) con:
- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Información del entorno (Python version, SO, etc.)

### 💡 Sugerir mejoras

Para mejoras o nuevas funcionalidades:
1. Abre un [issue](https://github.com/Dxnale/cryptic/issues) describiendo la propuesta
2. Discute la implementación con la comunidad
3. Si se aprueba, procede con el desarrollo

### 📚 Mejorar documentación

Las mejoras en documentación son muy valoradas:
- Correcciones de errores tipográficos
- Mejoras en ejemplos
- Traducciones
- Guías adicionales

## 🧪 Testing

### Ejecutar tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_analyzer.py

# Con cobertura
pytest --cov=cryptic

# Tests con output detallado
pytest -v
```

### Escribir tests

- Crea tests para nuevas funcionalidades
- Mantén cobertura > 90%
- Usa nombres descriptivos para funciones de test
- Incluye casos edge y escenarios de error

## 🔧 Configuración de desarrollo

### Herramientas recomendadas

- **Editor**: VS Code, PyCharm, Vim, etc.
- **Formateador y Linter**: Ruff (reemplaza Black + Flake8)
- **Type checker**: MyPy (opcional)

## 📝 Estándares de código

### Estilo Python

- Sigue [PEP 8](https://peps.python.org/pep-0008/)
- Usa type hints cuando sea apropiado
- Límites de línea: 127 caracteres (Ruff default)
- Imports ordenados: estándar, terceros, locales

### Commits

- Usa mensajes claros y descriptivos
- Primera línea: máximo 50 caracteres
- Usa imperativo: "Add" no "Added"
- Referencia issues cuando corresponda: `Closes #123`

### Documentación

- Documenta funciones públicas con docstrings
- Usa formato Google o NumPy
- Incluye ejemplos de uso
- Mantén documentación actualizada

## 🚨 Código de conducta

Este proyecto sigue el [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Al participar, esperas seguir estas guías.

## ❓ Preguntas

Si tienes dudas:
1. Revisa la [documentación](README.md)
2. Busca en los [issues existentes](https://github.com/Dxnale/cryptic/issues)
3. Pregunta en [Discussions](https://github.com/Dxnale/cryptic/discussions)

## 🎉 Reconocimiento

¡Gracias por contribuir a hacer **Cryptic** mejor! Todas las contribuciones son valoradas y reconocidas.

---

*Esta guía está inspirada en las mejores prácticas de proyectos OpenSource exitosos.*
