# Roadmap de Desarrollo - Proyecto Cryptic

Este documento define el plan de desarrollo futuro para implementar las funcionalidades prometidas en el README que actualmente no están implementadas.

## 🎯 **Funcionalidades Faltantes Identificadas**

### **📊 Estado Actual vs Prometido**

| Funcionalidad | Estado README | Estado Implementación | Prioridad |
|---------------|---------------|----------------------|-----------|
| Identificación de hashes | ✅ Prometido | ✅ **COMPLETADO** | N/A |
| Detección de datos sensibles | ✅ Prometido | ❌ No implementado | **ALTA** |
| CLI | ✅ Prometido | ❌ No implementado | **ALTA** |
| Configuración de reglas | ✅ Prometido | ❌ No implementado | **MEDIA** |
| Sugerencias de encriptación | ✅ Prometido | ❌ No implementado | **MEDIA** |
| Detección de datos cifrados | ✅ Prometido | ❌ No implementado | **BAJA** |
| Integración con testing | ✅ Prometido | ⚠️ Parcial | **BAJA** |

---

## 🚀 **Plan de Desarrollo por Fases**

### **Fase 1: Detección de Datos Sensibles** ⭐ *PRIORIDAD ALTA*

#### **Objetivo**
Implementar detección automática de información sensible como emails, nombres, RUT, números de tarjetas, etc.

#### **Tareas**
1. **Crear módulo de patrones de datos sensibles**
   ```
   cryptic/patterns/sensitive_patterns.py
   ```
   - Patrones regex para emails
   - Patrones para RUT/DNI chilenos
   - Patrones para números de tarjetas de crédito
   - Patrones para nombres comunes
   - Patrones para teléfonos
   - Patrones para direcciones IP

2. **Extender CrypticAnalyzer**
   - Integrar detección de datos sensibles
   - Actualizar enum `DataSensitivity`
   - Mejorar lógica de recomendaciones

3. **Testing**
   - Tests para cada tipo de dato sensible
   - Tests de falsos positivos/negativos
   - Tests de rendimiento

#### **Criterios de Éxito**
- [ ] Detecta emails con 95%+ precisión
- [ ] Detecta RUT chilenos con 98%+ precisión
- [ ] Detecta números de tarjetas con 99%+ precisión
- [ ] Tiempo de procesamiento < 100ms por entrada

#### **Estimación**: 2-3 semanas

---

### **Fase 2: Interfaz de Línea de Comandos** ⭐ *PRIORIDAD ALTA*

#### **Objetivo**
Crear CLI para uso desde terminal, cumpliendo con los requisitos del README.

#### **Tareas**
1. **Implementar CLI principal**
   ```
   cryptic/cli/main.py
   ```
   - Comando `cryptic verify <archivo>`
   - Comando `cryptic analyze <entrada>`
   - Comando `cryptic batch <archivo.csv>`
   - Opciones de configuración

2. **Configurar entry points**
   - Actualizar `pyproject.toml`
   - Crear comando ejecutable `cryptic`

3. **Manejo de archivos**
   - Lectura de CSV
   - Lectura de archivos de texto
   - Exportar reportes

#### **Comandos Esperados**
```bash
# Verificar archivo CSV
cryptic verify datos.csv --column=password

# Analizar entrada individual
cryptic analyze "user@example.com"

# Generar reporte completo
cryptic batch datos.csv --output=reporte.json
```

#### **Criterios de Éxito**
- [ ] CLI instalable via `uv run cryptic --help`
- [ ] Procesa archivos CSV correctamente
- [ ] Genera reportes en múltiples formatos
- [ ] Manejo de errores robusto

#### **Estimación**: 1-2 semanas

---

### **Fase 3: Sistema de Configuración** ⭐ *PRIORIDAD MEDIA*

#### **Objetivo**
Permitir configuración personalizada de reglas de sensibilidad y patrones.

#### **Tareas**
1. **Crear sistema de configuración**
   ```
   cryptic/config/
   ├── __init__.py
   ├── settings.py
   └── rules.py
   ```

2. **Formatos de configuración**
   - YAML para configuración general
   - JSON para reglas específicas
   - Variables de entorno

3. **Configuraciones personalizables**
   - Niveles de sensibilidad por tipo de dato
   - Patrones personalizados
   - Exclusiones y whitelist
   - Configuración por proyecto

#### **Ejemplo de Configuración**
```yaml
# cryptic.config.yaml
sensitivity_rules:
  email: HIGH
  rut: CRITICAL
  phone: MEDIUM
  
custom_patterns:
  - name: "Employee ID"
    pattern: "EMP[0-9]{6}"
    sensitivity: MEDIUM
    
exclusions:
  - "test@example.com"
  - "11.111.111-1"  # RUT de prueba
```

#### **Criterios de Éxito**
- [ ] Configuración vía archivos YAML/JSON
- [ ] Override via variables de entorno
- [ ] Validación de configuraciones
- [ ] Documentación de opciones

#### **Estimación**: 1-2 semanas

---

### **Fase 4: Sugerencias de Encriptación** ⭐ *PRIORIDAD MEDIA*

#### **Objetivo**
Proporcionar recomendaciones específicas de encriptación para datos sensibles detectados.

#### **Tareas**
1. **Motor de recomendaciones**
   ```
   cryptic/core/recommender.py
   ```
   - Mapeo: tipo_dato -> algoritmo_recomendado
   - Consideraciones de contexto
   - Best practices por tipo

2. **Base de conocimiento**
   - Algoritmos apropiados por tipo de dato
   - Consideraciones de compliance (GDPR, etc.)
   - Ejemplos de implementación

3. **Integración con analyzer**
   - Recomendaciones contextuales
   - Código de ejemplo
   - Links a documentación

#### **Ejemplos de Recomendaciones**
- Email → "Use hash SHA-256 with salt for pseudonymization"
- Password → "Use bcrypt with cost factor 12+"  
- Credit Card → "Use format-preserving encryption (FPE)"
- RUT → "Use HMAC-SHA256 for reversible pseudonymization"

#### **Criterios de Éxito**
- [ ] Recomendaciones específicas por tipo de dato
- [ ] Considera contexto de uso
- [ ] Incluye ejemplos de código
- [ ] Referencias a estándares

#### **Estimación**: 1-2 semanas

---

### **Fase 5: Detección de Datos Cifrados** ⭐ *PRIORIDAD BAJA*

#### **Objetivo**
Detectar si los datos están cifrados (no solo hasheados) usando algoritmos como AES, RSA, etc.

#### **Tareas**
1. **Patrones de cifrado**
   - Base64 con características específicas
   - Longitudes típicas de cifrados
   - Entropía de datos cifrados

2. **Heurísticas de detección**
   - Análisis de entropía
   - Patrones de padding
   - Detección de formato PEM

3. **Diferenciación hash vs cifrado**
   - Clasificación más precisa
   - Confianza en identificación

#### **Criterios de Éxito**
- [ ] Distingue entre hash y cifrado
- [ ] Detecta AES, RSA, etc.
- [ ] Análisis de entropía efectivo
- [ ] Baja tasa de falsos positivos

#### **Estimación**: 2-3 semanas

---

### **Fase 6: Integración Avanzada con Testing** ⭐ *PRIORIDAD BAJA*

#### **Objetivo**
Facilitar integración con frameworks de testing y CI/CD.

#### **Tareas**
1. **Plugin para pytest**
   ```python
   @pytest.mark.cryptic_verify
   def test_user_data():
       assert is_properly_encrypted(user.email)
   ```

2. **Integración CI/CD**
   - GitHub Actions
   - Pre-commit hooks
   - Reportes automáticos

3. **Métricas de seguridad**
   - Porcentaje de datos protegidos
   - Trending de protección
   - Alertas automáticas

#### **Criterios de Éxito**
- [ ] Plugin pytest funcional
- [ ] Integración GitHub Actions
- [ ] Reportes automáticos
- [ ] Dashboard de métricas

#### **Estimación**: 2-3 semanas

---

## 📊 **Cronograma Estimado**

| Fase | Duración | Inicio Estimado | Funcionalidad Clave |
|------|----------|----------------|---------------------|
| **Fase 1** | 2-3 semanas | Inmediato | Detección datos sensibles |
| **Fase 2** | 1-2 semanas | Semana 4 | CLI completo |
| **Fase 3** | 1-2 semanas | Semana 6 | Configuración |
| **Fase 4** | 1-2 semanas | Semana 8 | Recomendaciones |
| **Fase 5** | 2-3 semanas | Semana 10 | Detección cifrados |
| **Fase 6** | 2-3 semanas | Semana 13 | Testing avanzado |

**Total estimado: 3-4 meses de desarrollo**

---

## 🎯 **Priorización de Desarrollo**

### **Sprint 1-2 (Immediate)**
- ✅ **COMPLETADO**: Refactorización modular
- 🚧 **Siguiente**: Detección de datos sensibles básica

### **Sprint 3-4 (Short term)**  
- CLI básico
- Configuración simple

### **Sprint 5-6 (Medium term)**
- Recomendaciones
- Configuración avanzada  

### **Sprint 7+ (Long term)**
- Detección cifrados
- Integración testing

---

## 📋 **Criterios de Definición de "Terminado"**

Para cada fase, se considera completada cuando:

- [ ] **Funcionalidad**: Todos los casos de uso funcionan
- [ ] **Testing**: Cobertura >90% para nuevos módulos
- [ ] **Documentación**: README actualizado
- [ ] **Compatibilidad**: API anterior sigue funcionando
- [ ] **Performance**: No degradación de rendimiento
- [ ] **CI/CD**: Todos los tests pasan

---

## 🔄 **Proceso de Revisión**

**Revisión mensual**: Evaluar progreso y ajustar prioridades
**Revisión post-fase**: Validar criterios de éxito
**Revisión final**: Alineación con objetivos del README

---

*Este roadmap se actualizará según el progreso y feedback recibido.*
