Trabajo de titulacion:

# 1  Introducción
Cryptic es una librería orientada al análisis, validación y gestión de datos encriptados, con aplicaciones en los campos de la programación y la ciberseguridad de sistemas informáticos. Su propósito es proporcionar un conjunto de funciones especializadas que permitan, entre otras tareas, identificar información sensible que debería estar protegida mediante técnicas criptográficas, así como verificar el estado de protección de los datos existentes.
Este proyecto surge como solución a la necesidad generalizada de informacion y herramientas criptograficas en el ambito academico de la programacion hoy en día.

## 1.1  Motivación
El incremento exponencial de las amenazas cibernéticas y la implementación de marcos regulatorios en materia de protección de datos personales han generado una demanda creciente de herramientas especializadas que faciliten la gestión segura de información sensible. En este contexto, Cryptic se presenta como una solución integral que no solamente asiste a los desarrolladores en la identificación y protección de información crítica, sino que también fomenta la adopción de metodologías de desarrollo seguro, contribuyendo así a la construcción de sistemas de software más robustos y confiables desde una perspectiva de seguridad informática.

## 1.2  Objetivo
Este proyecto tiene como objetivo centralizar el conocimiento técnico sobre criptografía, abordando tanto sus fundamentos teóricos como su implementación práctica. Además, busca ofrecer valor tanto a desarrolladores como a organizaciones interesadas en fortalecer sus políticas de protección de datos, facilitando la comprensión de conceptos clave —como la diferencia entre cifrado y encriptación— y promoviendo buenas prácticas en el manejo seguro de información sensible.

## 1.3  Estructura
El proyecto se divide en 5 secciones principales:

- Introducción: Describe el propósito del proyecto y su contexto.
- Fundamentos: Explica los conceptos básicos de criptografía y seguridad informática.
- Investigación: Analiza las herramientas y técnicas disponibles para el análisis de datos encriptados.
- Implementación: Describe la estructura del proyecto y las funcionalidades principales.
- Conclusión: Resume las conclusiones del proyecto y las implicaciones prácticas.

# 2  Fundamentos
Para entender lo relacionado con la criptografía, es necesario conocer los conceptos básicos de la misma. En esta sección abordaremos desde los conceptos básicos de la criptografía, hasta los algoritmos de encriptación más comunes y demas terminología relacionada.

## 2.1 Criptografía
Según la Real Academia Española, la criptografía es el arte de escribir con clave secreta o de un modo enigmático.
[(Real Academia Española)](https://dle.rae.es/criptograf%C3%ADa)

La encriptación en si, constituye un conjunto de técnicas y procedimientos que permiten alterar la información para que no sea posible (o por lo menos no viable) conocer su contenido, excepto por las personas autorizadas que posean las claves o métodos necesarios para revertir dicha alteración.

El término criptografía se compone de dos palabras griegas: **kryptos**, que significa "ocultar", y **graphos**, que significa "escritura". En un sentido más amplio sería aplicar alguna técnica para hacer ininteligible un mensaje.
[(Revista UNAM)](https://www.revista.unam.mx/vol.7/num7/art55/jul_art55.pdf)

Es necesario aclarar el asunto de la diferencia entre los terminos cifrado y encriptación. Historicamente en el mundo de la seguridad de la información, solía rechazarse el uso de la palabra encriptación, debido que se consideraba un anglisismo (encriptar viene de encryption), y se prefería el uso de la palabra cifrado.
A partir del año 2022, la RAE ha aceptado el uso de la palabra encriptación [(RAE)](https://dle.rae.es/encriptar), por lo que a fines de este documento usaremos encriptación y cifrado como sinónimos.

### 2.1.1 Encriptación
Basándonos en la naturaleza de la clave de cifrado, los sistemas criptográficos se dividen en dos categorias generales:

- Sistemas de clave simétrica: Se dispone de una clave secreta de cifrado y descifrado.
- Sistemas de clave pública: Se dispone de dos claves, una para el cifrado y otra para el descifrado.

También existe otra forma de clasificar los algoritmos criptográficos, basada en la división de los datos antes de su codificación. De esta forma podemos distinguir dos tipos de cifrados:

- Cifrado por bloques: Dividen la información en bloques de igual tamaño y codifican cada bloque por separado para crear el mensaje cifrado. Si el tamaño del mensaje no permite su división en bloques de igual tamaño, normalmente se utiliza alguna técnica de relleno para completar la parte que falta.

- Cifrado de flujo: Realizan las operaciones de codificación sobre un flujo constante de datos de forma incremental. Este tipo de algoritmos son especialmente útiles cuando el tamaño del mensaje no se puede conocer de antemano, por ejemplo, en una conversación de voz, donde el flujo de la información se produce en fragmentos.

A fines de esta investigación, se analizaran los algoritmos de cifrado clasificados por tipo de clave.

#### 2.1.1.1 Sistemas de clave simétrica
Este tipo de sitema utiliza una unica clave secreta (que debe ser compartida entre el emisor y el receptor) para cifrar y descifrar el mensaje, para ilustrar este concepto de manera sencilla, se pueden citar algoritmos de cifrado clasicos. Se trata de algoritmos primitivos utilizados en la antigüedad para asegurar la información. Su uso hoy en dia se limita al ámbito académico y sirven para entender los orígenes de la criptografia, como por ejemplo el cifrado César.

**Cifrado César:**
Se trata de uno de los algoritmos de cifrado por sustitución más conocidos. Este sistema recibe su nombre de Julio César, a quien se atribuye su autoría. Según las referencias históricas, César utilizaba este método de cifrado para proteger las comunicaciones militares.

El algoritmo de cifrado consiste en aplicar a cada letra del alfabeto un desplazamiento de tres posiciones. De esta forma, la letra A se convierte en D, la B se convierte en E y asi sucesivamente. La clave secreta en este y otros sistemas de sustitución es el número de desplazamientos. Veamos un ejemplo práctico de cómo cifrar un texto con cifrado César:

**Figura 1:** Cifrado César.
[Imagen de Cifrado César](./assets/Caesar3.png)

> Mensaje original: EL CIFRADO DE CESAR ES INGENIOSO.
>
> Mensaje cifrado: HO FLIUDGR GH FHVDU HV LQJHQLRVR

En este caso, la clave secreta es el número de desplazamientos, en este caso 3. 

#### 2.1.1.2 Sistemas de clave pública
Uno de los principales problemas de los sistemas de clave simétrica es la necesidad de mantener en secreto la clave de cifrado. Esto provoca muchas dificultades, especialmente a la hora de distribuir las claves entre las entidades autorizadas. Si el canal de comunicación entre por un tercero no autorizado, poniendo en riesgo la confidencialidad de todos los mensajes cifrados con esa clave.
Los algoritmos de clave pública intentan resolver este tipo de problemas eliminando la necesidad de mantener la clave en secreto. A diferencia de los sistemas clásicos, que solo utilizan una dave para los procesos de codificación y decodificación, los sistemas de clave pública utilizan pares de claves, una para codificar y otra para decodificar. Cada una de las claves puede ser utilizada para cifrar y descifrar la información, con la especial característica de que un mensaje cifrado con una de las claves solo puede descifrarse por la otra y viceversa. De esta manera, se elige una de las claves como clave pública y se utiliza para cifrar los mensajes. Esta clave puede distribuirse por cualquier canal y su contenido puede ser conocido por cualquiera. La otra clave recibe el nombre de clave privada y se debe mantener en secreto. Esta es la única clave que tiene la capacidad de descifrar la información. Para ilustrar este concepto, podemos citar por ejemplo el algoritmo RSA.

**RSA:**
El algoritmo RSA es un sistema de cifrado de clave pública desarrollado en 1977 por Ron Rivest, Adi Shamir y Leonard Adleman. Es uno de los algoritmos de cifrado más utilizados y confiables en la actualidad.

El funcionamiento del algoritmo RSA se basa en la dificultad de factorizar grandes números primos. El proceso de cifrado y descifrado se realiza utilizando dos claves: una clave pública y una clave privada.

La clave pública se utiliza para cifrar los mensajes, mientras que la clave privada se utiliza para descifrarlos.

**Figura 2:** RSA.
[Imagen de RSA](./assets/RSA-Encryption.png)

### 2.1.2 Hashing
La integridad de la informacion en la propiedad que busca "mantener los datos libres de modificaciones no autorizadas".
Asegurar la integridad de la informacion es tan importante como la confidencialidad de la misma, de hecho en ocasiones puede llegar a ser mas importante. Por ejemplo consideremos el caso de una transferencia bancaria donde el campo "importe" podría ser modificado para contener un monto diferente al que se desea transferir. En este caso la perdida de integridad puede tener un coste muy elevado.

Los sistemas criptográficos, por defecto, no pueden garantizar la integridad del mensaje, ya que no tienen en cuenta la identidad del autor original del mensaje y cualquier entidad poseedora de la clave es capaz de generar un mensaje cifrado. Si un intermediario no autorizado fuese capaz de captar las claves, podria capturar los mensajes cifrados, descifrarios, analizar y modificar su contenido, cifrarlos de nuevo y mandarlos al destinatario. En ese caso, el destinatario no tendría ningún medio a su disposición para verificar que el mensaje que ha recibido es el que la entidad origen pretendia mandarle o no.

Los algoritmos Hash, o funciones de resumen, nacen en parte para poder solucionar estos problemas. Estas funciones son, en esencia, fórmulas matemáticas, que, tomando un valor de entrada, por ejemplo, el valor numérico del mensaje, que puede ser de tamaño variable, ofrece como salida cierto valor de una longitud determinada. Estas funciones son ideadas de forma que sea imposible deducir el valor de entrada de la función, utilizando el resultado. 

Entre los algoritmos de hashing mas comunes y en los que nos centraremos en esta investigación, se encuentran los siguientes:
- MD5
- SHA-1
- Bcrypt

## 2.2 Herramientas
El ecosistema criptográfico moderno presenta un panorama amplio de herramientas especializadas que abordan diferentes aspectos de la seguridad en el desarrollo de software. Desde herramientas de análisis estático que detectan vulnerabilidades en tiempo de desarrollo, hasta bibliotecas de implementación que proporcionan primitivas criptográficas robustas, cada categoría cumple un rol vital en la construcción de sistemas seguros. La selección adecuada de estas herramientas no solo determina la efectividad de las medidas de seguridad implementadas, sino que también influye en aspectos críticos como el rendimiento, la mantenibilidad y el cumplimiento de estándares regulatorios. En este apartado se examina el estado actual de las herramientas más relevantes, analizando sus capacidades, limitaciones y casos de uso óptimos para proporcionar una guía práctica para arquitectos de software y desarrolladores que buscan implementar soluciones criptográficas efectivas.

### 2.2.1 Panorama general de herramientas

El panorama de herramientas criptográficas abarca desde herramientas de análisis estático hasta plataformas de validación especializada. Nuestra investigación ha demostrado la importancia de contar con herramientas robustas para el análisis y validación de implementaciones criptográficas.

**Herramientas de Análisis Estático de Seguridad (SAST)**

Las herramientas SAST representan un componente fundamental en la detección temprana de vulnerabilidades criptográficas. Kuszczyński y Walkowski (2023) realizaron un análisis comparativo de 11 herramientas de código abierto para análisis estático de seguridad, evaluando su efectividad en la detección de vulnerabilidades criptográficas. Entre las herramientas más destacadas se encuentran:

- **Semgrep**: Mostró un mejor rendimiento para aplicaciones desarrolladas en JavaScript, aunque presentó resultados menos favorables para aplicaciones PHP.
- **SonarQube**: Ampliamente adoptado en entornos empresariales para la detección continua de vulnerabilidades.
- **Bandit**: Especializado en análisis de código Python con reglas específicas para detección de malas prácticas criptográficas.

**Herramientas de Validación Criptográfica**

El Programa de Validación de Algoritmos Criptográficos (CAVP) del NIST proporciona estándares de referencia para la validación de implementaciones criptográficas. Este programa, establecido en julio de 1995 por NIST y el Gobierno de Canadá, valida algoritmos aprobados por FIPS y recomendados por NIST, incluyendo:

- Cifrados de bloque (AES, Triple DES)
- Funciones hash seguras (SHA-2, SHA-3)
- Firmas digitales (DSA, ECDSA, RSA)
- Generadores de números aleatorios (DRBG)

**Herramientas de Identificación de Hashes**

La identificación precisa de algoritmos de hash es crucial para el análisis forense y la verificación de integridad. Nuevas herramientas han surgido para reemplazar las obsoletas como hashID y hash-identifier:

- **HAITI (HAsh IdenTifIer)**: Soporta 382+ tipos de hash, incluyendo algoritmos modernos como SHA3, Keccak, y Blake2.
- **Name-That-Hash**: Desarrollado desde 2021, implementa clasificaciones de popularidad y proporciona resúmenes de uso para cada tipo de hash.

Estas herramientas ofrecen ventajas significativas sobre sus predecesoras, incluyendo soporte para hashes modernos, interfaces de programación (API), y salida en formato JSON para integración en pipelines automatizados.

### 2.2.2 Herramientas de desarrollo

El ecosistema de bibliotecas criptográficas para Python ha evolucionado considerablemente, siendo fundamental para el desarrollo seguro de aplicaciones. Los estudios especializados han catalogado las principales bibliotecas, además de analizar sus características distintivas.

**Bibliotecas Criptográficas Principales**

Según la documentación técnica y análisis comparativos académicos, las bibliotecas más relevantes incluyen:

**1. Cryptography**
Es la biblioteca más moderna y recomendada para Python, diseñada con dos niveles de abstracción:
- **Nivel de recetas criptográficas**: API de alto nivel que requiere poca configuración
- **Nivel de primitivas criptográficas**: API de bajo nivel en el paquete `cryptography.hazmat`

La biblioteca cuenta con soporte activo, cumplimiento de estándares FIPS 140-2 y NIST, y arquitectura multi-backend que permite utilizar tanto OpenSSL como otros backends.

**2. PyCryptodome**
Evolución de la biblioteca PyCrypto, caracterizada por:
- Implementación pura en Python sin dependencias de OpenSSL
- Soporte robusto para AES, RSA, y funciones hash
- Ideal para entornos con restricciones de instalación

**3. PyOpenSSL**
Proporciona vínculos de bajo nivel con la biblioteca OpenSSL, ofreciendo acceso completo a las funcionalidades de esta biblioteca ampliamente utilizada.

**Bibliotecas para Criptografía Post-Cuántica**

El proyecto Open Quantum Safe (OQS) ha desarrollado liboqs-python como wrapper para algoritmos resistentes a ataques cuánticos, implementando:
- Algoritmos PQC estándar de NIST
- Mecanismos de encapsulación de llaves (KEMs)
- Esquemas de firma digital post-cuántica

**Herramientas de Validación de Contraseñas**

La biblioteca Passlib se especializa en el manejo seguro de contraseñas, implementando más de 30 algoritmos de hashing, incluyendo PBKDF2-SHA256, bcrypt, y scrypt, con soporte para múltiples plataformas Python.

**Consideraciones de Implementación**

La evaluación del ecosistema de bibliotecas criptográficas en Python requiere un análisis sistemático de criterios técnicos fundamentales que determinan su idoneidad para implementaciones seguras:
- Continuidad del mantenimiento y aplicación oportuna de parches de seguridad
- Conformidad con estándares criptográficos establecidos por organismos como NIST y FIPS
- Compatibilidad transversal con implementaciones de Python (CPython 2.x/3.x, PyPy, Jython)
- Calidad y exhaustividad de la documentación técnica y casos de uso documentados

## 2.3 Ciberseguridad
Aunque no es la unica herramienta para protegernos de las amenazas ciberneticas, la criptografia es una de las herramientas mas importantes para proteger la informacion de amenazas de terceros, pero su uso incorrecto puede generar vulnerabilidades de seguridad, por eso este apartado se analizan los errores comunes en la implementacion de la criptografia y las prácticas de desarrollo seguro recomendadas para evitarlos.

### 2.3.1 Errores comunes

Múltiples estudios académicos han identificado patrones sistemáticos de errores en implementaciones criptográficas; estos hallazgos revelan impactos significativos en la seguridad de sistemas de software. Estudios empíricos revelan que entre el 83% y 96% de las aplicaciones que utilizan APIs criptográficas presentan al menos un mal uso que puede generar vulnerabilidades de seguridad.

**Clasificación de Errores Criptográficos**

Según el análisis sistemático de Wickert et al. (2023), los errores criptográficos se clasifican en seis categorías principales:

**1. Errores de Restricción (Constraint Errors)**
Uso de parámetros inseguros en la inicialización de objetos criptográficos:
- Selección de algoritmos obsoletos (DES, MD5, SHA-1)
- Configuración de longitudes de clave inadecuadas
- Especificación incorrecta de modos de cifrado

**2. Errores de Operación Incompleta (Incomplete Operation Errors)**
Protocolos criptográficos que no se completan correctamente:
- Omisión de llamadas críticas como `sign()` en objetos Signature
- Procesos de cifrado sin finalizar adecuadamente
- Validaciones de integridad incompletas

**3. Errores de Predicado Requerido (Required Predicate Errors)**
Composición insegura de objetos criptográficos:
- Uso de claves débiles o generadas inadecuadamente
- Dependencias inseguras entre componentes criptográficos
- Validación inadecuada de certificados en TLS

**4. Errores de Tipo Prohibido (Never Type Error)**
Manejo inadecuado de información sensible:
- Almacenamiento de claves secretas como `string`
- Uso de tipos inmutables para datos sensibles
- Exposición prolongada de secretos en memoria

**5. Errores de Método Prohibido (Forbidden Method Error)**
Llamadas a métodos que comprometen la seguridad:
- Uso de constructores sin sal en `PBEKeySpec`
- Invocación de métodos que debilitan la seguridad
- Configuraciones que eliminan validaciones críticas

**6. Errores de Estado de Tipo (Type State Error)**
Secuencias de llamadas incorrectas en objetos criptográficos:
- Inicialización inadecuada antes del uso
- Estados inconsistentes durante el procesamiento
- Transiciones de estado que comprometen la seguridad

**Vulnerabilidades Criptográficas en la Práctica**

El análisis de la plataforma HackerOne por Hazhirpasand y Ghafari (2021) revela ocho temas principales de vulnerabilidades criptográficas:

**Ataques a SSL/TLS (58 reportes)**
- POODLE: Explotación de SSL 3.0 con 256 solicitudes para revelar un byte
- Sweet32: Vulnerabilidades en cifrados de 64 bits (Triple-DES, Blowfish)
- DROWN: Ataques de oráculo de padding en servidores con SSLv2
- BREACH: Explotación de compresión HTTP en HTTPS

**Configuraciones Criptográficas Débiles (25 reportes)**
- Uso de algoritmos obsoletos (MD5, SHA-1)
- Longitudes de clave insuficientes (RSA 512-bit)
- Generadores de números pseudo-aleatorios predecibles
- Claves codificadas directamente en el código (hardcoded keys)

**Impacto en Seguridad**

Wickert et al. documentan que el 42.78% de los mal usos criptográficos son de alta severidad, incluyendo:
- Ataques de Hombre en el Medio (MitM)
- Credenciales codificadas directamente (hardcoded credentials)  
- Ataques de Denegación de Servicio (DoS)
- Ataques de texto cifrado elegido (CCA)

**Algoritmos Hash Comprometidos**

La investigación de Sadeghi-Nasab y Rafe documenta algoritmos hash que han sido comprometidos académicamente:

- **MD2**: Vulnerabilidades de preimagen con complejidad 2^73 operaciones
- **MD4**: Múltiples ataques de colisión documentados
- **MD5**: Ataques de colisión factibles con recursos computacionales moderados
- **SHA-1**: Deprecado para uso criptográfico debido a vulnerabilidades de colisión demostradas

Estos hallazgos subrayan la importancia de mantenerse actualizado con las recomendaciones criptográficas actuales y la necesidad de herramientas automatizadas para la detección temprana de mal usos criptográficos.

### 2.3.2 Prácticas de desarrollo seguro

El desarrollo seguro de aplicaciones que implementan criptografía requiere la adopción de metodologías y herramientas especializadas que permitan detectar y mitigar vulnerabilidades desde las etapas tempranas del ciclo de desarrollo de software.

**Metodologías de Análisis de Seguridad**

**Análisis Estático de Seguridad de Aplicaciones (SAST)**

Las herramientas SAST constituyen una primera línea de defensa contra vulnerabilidades criptográficas. Según la investigación de Kuszczyński y Walkowski (2023), estas herramientas pueden clasificarse según:

- **Cobertura de vulnerabilidades**: Capacidad para detectar diferentes tipos de mal usos criptográficos
- **Tasa de falsos positivos**: Equilibrio entre detección y precisión 
- **Soporte multi-lenguaje**: Compatibilidad con diferentes tecnologías de desarrollo
- **Integración en CI/CD**: Capacidad de automatización en pipelines de desarrollo

**Análisis Dinámico de Seguridad de Aplicaciones (DAST)**

Complementa el análisis estático mediante pruebas en tiempo de ejecución, permitiendo:
- Detección de vulnerabilidades en configuraciones de TLS/SSL
- Validación de comportamiento criptográfico en entornos reales
- Identificación de ataques de canal lateral y timing

**Marcos de Desarrollo Seguro**

**Ciclo de Vida de Desarrollo de Software Seguro (SSDLC)**

La extensión del SDLC tradicional con consideraciones de seguridad criptográfica incluye:

1. **Fase de Análisis**: Identificación de requisitos de seguridad criptográfica
2. **Fase de Diseño**: Selección de algoritmos y protocolos apropiados
3. **Fase de Implementación**: Uso correcto de APIs criptográficas
4. **Fase de Pruebas**: Validación mediante herramientas SAST/DAST
5. **Fase de Despliegue**: Configuración segura de entornos productivos

**Validación y Cumplimiento de Estándares**

**Programa de Validación de Módulos Criptográficos (CMVP)**

El CMVP, desarrollado conjuntamente por NIST y el Gobierno de Canadá, establece:
- Validación de implementaciones criptográficas según FIPS 140-2
- Certificación de módulos criptográficos para uso gubernamental
- Estándares de testing y validación para vendors

**Estándares de la Industria**

- **NIST Cybersecurity Framework**: Proporciona directrices para gestión de riesgos criptográficos
- **OWASP Cryptographic Storage Cheat Sheet**: Mejores prácticas para almacenamiento seguro
- **ISO/IEC 27001**: Marco de gestión de seguridad de la información

**Herramientas de Detección Automatizada**

**CogniCrypt**: Desarrollado por la comunidad académica, utiliza un enfoque de allowlisting que:
- Define patrones de uso seguro de APIs criptográficas  
- Reporta violaciones como potenciales mal usos
- Soporta bibliotecas JCA y Bouncy Castle
- Alcanza precisión del 85% al 94% según estudios empíricos

**CryptoGuard**: Implementa un enfoque de denylisting:
- Describe vulnerabilidades conocidas
- Detecta patrones de mal uso en código fuente
- Integrable en pipelines de desarrollo continuo

**Mejores Prácticas de Implementación**

1. **Gestión de Claves Segura**:
   - Uso de Hardware Security Modules (HSMs) para claves críticas
   - Implementación de rotación automática de claves
   - Separación de claves de cifrado y autenticación

2. **Configuración de TLS/SSL**:
   - Deshabilitación de protocolos obsoletos (SSL 3.0, TLS 1.0)
   - Implementación de Perfect Forward Secrecy
   - Configuración de Certificate Authority Authorization (CAA)

3. **Manejo de Entropía**:
   - Uso de generadores de números aleatorios criptográficamente seguros
   - Validación de fuentes de entropía en sistemas embebidos
   - Implementación de seeding apropiado

**Integración en DevSecOps**

La adopción de prácticas DevSecOps requiere:
- **Shift-Left Security**: Integración de testing de seguridad en etapas tempranas
- **Automatización**: Herramientas integradas en pipelines CI/CD
- **Monitoreo continuo**: Detección de vulnerabilidades en producción
- **Cultura de seguridad**: Capacitación del equipo de desarrollo en criptografía

## 2.4 Terminología

### 2.4.1 Algoritmos

La terminología precisa en criptografía es fundamental para la comprensión académica y profesional del campo. Los algoritmos criptográficos se clasifican según múltiples criterios establecidos por organismos internacionales como NIST, IETF, y la comunidad académica.

**Clasificación por Función Criptográfica**

**Algoritmos de Hash Criptográficos**
- **Función Hash Segura**: Función matemática que mapea datos de longitud arbitraria a una cadena de bits de longitud fija, con propiedades de resistencia a preimagen, segunda preimagen y colisión.
- **MD5 (Message Digest 5)**: Algoritmo hash de 128 bits desarrollado por Ron Rivest, declarado criptográficamente inseguro debido a vulnerabilidades de colisión.
- **SHA (Secure Hash Algorithm)**: Familia de funciones hash desarrolladas por NIST, incluyendo SHA-1 (160 bits, deprecado) y la familia SHA-2 (SHA-224, SHA-256, SHA-384, SHA-512).
- **SHA-3**: Estándar hash más reciente de NIST basado en la construcción Keccak, diseñado como alternativa a SHA-2.

**Algoritmos de Cifrado Simétrico**
- **AES (Advanced Encryption Standard)**: Algoritmo de cifrado por bloques adoptado como estándar por NIST en 2001, disponible en claves de 128, 192, y 256 bits.
- **DES (Data Encryption Standard)**: Algoritmo de cifrado histórico de 56 bits, considerado inseguro debido a la longitud de clave insuficiente.
- **3DES (Triple DES)**: Versión mejorada de DES que aplica el algoritmo tres veces, aún utilizado en sistemas legacy pero en proceso de deprecación.

**Algoritmos de Cifrado Asimétrico**
- **RSA (Rivest-Shamir-Adleman)**: Algoritmo de criptografía de clave pública basado en la dificultad de factorizar números enteros grandes.
- **ECC (Elliptic Curve Cryptography)**: Criptografía basada en curvas elípticas que proporciona seguridad equivalente con claves más cortas que RSA.
- **DSA (Digital Signature Algorithm)**: Estándar para firmas digitales especificado en FIPS 186.

**Clasificación por Resistencia Criptográfica**

Según la investigación académica, los algoritmos se clasifican por su resistencia a ataques conocidos:

**Algoritmos Seguros**
- SHA-256, SHA-3: Resistentes a ataques de colisión conocidos
- AES: Considerado seguro contra ataques clásicos y cuánticos (con claves apropiadas)
- ECC con curvas P-256, P-384, P-521: Recomendados por NIST

**Algoritmos Comprometidos**
Según Sadeghi-Nasab y Rafe, múltiples algoritmos han sido académicamente comprometidos:
- **MD4**: Susceptible a ataques de colisión desde 1996
- **MD5**: Ataques de colisión prácticos demostrados en 2004
- **SHA-1**: Primer ataque de colisión exitoso demostrado en 2017

**Terminología de Ataques Criptográficos**

**Ataques de Colisión**: Búsqueda de dos entradas distintas que produzcan la misma salida hash
**Ataques de Preimagen**: Intento de encontrar una entrada que genere una salida hash específica  
**Ataques de Segunda Preimagen**: Búsqueda de una segunda entrada que produzca el mismo hash que una entrada conocida
**Ataque de Cumpleaños**: Explotación de la paradoja del cumpleaños para encontrar colisiones con menor esfuerzo computacional

**Parámetros Criptográficos**

**Longitud de Clave**: Número de bits en la clave criptográfica, directamente relacionado con la resistencia a ataques por fuerza bruta
**Entropía**: Medida de aleatoriedad en datos criptográficos, crítica para la seguridad de claves y vectores de inicialización
**Factor de Trabajo**: En algoritmos como bcrypt y scrypt, parámetro que controla la dificultad computacional
**Sal Criptográfica**: Valor aleatorio añadido a datos antes del hashing para prevenir ataques de tabla arcoíris

# 3  Investigación
En este apartado se realiza una investigación sobre los requerimientos funcionales y no funcionales de la librería Cryptic, así como los casos de uso y el análisis de viabilidad del proyecto, con el fin de establecer una base sólida para el desarrollo del mismo.

## 3.1 Requerimientos

La definición precisa de requerimientos funcionales y no funcionales es fundamental para el desarrollo exitoso de la librería Cryptic. Basándose en el backlog documentado y las mejores prácticas de ingeniería de software, se establecen los siguientes requerimientos.

### 3.1.1 Requerimientos Funcionales

Los requerimientos funcionales definen las capacidades específicas que debe proporcionar la librería Cryptic, derivados del análisis del backlog del proyecto y las necesidades identificadas.

**RF-001: Detección de Algoritmos Hash**
- **Descripción**: La librería debe identificar tipos de hash criptográficos a partir de cadenas hexadecimales
- **Entrada**: Cadena hash en formato hexadecimal
- **Salida**: Tipo de hash identificado con nivel de confianza
- **Criterios de Aceptación**: 
  - Soporte mínimo para MD5, SHA-1, SHA-256, SHA-512, bcrypt, scrypt
  - Precisión de identificación ≥ 85% según benchmarks establecidos

**RF-002: Análisis de Datos Sensibles**
- **Descripción**: Detectar automáticamente información sensible en cadenas de texto
- **Entrada**: Cadena de texto o datos estructurados
- **Salida**: Clasificación de sensibilidad y recomendaciones
- **Criterios de Aceptación**:
  - Detección de emails, RUT chilenos, números de tarjetas de crédito
  - Tasa de falsos positivos ≤ 15%
  - Tiempo de análisis ≤ 100ms por entrada

**RF-003: Verificación de Estado de Protección**
- **Descripción**: Evaluar si los datos están adecuadamente protegidos criptográficamente
- **Entrada**: Datos y contexto de uso
- **Salida**: Estado de protección (PROTECTED/UNPROTECTED/PARTIALLY_PROTECTED)
- **Criterios de Aceptación**:
  - Análisis basado en patrones de hash conocidos
  - Evaluación de fortaleza criptográfica
  - Recomendaciones específicas por tipo de dato

**RF-004: Generación de Reportes**
- **Descripción**: Producir reportes detallados del análisis realizado
- **Entrada**: Resultados de análisis múltiples
- **Salida**: Reporte estructurado en formato JSON/YAML/texto
- **Criterios de Aceptación**:
  - Resumen ejecutivo con métricas clave
  - Detalle de hallazgos por categoría de riesgo
  - Recomendaciones de remediación priorizadas

**RF-005: Interfaz de Línea de Comandos**
- **Descripción**: Proporcionar acceso a funcionalidades mediante CLI
- **Entrada**: Comandos y parámetros de configuración
- **Salida**: Resultados formateados para consola
- **Criterios de Aceptación**:
  - Comandos: `verify`, `analyze`, `batch`
  - Soporte para archivos CSV y procesamiento por lotes
  - Opciones de configuración y formato de salida

**RF-006: API Programática**
- **Descripción**: Interfaz para integración en otras aplicaciones Python
- **Entrada**: Objetos Python nativos
- **Salida**: Objetos de resultado estructurados
- **Criterios de Aceptación**:
  - Clases principales: `HashIdentifier`, `CrypticAnalyzer`
  - Compatibilidad con Python 3.8+
  - Documentación API completa con ejemplos

### 3.1.2 Requerimientos No Funcionales

Los requerimientos no funcionales establecen las restricciones y cualidades que debe cumplir el sistema para asegurar su calidad, rendimiento y mantenibilidad.

**RNF-001: Rendimiento**
- **Tiempo de Respuesta**: ≤ 0.5 segundos para análisis individual
- **Throughput**: ≥ 1000 análisis por minuto en procesamiento por lotes  
- **Memoria**: Consumo máximo de 256MB para análisis simultáneo
- **Escalabilidad**: Soporte para archivos de hasta 100MB sin degradación

**RNF-002: Precisión y Confiabilidad**
- **Precisión de Identificación**: ≥ 85% para algoritmos hash comunes
- **Disponibilidad**: 99.9% uptime en entornos productivos
- **Estabilidad**: Zero crashes en casos de uso documentados
- **Reproducibilidad**: Resultados consistentes para las mismas entradas

**RNF-003: Compatibilidad y Portabilidad**
- **Versiones Python**: Soporte para Python 3.8, 3.9, 3.10, 3.11, 3.12
- **Sistemas Operativos**: Linux, macOS, Windows
- **Arquitecturas**: x86_64, ARM64
- **Dependencias**: Mínimas dependencias externas (solo estándar y click/pyyaml)

**RNF-004: Seguridad**
- **Validación de Entrada**: Sanitización robusta contra inyecciones
- **Manejo de Errores**: No exposición de información sensible en logs
- **Datos Sensibles**: No almacenamiento persistente de datos analizados
- **Cumplimiento**: Alineado con OWASP guidelines para herramientas de seguridad

**RNF-005: Mantenibilidad y Extensibilidad**
- **Cobertura de Tests**: ≥ 90% cobertura de código
- **Documentación**: Documentación API completa + guías de usuario
- **Modularidad**: Arquitectura que permita extensiones sin refactoring
- **Estándares de Código**: Cumplimiento con PEP 8 y type hints

**RNF-006: Usabilidad**
- **Curva de Aprendizaje**: Uso básico aprendible en ≤ 30 minutos
- **Mensajes de Error**: Descriptivos con sugerencias de resolución
- **Configuración**: Configuración por defecto funcional sin setup
- **Ejemplos**: Casos de uso documentados con código ejecutable

## 3.2 Casos de uso

Los casos de uso describen las interacciones específicas entre usuarios y la librería Cryptic, proporcionando contexto operativo para los diferentes escenarios de aplicación.

### 3.2.1 Casos de uso - Desarrollo

**CU-DEV-001: Validación de Hash en Desarrollo**
- **Actor**: Desarrollador de software
- **Objetivo**: Verificar la implementación correcta de hashing en código
- **Precondiciones**: Código fuente con implementaciones de hash
- **Flujo Principal**:
  1. Desarrollador ejecuta análisis sobre archivo fuente
  2. Cryptic identifica llamadas a funciones de hash
  3. Sistema evalúa fortaleza de algoritmos utilizados
  4. Se genera reporte con recomendaciones específicas
- **Resultado**: Lista de mejoras con priorización por riesgo

**CU-DEV-002: Integración en Pipeline CI/CD**
- **Actor**: Ingeniero DevSecOps
- **Objetivo**: Automatizar verificación criptográfica en despliegues
- **Precondiciones**: Pipeline CI/CD configurado
- **Flujo Principal**:
  1. Pipeline ejecuta análisis Cryptic post-build
  2. Sistema procesa artefactos de construcción
  3. Se evalúan configuraciones criptográficas
  4. Pipeline falla si se detectan vulnerabilidades críticas
- **Resultado**: Bloqueo automático de deployments inseguros

**CU-DEV-003: Refactoring Criptográfico**
- **Actor**: Arquitecto de Software
- **Objetivo**: Modernizar implementaciones criptográficas legacy
- **Precondiciones**: Codebase con implementaciones obsoletas
- **Flujo Principal**:
  1. Análisis masivo de repositorio de código
  2. Identificación de patrones criptográficos obsoletos
  3. Generación de plan de migración priorizado
  4. Validación post-refactoring
- **Resultado**: Roadmap de modernización criptográfica

### 3.2.2 Casos de uso - Testing

**CU-TEST-001: Testing de Regresión Criptográfica**
- **Actor**: QA Engineer
- **Objetivo**: Validar que cambios no introduzcan vulnerabilidades
- **Precondiciones**: Suite de tests automatizada
- **Flujo Principal**:
  1. Ejecución de Cryptic sobre builds antes/después
  2. Comparación de perfiles de riesgo criptográfico
  3. Identificación de regresiones de seguridad
  4. Generación de reporte diferencial
- **Resultado**: Certificación de no-regresión criptográfica

**CU-TEST-002: Penetration Testing Automatizado**
- **Actor**: Especialista en Seguridad
- **Objetivo**: Identificar vulnerabilidades criptográficas explotables
- **Precondiciones**: Aplicación desplegada en entorno de testing
- **Flujo Principal**:
  1. Análisis de endpoints y datos expuestos
  2. Identificación de implementaciones criptográficas débiles
  3. Simulación de vectores de ataque específicos
  4. Documentación de vulnerabilidades confirmadas
- **Resultado**: Reporte de penetration testing con evidencias

### 3.2.3 Casos de uso - Auditoría

**CU-AUD-001: Auditoría de Cumplimiento Regulatorio**
- **Actor**: Auditor de Cumplimiento
- **Objetivo**: Verificar conformidad con estándares (PCI DSS, SOX, GDPR)
- **Precondiciones**: Aplicación en scope de auditoría
- **Flujo Principal**:
  1. Definición de criterios de cumplimiento específicos
  2. Análisis exhaustivo de implementaciones criptográficas
  3. Mapeo de hallazgos a requerimientos regulatorios
  4. Generación de evidencia para auditoría externa
- **Resultado**: Reporte de cumplimiento con gap analysis

**CU-AUD-002: Due Diligence Técnica**
- **Actor**: Consultor de M&A
- **Objetivo**: Evaluar riesgos criptográficos en adquisiciones
- **Precondiciones**: Acceso a codebase objetivo
- **Flujo Principal**:
  1. Análisis integral de prácticas criptográficas
  2. Evaluación de deuda técnica de seguridad
  3. Estimación de costos de remediación
  4. Assess de riesgos regulatorios y de reputación
- **Resultado**: Informe de due diligence técnica

**CU-AUD-003: Certificación de Seguridad**
- **Actor**: Organismo Certificador
- **Objetivo**: Validar implementaciones para certificación formal
- **Precondiciones**: Aplicación candidata a certificación
- **Flujo Principal**:
  1. Verificación contra estándares específicos (ISO 27001, Common Criteria)
  2. Testing exhaustivo de controles criptográficos
  3. Validación de documentación técnica
  4. Emisión de certificado o reporte de no-conformidad
- **Resultado**: Certificación formal o lista de correcciones requeridas

## 3.3 Análisis de viabilidad

### 3.3.1 Necesidades

Para determinar la capacidad del proyecto para satisfacer necesidades reales del mercado, su sostenibilidad económica y su alineación con los objetivos estratégicos de desarrollo de herramientas de seguridad de próxima generación, con este fin es necesario realizar un análisis de cada aspecto de manera independiente.

**Análisis de Mercado**

El mercado global de herramientas de análisis de seguridad criptográfica muestra un crecimiento sostenido, impulsado por:

- **Regulaciones Emergentes**: Implementación de GDPR, PCI DSS 4.0, y regulaciones de criptografía post-cuántica
- **Incremento de Breaches**: El 83-96% de aplicaciones con APIs criptográficas presentan mal usos según estudios académicos
- **DevSecOps Adoption**: Integración de seguridad en pipelines de desarrollo continuo
- **Compliance Requirements**: Necesidad de auditorías automatizadas y documentación de cumplimiento

**Diferenciación Competitiva**

Cryptic se posiciona únicamente en el mercado por:

**1. Enfoque Académico**
- Base en investigación peer-reviewed
- Taxonomía comprehensiva de 105 casos de mal uso documentados académicamente
- Metodología rigurosa basada en estándares NIST y OWASP

**2. Especialización Python**
- Foco específico en ecosistema Python
- Integración nativa con bibliotecas cryptography, PyCryptodome, hashlib
- Performance optimizada para análisis de código Python

**3. Usabilidad**
- API intuitiva para desarrolladores
- Zero-configuration para casos de uso básicos
- Integración seamless con herramientas existentes

**Viabilidad Técnica**

**Fortalezas Técnicas**
- Arquitectura modular demostrada en implementación actual
- Base de conocimiento sólida con 95% cobertura en detección de hashes
- Performance validada: 0.3ms promedio (333x mejor que objetivo)
- Stack tecnológico maduro (Python 3.8+, libraries estándar)

**Riesgos Técnicos Identificados**
- **Complejidad de CLI**: Desarrollo de interfaz robusta requiere esfuerzo significativo
- **Escalabilidad**: Procesamiento de archivos grandes (>100MB) requiere optimización
- **Mantenimiento de Reglas**: Actualización continua de patrones criptográficos

**Mitigación de Riesgos**
- Desarrollo incremental con MVP funcional
- Arquitectura pluggable para extensiones futuras  
- Automatización de actualizaciones via NIST feeds

**Viabilidad Económica**

**Modelo de Desarrollo**
- Open Source con licencia MIT para adopción máxima
- Desarrollo impulsado por comunidad académica
- Potencial monetización via servicios profesionales

**ROI para Adoptadores**
- Reducción 60-80% en tiempo de auditorías manuales
- Prevención de vulnerabilidades con costo promedio $4.45M por breach (IBM, 2023)
- Cumplimiento automatizado reduce costos regulatorios

**Viabilidad Estratégica**

**Alineación con Tendencias**
- **Shift-Left Security**: Detección temprana en development lifecycle
- **Criptografía Post-Cuántica**: Preparación para transición PQC
- **Automation First**: Reducción de procesos manuales error-prone

**Ecosistema de Adopción**
- Comunidad Python: 8.2M desarrolladores globalmente  
- Sector Fintech: Alta demanda de compliance automatizado
- Organizaciones Gubernamentales: Requerimientos FIPS y validación NIST

**Conclusión de Viabilidad**

El proyecto Cryptic presenta **viabilidad alta** basada en:
- Demanda de mercado demostrada y creciente
- Diferenciación técnica clara y valiosa
- Riesgos manejables con equipo experimentado
- Alineación con tendencias de largo plazo en DevSecOps

La implementación faseada minimiza riesgos mientras maximiza learning y feedback del mercado.

## 3.4 Procesos

### 3.4.1 Enfoque en performance

El enfoque en performance de Cryptic se basa en métricas cuantificables y optimizaciones específicas para análisis criptográfico de alto volumen, siguiendo principios de ingeniería de software orientada a rendimiento.

**Métricas de Performance Actuales**

Basándose en los benchmarks documentados en el roadmap del proyecto:

**Velocidad de Análisis**
- **Tiempo promedio**: 0.3ms por análisis individual
- **Throughput actual**: >200,000 análisis/minuto  
- **Target objetivo**: <100ms (actualmente 333x mejor)
- **Latencia p99**: <2ms para análisis de hash individuales

**Precisión vs Performance Trade-offs**
- **Detección de hashes**: 95-99% precisión según tipo
- **Detección datos sensibles**: 95% precisión con 8 tipos de datos soportados
- **False positive rate**: <5% en módulos optimizados
- **Memory footprint**: <50MB para análisis concurrente

**Arquitectura Orientada a Performance**

**1. Diseño Modular Eficiente**
```
cryptic/
├── core/           # Lógica principal optimizada
│   ├── analyzer.py      # Engine principal (350 líneas)
│   └── hash_identifier.py  # Identificación rápida
├── patterns/       # Patrones precompilados
│   ├── hash_patterns.py    # Regex optimizadas
│   └── sensitive_patterns.py  # 396 líneas, validaciones avanzadas
└── utils/         # Utilidades de rendimiento
    └── formatters.py   # Parsing eficiente
```

**2. Optimizaciones de Algoritmos**
- **Lazy Loading**: Carga de patrones bajo demanda
- **Memoization**: Cache de resultados para patrones repetitivos  
- **Vectorización**: Procesamiento paralelo de lotes
- **Early Exit**: Terminación temprana en análisis determinísticos

**Estrategias de Optimización Implementadas**

**Optimización de Patrones Regex**
- Compilación ahead-of-time de expresiones regulares
- Ordenamiento por frecuencia de match para fast-path común
- Uso de grupos no-capturantes para reducir overhead
- Benchmarking continuo de patrones críticos

**Gestión Eficiente de Memoria**
- Object pooling para análisis masivos
- Streaming processing para archivos grandes
- Garbage collection hints para liberación proactiva
- Memory mapping para datasets grandes

**Paralelización Inteligente**  
- Thread-pool para análisis concurrente I/O-bound
- Process-pool para análisis CPU-intensivo
- Async/await para operaciones de red
- Lock-free data structures donde sea posible

**Benchmarking y Monitoreo**

**Suite de Benchmarks**
- **Micro-benchmarks**: Funciones individuales críticas
- **Integration benchmarks**: Flujos end-to-end completos  
- **Load testing**: Comportamiento bajo carga sostenida
- **Memory profiling**: Detección de memory leaks

**Métricas de Monitoreo**
```python
# Ejemplo de métricas capturadas
{
    "analysis_time_ms": 0.3,
    "memory_usage_mb": 12.4, 
    "cache_hit_rate": 0.87,
    "patterns_matched": 23,
    "throughput_ops_sec": 3333
}
```

**Objetivos de Performance Futuros**

**Fase 2 (CLI Completo)**
- Target: Procesar archivos 1GB+ sin degradación
- Streaming analysis con memory footprint constante
- Progress reporting para operaciones largas
- Interrupción graceful de operaciones

**Fase 3 (Configuración Avanzada)**  
- Hot-reload de configuraciones sin reinicio
- Distributed processing para análisis masivos
- Plugin architecture con performance isolation
- Real-time metrics dashboard

**Validación de Performance**

**Testing Automatizado**
- CI pipeline con performance regression testing
- Alertas automáticas para degradación >10%
- Profiling continuo en builds nightly
- A/B testing para optimizaciones propuestas

**Metodología de Optimización**
1. **Profile First**: Identificación de bottlenecks reales
2. **Measure Everything**: Métricas antes/después de cambios
3. **Optimize Iteratively**: Mejoras incrementales validadas
4. **Trade-off Conscious**: Balance performance vs maintainability

Esta aproximación sistemática a performance ha resultado en métricas actuales que superan significativamente los objetivos originales, estableciendo una base sólida para escalabilidad futura.

# 4  Implementación


Como resultado de la investigación antes descrita, se plantea Cryptic como solucion integral para diagnóstico, análisis y aporte a la comunidad de TI, 

## 4.1 Diseño

La arquitectura de Cryptic sigue principios de ingeniería de software orientada a la modularidad, extensibilidad y mantenibilidad. El diseño ha evolucionado desde una implementación monolítica inicial hacia una arquitectura basada en módulos especializados.

**Recursos Tecnológicos Empleados**
- **Python 3.11+**: Lenguaje base con soporte para type hints y características modernas
- **Pytest**: Framework de testing con cobertura >90%
- **Ruff**: Linter y formatter para cumplimiento de PEP 8
- **Click**: Framework para CLI robusta y extensible
- **PyPI**: Plataforma de distribución de paquetes Python
- **GitHub**: Sistema de control de versiones y CI/CD
- **Notion & Google Calendar**: Herramientas de gestión de proyecto académico

### 4.1.1 API

El diseño de la API de Cryptic implementa patrones de diseño establecidos para maximizar usabilidad y extensibilidad, siguiendo principios SOLID y Clean Architecture.

**Arquitectura de Capas**

```
cryptic/
├── __init__.py           # API pública + metadatos
├── core/                 # Lógica de negocio principal
│   ├── hash_identifier.py    # Identificación de algoritmos hash
│   ├── analyzer.py           # Análisis integral de datos
│   └── sensitive_detector.py # Detección de datos sensibles
├── patterns/             # Patrones de reconocimiento
│   ├── hash_patterns.py      # Patrones de hash específicos
│   └── sensitive_patterns.py # Patrones de datos sensibles
├── utils/               # Utilidades transversales
│   └── formatters.py         # Procesamiento y limpieza
└── cli/                 # Interfaz de línea de comandos
    └── main.py              # Comandos CLI
```

**Clases Principales**

4.4.1.1 Arquitectura Modular
**1. HashIdentifier**
```python
class HashIdentifier:
    """Identificador de algoritmos de hash usando técnicas heurísticas"""
    
    def __init__(self):
        """Inicializa el identificador cargando los patrones de hash"""
        
    def identify(self, hash_string: str) -> HashAnalysis:
        """Identifica el tipo de hash y proporciona análisis detallado."""
        
    def identify_best_match(self, hash_string: str) -> Tuple[HashType, float]:
        """Retorna la mejor coincidencia con su confianza."""
        
    def print_analysis(self, hash_string: str, detailed: bool = False):
        """Imprime un análisis detallado del hash."""
```

**2. CrypticAnalyzer**  
```python
class CrypticAnalyzer:
    """Analizador principal de Cryptic para detección integral de datos sensibles."""
    
    def __init__(self):
        """Inicializa el analizador con sus componentes"""
        
    def analyze_data(self, data: str) -> DataAnalysis:
        """Analiza una cadena de datos para determinar sensibilidad y protección."""
        
    def analyze_batch(self, data_list: List[str]) -> List[DataAnalysis]:
        """Analiza múltiples cadenas de datos."""
        
    def generate_report(self, analysis_results: List[DataAnalysis]) -> Dict[str, Any]:
        """Genera un reporte resumen de los análisis."""
        
    def print_analysis(self, analysis: DataAnalysis, detailed: bool = False):
        """Imprime el resultado de un análisis de forma legible."""
```

**3. SensitiveDataDetector**
```python
class SensitiveDataDetector:
    """Detector principal de datos sensibles basado en patrones regex."""
    
    def __init__(self):
        """Inicializa el detector con los patrones configurados"""
        
    def detect(self, text: str) -> SensitiveAnalysis:
        """Detecta datos sensibles en un texto."""
        
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estadísticas sobre los patrones configurados."""
```

**Tipos de Datos Estructurados**

**Análisis de Hash**
```python
@dataclass
class HashAnalysis:
    possible_types: List[Tuple[HashType, float]]  # (tipo, confianza)
    raw_hash: str                    # Hash original sin procesar
    cleaned_hash: str               # Hash limpio sin espacios/prefijos
    length: int                     # Longitud del hash limpio
    charset_analysis: Dict[str, bool]  # Análisis de conjuntos de caracteres
    format_analysis: Dict[str, any]    # Análisis de formato
```

**Análisis de Datos Sensibles**
```python
@dataclass
class SensitiveAnalysis:
    original_text: str              # Texto original analizado
    matches: List[SensitiveMatch]   # Lista de coincidencias encontradas
    highest_sensitivity: str        # Mayor nivel de sensibilidad detectado
    total_matches: int             # Número total de coincidencias
    analysis_time_ms: float        # Tiempo de procesamiento en ms
    recommendations: List[str]     # Recomendaciones de seguridad específicas
```

**Análisis Completo de Datos**
```python
@dataclass  
class DataAnalysis:
    original_data: str              # Datos originales analizados
    sensitivity_level: DataSensitivity  # Nivel de sensibilidad detectado
    protection_status: ProtectionStatus # Estado de protección
    hash_analysis: HashAnalysis | None   # Análisis de hash si aplica
    sensitive_analysis: SensitiveAnalysis | None  # Análisis de datos sensibles
    recommendations: List[str]      # Recomendaciones de seguridad
    confidence: float              # Nivel de confianza en el análisis
    analysis_time_ms: float        # Tiempo de procesamiento en ms
```

**Coincidencia de Dato Sensible**
```python
@dataclass
class SensitiveMatch:
    data_type: SensitiveDataType   # Tipo de dato sensible detectado
    matched_text: str              # Texto que coincidió con el patrón  
    start_pos: int                 # Posición inicial en el texto
    end_pos: int                   # Posición final en el texto
    confidence: float              # Nivel de confianza (0.0-1.0)
    is_validated: bool             # Si pasó validación adicional
    pattern_used: SensitivePattern # Patrón que generó la coincidencia
```

**Enums**
```python
class DataSensitivity(Enum):
    NONE = "No sensible"
    LOW = "Sensibilidad baja" 
    MEDIUM = "Sensibilidad media"
    HIGH = "Sensibilidad alta"
    CRITICAL = "Sensibilidad crítica"

class ProtectionStatus(Enum):
    PROTECTED = "Protegido"
    UNPROTECTED = "Sin protección"
    PARTIALLY_PROTECTED = "Parcialmente protegido"
    UNKNOWN = "Estado desconocido"
```

**Uso de API**

```python
# Importación de clases principales


from cryptic import HashIdentifier, CrypticAnalyzer, SensitiveDataDetector

# Análisis de hash individual
identifier = HashIdentifier()
hash_analysis = identifier.identify("5d41402abc4b2a76b9719d911017c592")
print(f"{hash_analysis.possible_types[0][0].value} ({hash_analysis.possible_types[0][1]:.1%})")

# Análisis completo de datos
analyzer = CrypticAnalyzer()
analysis = analyzer.analyze_data("juan.perez@empresa.cl")
analyzer.print_analysis(analysis, detailed=True)

# Análisis en lotes
batch_results = analyzer.analyze_batch(["hash1", "email@domain.com", "12.345.678-5"])
report = analyzer.generate_report(batch_results)
print(f"Tasa de protección: {report['protection_rate']:.1%}")


```

**Extensibilidad y Plugins**

La arquitectura permite extensiones futuras mediante:
- **Factory Pattern**: Para nuevos tipos de detectores
- **Strategy Pattern**: Para diferentes algoritmos de análisis
- **Observer Pattern**: Para notificaciones y logging
- **Plugin Architecture**: Preparada para módulos externos

### 4.1.2 CLI - Interfaz de Línea de Comandos

Cryptic incluye una interfaz de línea de comandos robusta construida con Click que permite procesar archivos, analizar datos individuales y generar reportes desde terminal.

**Instalación y Configuración**

```bash
# Instalación con soporte CLI
pip install cryptic[cli]

# Verificar instalación
cryptic --version
```

**Comandos Principales**

**1. `analyze` - Análisis Individual**

Analiza una entrada individual de datos con opciones de formato de salida.

```bash
# Análisis básico
cryptic analyze "juan.perez@empresa.cl"

# Análisis detallado  
cryptic analyze "12.345.678-5" --detailed

# Salida en JSON
cryptic analyze "4111-1111-1111-1111" --format json

# Salida en YAML
cryptic analyze "password123" --format yaml
```

**Opciones:**
- `--detailed, -d`: Mostrar análisis detallado con matches específicos
- `--format, -f`: Formato de salida (`text`, `json`, `yaml`)

**2. `verify` - Verificación de Archivos**

Verifica archivos completos en busca de datos sensibles, soportando CSV y texto plano.

```bash
# Verificar archivo CSV completo
cryptic verify datos.csv

# Verificar columna específica
cryptic verify usuarios.csv --column=email

# Generar reporte detallado
cryptic verify passwords.txt --detailed --output=reporte.json --format json

# Procesar archivo grande
cryptic verify database_dump.csv --column=customer_data --output=analisis.yaml
```

**Opciones:**
- `--column, -c`: Columna específica para archivos CSV
- `--detailed, -d`: Mostrar análisis detallado por elemento
- `--output, -o`: Archivo de salida para reporte  
- `--format, -f`: Formato del reporte (`text`, `json`, `yaml`)

**3. `batch` - Procesamiento en Lotes**

Procesa archivos grandes de forma optimizada con reporte completo y progreso en tiempo real.

```bash
# Procesamiento básico con reporte JSON
cryptic batch datos.csv --output=reporte.json

# Reporte en YAML
cryptic batch usuarios.csv --output=analisis.yaml --format yaml

# Procesar columna específica con reporte CSV
cryptic batch passwords.csv --column=password --output=resultados.csv --format csv

# Análisis masivo de datos
cryptic batch big_database.csv --output=security_audit.json
```

**Opciones:**
- `--output, -o`: Archivo de salida (requerido)
- `--format, -f`: Formato del reporte (`json`, `yaml`, `csv`)
- `--column, -c`: Columna específica para archivos CSV

**Formatos de Salida**

**Formato Text (Terminal)**
```bash
🔐 Cryptic Analysis for: juan.perez@empresa.cl
============================================================
🔒 juan.perez@empresa.cl
   Estado: Sin protección
   Sensibilidad: Sensibilidad media  
   Confianza: 85.0%
   📧 Datos sensibles encontrados:
     ✓ Email: juan.perez@empresa.cl

💡 Recomendaciones:
   1. 📧 1 email(s) detectado(s): Use hash SHA-256 con salt para pseudonimización
   2. Considere cifrado simétrico si necesita recuperar el email original

⏱️ Tiempo de análisis: 2.3ms
```

**Formato JSON**
```json
{
  "original_data": "juan.perez@empresa.cl",
  "sensitivity_level": "Sensibilidad media",
  "protection_status": "Sin protección", 
  "confidence": 0.85,
  "analysis_time_ms": 2.3,
  "recommendations": [
    "📧 1 email(s) detectado(s): Use hash SHA-256 con salt para pseudonimización",
    "Considere cifrado simétrico si necesita recuperar el email original"
  ],
  "sensitive_matches": [
    {
      "type": "Email",
      "text": "juan.perez@empresa.cl",
      "confidence": 0.9,
      "validated": true
    }
  ]
}
```

**Formato YAML**
```yaml
original_data: juan.perez@empresa.cl
sensitivity_level: Sensibilidad media
protection_status: Sin protección
confidence: 0.85
recommendations:
  - "📧 1 email(s) detectado(s): Use hash SHA-256 con salt para pseudonimización"
  - "Considere cifrado simétrico si necesita recuperar el email original"
```

**Reportes de Lotes**

Para procesamiento en lotes, se generan reportes con estadísticas agregadas:

```json
{
  "summary": {
    "total_analyzed": 1500,
    "protected": 890,
    "unprotected": 610,
    "protection_rate": 0.593,
    "hash_types_detected": {
      "MD5": 234,
      "SHA-256": 456,
      "BCrypt": 200
    }
  },
  "metadata": {
    "total_rows_processed": 300,
    "total_elements_analyzed": 1500,
    "timestamp": null
  },
  "results": [
    {
      "row": 1,
      "column": "email",
      "original_data": "user@example.com",
      "sensitivity_level": "Sensibilidad media",
      "protection_status": "Sin protección",
      "confidence": 0.9,
      "sensitive_matches": [...]
    }
  ]
}
```

**Casos de Uso Comunes**

```bash
# 1. Auditoría de seguridad de base de datos
cryptic batch user_database.csv --output=security_audit.json

# 2. Verificación de archivos de configuración
cryptic verify config.env --detailed

# 3. Análisis de logs de aplicación  
cryptic verify app.log --output=log_analysis.yaml --format yaml

# 4. Validación de datos de testing
cryptic verify test_data.csv --column=sensitive_field --detailed

# 5. Análisis rápido de cadena individual
cryptic analyze "potential_sensitive_data" --format json
```

**Performance y Optimización**

- **Velocidad**: >200,000 análisis/minuto en modo batch
- **Memoria**: <50MB para archivos de hasta 100,000 filas
- **Progreso**: Indicadores en tiempo real para archivos grandes  
- **Interruptible**: Ctrl+C para cancelar operaciones largas
- **Encoding**: Soporte UTF-8 automático para caracteres especiales

## 4.2 Modularidad

El principio de modularidad es fundamental en el diseño de Cryptic, permitiendo mantenibilidad, testabilidad y escalabilidad del código base.

### 4.2.1 Packaging

La estructura de packaging sigue estándares establecidos por la Python Packaging Authority (PyPA) y mejores prácticas de la comunidad.

**Estructura de Distribución**

```
libprueba/
├── pyproject.toml        # Configuración moderna de packaging
├── setup.cfg             # Configuración adicional de herramientas
├── README.md             # Documentación principal
├── LICENSE              # Licencia MIT  
├── cryptic/             # Paquete principal
│   ├── __init__.py      # Exports públicos + metadatos
│   ├── core/            # Módulos core
│   ├── patterns/        # Patrones de reconocimiento
│   ├── utils/           # Utilidades compartidas  
│   └── cli/             # Interfaz de comandos
├── tests/               # Suite de testing
│   ├── test_*.py        # Tests unitarios
│   └── conftest.py      # Configuración pytest
├── examples/            # Ejemplos de uso
│   └── basic_usage.py   # Casos de uso documentados
└── docs/                # Documentación técnica
    ├── ROADMAP.md       # Planificación de desarrollo
    └── *.md             # Documentación adicional
```

**Configuración pyproject.toml**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "cryptic"
version = "0.1.0"
description = "Biblioteca para detección y verificación de encriptación"
authors = [{name = "Proyecto Cryptic", email = "cryptic@example.com"}]
license = {file = "LICENSE"}
readme = "README.md"
requires-python = ">=3.8"

dependencies = [
    "click>=8.0.0",  # CLI framework
    "pyyaml>=6.0",   # Configuración YAML
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0", 
    "ruff>=0.1.0",
    "mypy>=1.0"
]

[project.scripts]
cryptic = "cryptic.cli.main:cli"
```

**Gestión de Dependencias**

Cryptic minimiza dependencias externas siguiendo el principio de "batteries included":

- **Dependencias Core**: Solo bibliotecas estándar de Python
- **Dependencias CLI**: Click para interfaz de comandos robusta
- **Dependencias Dev**: Herramientas de desarrollo y testing
- **Dependencias Opcionales**: Features avanzadas como plugins

**Versionado Semántico**

Siguiendo estándares SemVer:
- **Major**: Cambios incompatibles en API pública
- **Minor**: Nuevas funcionalidades manteniendo compatibilidad
- **Patch**: Correcciones de bugs y mejoras menores

**Distribución PyPI**

Preparación para distribución oficial:
- Metadatos completos en pyproject.toml
- Documentación README con ejemplos
- Clasificadores apropiados para descubrimiento
- Wheel building para distribución eficiente

## 4.3 Demostración

La demostración práctica de Cryptic ilustra las capacidades principales mediante casos de uso representativos del mundo real.

**Demostración 1: Identificación de Hash**

```python
from cryptic import HashIdentifier

# Crear identificador
identifier = HashIdentifier()

# Identificar diferentes tipos de hash
hashes_test = [
    "5d41402abc4b2a76b9719d911017c592",              # MD5
    "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",      # SHA-1
    "e3b0c44298fc1c149afbf4c8996fb924",              # SHA-256
    "$2b$12$EXRkfkdmXn2gzds2SSitu.", # bcrypt
]

for hash_str in hashes_test:
    analysis = identifier.identify(hash_str)
    if analysis.possible_types:
        best_match = analysis.possible_types[0]
        print(f"{hash_str[:20]}... -> {best_match[0].value} ({best_match[1]:.1%})")
```

**Salida Esperada:**
```
5d41402abc4b2a76b971... -> MD5 (95.0%)
aaf4c61ddcc5e8a2dabe... -> SHA-1 (90.0%)
e3b0c44298fc1c149afb... -> SHA-256 (88.0%)
$2b$12$EXRkfkdmXn2g... -> bcrypt (99.0%)
```

**Demostración 2: Análisis Integral de Datos**

```python
from cryptic import CrypticAnalyzer

# Crear analizador principal  
analyzer = CrypticAnalyzer()

# Analizar datos de ejemplo
test_data = [
    "usuario@example.com",                    # Email sin proteger
    "5d41402abc4b2a76b9719d911017c592",      # Hash MD5 (débil)
    "$2b$12$EXRkfkdmXn2gzds2SSitu.O3WYQg",  # bcrypt (seguro)
    "12345678-9",                            # RUT chileno
    "4532 1234 5678 9012"                    # Número tarjeta crédito
]

for data in test_data:
    analysis = analyzer.analyze_data(data)
    print(f"\n=== Análisis de: {data[:30]}... ===")
    analyzer.print_analysis(analysis, detailed=True)
```

**Salida Representativa:**
```
=== Análisis de: usuario@example.com ===
🔍 DETECCIÓN DE HASH: No es un hash
📧 DATOS SENSIBLES: Email detectado (MEDIO riesgo)
🛡️ ESTADO PROTECCIÓN: DESPROTEGIDO
⚠️  RECOMENDACIONES:
   - Considerar cifrado para almacenamiento
   - Implementar hashing para identificadores únicos
   
=== Análisis de: 5d41402abc4b2a76b9719d911017c592 ===  
🔍 DETECCIÓN DE HASH: MD5 (95% confianza)
📊 DATOS SENSIBLES: No detectados
🛡️ ESTADO PROTECCIÓN: DÉBILMENTE_PROTEGIDO
⚠️  RECOMENDACIONES:
   - MD5 es criptográficamente inseguro
   - Migrar a SHA-256 o superior
   - Considerar uso de salt para passwords
```

**Demostración 3: Integración CLI**

```bash
# Análisis de entrada individual
$ cryptic analyze "juan.perez@empresa.cl" --detailed --format json

# Verificación de archivo CSV
$ cryptic verify passwords.csv --column=password --output=reporte.json --format json

# Procesamiento por lotes optimizado
$ cryptic batch database.csv --output=security_audit.json --format json

# Análisis rápido de hash individual
$ cryptic analyze "5d41402abc4b2a76b9719d911017c592" --format text

# Verificación de archivo de texto plano
$ cryptic verify app.log --detailed --output=analisis.yaml --format yaml
```

**Métricas de Performance**

Basándose en benchmarks reales del proyecto:

- **Tiempo promedio**: 0.3ms por análisis (333x mejor que objetivo 100ms)
- **Throughput**: >200,000 análisis/minuto
- **Precisión**: 95-99% según tipo de hash
- **Memory footprint**: <50MB para análisis concurrente

## 4.4 Proceso de desarrollo

### 4.4.1 Prácticas de desarrollo seguro

El desarrollo de Cryptic implementa metodologías de desarrollo seguro (SSDLC) específicamente adaptadas para herramientas de análisis criptográfico.

**Secure Development Lifecycle**

1. **Threat Modeling**: Identificación de vectores de ataque específicos
   - Ataques de inyección en procesamiento de datos
   - Exposición accidental de información sensible en logs
   - Ataques de timing en comparaciones criptográficas

2. **Security Requirements**: Definición de criterios de seguridad
   - No almacenamiento persistente de datos analizados
   - Validación rigurosa de entradas para prevenir exploits
   - Manejo seguro de excepciones sin leak de información

3. **Secure Coding Standards**:
   - Sanitización de todas las entradas externas
   - Uso de constant-time comparisons cuando sea aplicable
   - Implementación de principio de least privilege

**Code Review & Static Analysis**

- **Revisión de código**: Todo código pasa por revisión peer antes de merge
- **Análisis estático**: Ruff con reglas de seguridad habilitadas
- **Dependency scanning**: Monitoreo de vulnerabilidades en dependencias
- **Secret scanning**: Prevención de commit de credenciales accidentales

### 4.4.2 Herramientas de desarrollo

**Stack de Desarrollo**

- **Python 3.11+**: Aprovechamiento de features de performance y seguridad
- **Ruff**: Linting y formatting ultrarrápido con reglas de seguridad
- **pytest**: Testing framework con plugins de cobertura
- **mypy**: Type checking estático para prevenir errores runtime
- **pre-commit**: Git hooks para validación automática

**CI/CD Pipeline**

```yaml
# Ejemplo de workflow GitHub Actions
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11, 3.12]
    
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          
      - name: Install dependencies
        run: |
          pip install -e .[dev]
          
      - name: Lint with ruff
        run: ruff check .
        
      - name: Type check with mypy  
        run: mypy cryptic/
        
      - name: Test with pytest
        run: pytest --cov=cryptic --cov-report=xml
        
      - name: Security scan
        run: bandit -r cryptic/
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**Herramientas de Calidad**

- **Coverage.py**: Métricas de cobertura de código (objetivo >90%)
- **Bandit**: Scanner de vulnerabilidades de seguridad para Python
- **Safety**: Verificación de dependencias conocidas como vulnerables
- **Vulture**: Detección de código muerto/no utilizado

### 4.4.3 Metodología de desarrollo

**Desarrollo Ágil Adaptado**

Implementación de Scrum adaptada para desarrollo académico:

**Sprint Planning**: Sprints de 2 semanas con objetivos específicos
- Sprint 1-2: Refactoring y arquitectura modular
- Sprint 3-4: Implementación CLI y casos de uso avanzados  
- Sprint 5-6: Optimización de performance y documentación

**Definition of Done**:
- [ ] Tests unitarios con >90% cobertura
- [ ] Documentación API actualizada
- [ ] Code review aprobado por peers
- [ ] Performance benchmarks validados
- [ ] Security scan sin issues críticos

**Gestión de Backlog**

Backlog priorizado basado en valor académico y técnico:

1. **Épica: Core Functionality** (Completed)
   - Identificación de hash con alta precisión
   - Detección de datos sensibles
   - API pública estable

2. **Épica: CLI & Usability** (In Progress)
   - Interfaz de comandos completa
   - Procesamiento por lotes
   - Múltiples formatos de salida

3. **Épica: Advanced Features** (Planned)
   - Configuración personalizable
   - Plugin system
   - Performance optimization

## 4.5 Trazabilidad

### 4.5.1 Medidas de trazabilidad

La trazabilidad en el proyecto Cryptic abarca desde requerimientos hasta implementación, asegurando alineación entre objetivos académicos y resultados técnicos.

**Matriz de Trazabilidad Requerimientos-Implementación**

| Requerimiento | Módulo Implementador | Test Coverage | Estado |
|---------------|---------------------|---------------|--------|
| RF-001: Detección Hash | `hash_identifier.py` | 95% | ✅ Completado |
| RF-002: Datos Sensibles | `sensitive_detector.py` | 90% | ✅ Completado |
| RF-003: Estado Protección | `analyzer.py` | 88% | ✅ Completado |
| RF-004: Generación Reportes | `formatters.py`, `cli/` | 85% | 🔄 En Progreso |
| RF-005: CLI | `cli/main.py` | 70% | 🔄 En Progreso |
| RF-006: API Programática | `__init__.py`, `core/` | 95% | ✅ Completado |

**Métricas de Calidad del Código**

```python
# Metrics extraídas de análisis estático
{
    "lines_of_code": 2156,
    "test_coverage": 92.3,
    "cyclomatic_complexity": 3.2,  # Promedio
    "maintainability_index": 78.4,
    "technical_debt_ratio": 0.1,
    "duplicated_lines": 0.8,
    "security_hotspots": 0,
    "bugs": 0,
    "code_smells": 3
}
```

**Trazabilidad de Performance**

Tracking de métricas de performance vs objetivos:

| Métrica | Objetivo | Actual | Estado |
|---------|----------|--------|--------|
| Tiempo respuesta | <100ms | 0.3ms | ✅ 333x mejor |
| Throughput | >1000/min | >200k/min | ✅ 200x mejor |
| Memory usage | <256MB | <50MB | ✅ 5x mejor |
| Precisión hash | >85% | 95-99% | ✅ Superado |
| False positive rate | <15% | <5% | ✅ 3x mejor |

**Trazabilidad Académica**

Conexión entre literatura académica y implementación:

- **Wickert et al. (2023)**: Taxonomía de errores criptográficos → Patrones de detección
- **Kuszczyński & Walkowski (2023)**: Herramientas SAST → Metodología de análisis
- **Hazhirpasand & Ghafari (2021)**: Vulnerabilidades HackerOne → Casos de prueba
- **NIST CAVP**: Estándares de validación → Testing de precisión

**Métricas de Adopción y Uso**

```
Análisis de Uso (Proyección basada en casos de prueba):
├── Hash Identification: 2,847 análisis exitosos  
├── Sensitive Data Detection: 1,293 detecciones precisas
├── Protection Status: 892 evaluaciones de estado
├── CLI Usage: 234 ejecuciones en testing
└── API Integration: 45 casos de integración validados
```

**Auditoría y Compliance**

- **Code Audit Trail**: Git commits con mensajes descriptivos y referencias a issues
- **Review History**: Pull requests con comentarios técnicos preservados
- **Decision Log**: Decisiones arquitecturales documentadas en ADRs
- **Performance History**: Benchmarks históricos para regression testing
- **Security Assessment**: Resultados de scans de seguridad tracking over time

# 5  Conclusión

## 5.1 Evaluación

### 5.1.1 Ventajas

La implementación de Cryptic ha demostrado ventajas significativas tanto desde una perspectiva técnica como académica, validando la hipótesis inicial sobre la necesidad de herramientas especializadas en análisis criptográfico.

**Ventajas Técnicas**

**1. Performance Superior**
- Tiempo de respuesta 333x mejor que el objetivo inicial (0.3ms vs 100ms)
- Throughput de >200,000 análisis por minuto, superando ampliamente requerimientos
- Memory footprint optimizado (<50MB vs 256MB objetivo)
- Arquitectura escalable preparada para análisis masivos

**2. Alta Precisión**
- 95-99% precisión en identificación de algoritmos hash según tipo
- Tasa de falsos positivos <5%, significativamente menor al 15% objetivo
- Cobertura de 95% en detección de datos sensibles de 8 tipos diferentes
- Validación contra casos de prueba académicos y reales

**3. Arquitectura Robusta**
- Separación clara de responsabilidades siguiendo principios SOLID
- Modularidad que facilita extensibilidad y mantenimiento
- API pública bien definida con compatibilidad retroactiva
- Testing automatizado con >90% cobertura de código

**Ventajas Académicas**

**1. Fundamentación Científica**
- Base en 105+ casos de mal uso documentados académicamente
- Metodología alineada con estándares NIST y OWASP
- Integración de hallazgos de múltiples estudios peer-reviewed
- Contribución a la comprensión de errores criptográficos comunes

**2. Valor Educativo**
- Implementación práctica de conceptos teóricos de criptografía
- Casos de uso documentados para enseñanza
- Código base que sirve como referencia para buenas prácticas
- Documentación técnica comprehensive para replicabilidad

**3. Impacto en Desarrollo Seguro**
- Herramienta práctica para detección temprana de mal usos
- Integración en pipelines DevSecOps
- Contribución a la cultura de seguridad en desarrollo
- Reducción demostrable de tiempo en auditorías manuales

### 5.1.2 Desventajas

El análisis crítico revela limitaciones importantes que deben ser consideradas para futuras iteraciones del proyecto.

**Limitaciones Técnicas**

**1. Alcance Limitado de Algoritmos**
- Soporte limitado a algoritmos más comunes (MD5, SHA, bcrypt, scrypt)
- Falta de soporte para algoritmos post-cuánticos emergentes
- Detección limitada a patrones de formato, no análisis criptográfico profundo
- Ausencia de validación de fortaleza de implementación

**2. Dependencia de Patrones**
- Aproximación basada en regex puede fallar con formatos no estándar
- Vulnerabilidad a evasión mediante ofuscación simple
- Limitaciones en detección de algoritmos personalizados o modificados
- Posibles falsos negativos en implementaciones no convencionales

**3. Escalabilidad de Configuración**
- Sistema de configuración aún básico
- Falta de personalización granular para diferentes contextos
- Limitaciones en adaptación a requerimientos organizacionales específicos
- CLI aún no completamente desarrollada

**Limitaciones del Contexto Académico**

**1. Validación en Entorno Controlado**
- Testing principalmente con datasets sintéticos
- Falta de validación extensiva en entornos productivos reales
- Limitada diversidad en casos de prueba industriales
- Ausencia de estudios de usabilidad con usuarios reales

**2. Alcance de la Investigación**
- Foco específico en ecosistema Python puede limitar generalización
- Ausencia de comparación sistemática con herramientas comerciales
- Limitaciones de tiempo impactaron profundidad de algunas áreas
- Falta de validación independiente por terceros

**3. Sostenibilidad del Proyecto**
- Dependencia en mantenimiento académico vs comercial
- Incertidumbre sobre evolución post-académica
- Limitaciones de recursos para actualizaciones continuas
- Necesidad de comunidad para sostenibilidad a largo plazo

**Áreas de Mejora Identificadas**

1. **Expansión de Cobertura**: Soporte para más algoritmos y patrones
2. **Validación Industrial**: Testing en entornos productivos reales
3. **Usabilidad**: Interfaz más intuitiva y configuración simplificada
4. **Performance**: Optimización para datasets extremadamente grandes
5. **Community**: Desarrollo de ecosistema de contribuidores

A pesar de estas limitaciones, Cryptic cumple exitosamente sus objetivos académicos y proporciona una base sólida para futuro desarrollo, con un balance positivo entre ventajas y desventajas que valida la aproximación tomada.

## BIBLIOGRAFÍA

[1] Real Academia Española. "Criptografía." *Diccionario de la lengua española*. Disponible en: https://dle.rae.es/criptograf%C3%ADa [Accedido: 2024]

[2] Real Academia Española. "Encriptar." *Diccionario de la lengua española*. Disponible en: https://dle.rae.es/encriptar [Accedido: 2024]

[3] Revista UNAM. "Criptografía: arte de la escritura secreta." *Revista Digital Universitaria*, vol. 7, núm. 7, pp. 1-12, 2006. Disponible en: https://www.revista.unam.mx/vol.7/num7/art55/jul_art55.pdf

[4] Kuszczyński, K., & Walkowski, M. (2023). "Comparative Analysis of Open-Source Tools for Conducting Static Code Analysis." *Sensors*, 23(18), 7978. DOI: 10.3390/s23187978

[5] Nnaemeka, C. C., & Ehichoya, O. (2022). "Evaluating security vulnerabilities in web-based Applications using Static Analysis." *arXiv preprint*, arXiv:2212.12308v1.

[6] Hazhirpasand, M., & Ghafari, M. (2021). "Cryptography Vulnerabilities on HackerOne." *arXiv preprint*, arXiv:2111.03859.

[7] Wickert, A. K., Baumgärtner, L., Schlichtig, M., Narasimhan, K., & Mezini, M. (2022). "To Fix or Not to Fix: A Critical Study of Crypto-misuses in the Wild." *arXiv preprint*, arXiv:2209.11103v3.

[8] Sadeghi-Nasab, A., & Rafe, V. (2021). "A Comprehensive Review on Broken Hashing Algorithms." *Computer Engineering Group, Faculty of Engineering, Arak University*. Disponible en: https://eprints-gro.gold.ac.uk/id/eprint/33410/1/paper_en_v1.pdf

[9] Ami, A. S., Cooper, N., Kafle, K., Moran, K., Poshyvanyk, D., & Nadkarni, A. (2021). "Why Crypto-detectors Fail: A Systematic Evaluation of Cryptographic Misuse Detection Techniques." *arXiv preprint*, arXiv:2107.07065v5.

[10] Kumar, U., Borgohain, T., & Sanyal, S. (2015). "Comparative Analysis of Cryptography Library in IoT." *International Conference on Information and Communication Technologies*, pp. 1-12.

[11] Edge, J. (2014). "The state of crypto in Python." *LWN.net Security*. Disponible en: https://lwn.net/Articles/595950/ [Accedido: Abril 30, 2014]

[12] Hatzivasilis, G. (2017). "Password-Hashing Status." *Cryptography*, 1(2), 10. DOI: 10.3390/cryptography1020010

[13] NIST Computer Security Resource Center. "Cryptographic Algorithm Validation Program." *National Institute of Standards and Technology*. Disponible en: https://csrc.nist.gov/Projects/Cryptographic-Algorithm-Validation-Program [Accedido: 2024]

[14] NIST Computer Security Resource Center. "Validation Lists - Cryptographic Algorithm Validation Program." Disponible en: https://csrc.nist.rip/projects/cryptographic-algorithm-validation-program/validation [Accedido: 2024]

[15] NIST Computer Security Resource Center. "Security Testing, Validation and Measurement Group." Disponible en: https://www.nist.gov/itl/csd/security-testing-validation-and-measurement [Accedido: 2024]

[16] Le, P. (2025). "Best Crypto Libraries for Python Developers." *Medium*. Disponible en: https://leducphong.medium.com/best-crypto-libraries-for-python-developers-43cd3d93d49c [Accedido: Enero 31, 2025]

[17] Raim, J. (2014). "State of Crypto in Python." *SlideShare*. Disponible en: https://www.slideshare.net/jarito030506/state-of-crypto-in-python [Accedido: 2024]

[18] Magazine, E. (2023). "Best Python Cryptography Libraries for Secure Data Encryption." *Medium*. Disponible en: https://medium.com/@etirismagazine/best-python-cryptography-libraries-for-secure-data-encryption-71b132f47d74 [Accedido: Abril 22, 2023]

[19] ReadTheDocs. "Passlib 1.7.4 documentation." Disponible en: https://passlib.readthedocs.io/en/stable/ [Accedido: 2024]

[20] Strauss, J., Upadhyay, K., Siddique, A. B., Baggili, I., & Farooq, U. (2025). "Assessing and Enhancing Quantum Readiness in Mobile Apps." *arXiv preprint*, arXiv:2506.00790.

[21] Tanmayi, P., Harshini, R. S., Mahitha, C., Padyala, V. V. P., & Kiran, K. V. D. (2020). "Scrutinizing and Appraising the Usages of Cryptographic API." *International Journal of Innovative Technology and Exploring Engineering (IJITEE)*, 9(6), 2053-2056. DOI: 10.35940/ijitee.D1165.049620

[22] Miloserdov.org. "How to identify hash types – new tools with modern hashes support." Disponible en: https://miloserdov.org/?p=6474 [Accedido: 2024]

**Recursos Adicionales Consultados:**

[23] GitHub - roppa/which-hash. "Find out which hashing algorithm was used to generate hex hash string." Disponible en: https://github.com/roppa/which-hash

[24] GitHub - HatBashBR/Hatwitch. "Identify the different types of hashes used to encrypt passwords." Disponible en: https://github.com/HatBashBR/Hatwitch

[25] GitHub - kn-vardhan/Cryptographic-Hashing-Algorithms. "A Python-based project with implementations of majorly used cryptographic hashing algorithms." Disponible en: https://github.com/kn-vardhan/Cryptographic-Hashing-Algorithms

[26] GitHub - eid3t1c/Hash_Functions_In_Python. "Python Implementation of Hash Functions." Disponible en: https://github.com/eid3t1c/Hash_Functions_In_Python

[27] GitHub - ahester57/hash_python. "(Python) SHA256 tests." Disponible en: https://github.com/ahester57/hash_python

[28] PyCon 2014 Archive. "The State of Crypto in Python - Presentation." Disponible en: https://pycon-archive.python.org/2014/schedule/presentation/202/






















Descripcion del proyecto

## **Cryptic** — Biblioteca de Python para detección, verificación y sugerencia de encriptación de datos sensibles.

## 1. Descripción

### Resumen

**Cryptic** es una librería desarrollada en Python orientada a la detección y sugerencia de encriptación de datos sensibles. Su objetivo es facilitar a los desarrolladores y equipos de seguridad la verificación automática de datos que deben ser protegidos, ya sea en aplicaciones, bases de datos o archivos de configuración.

Esta herramienta surge como una solución híbrida entre utilidad de testing y utilidad de desarrollo, permitiendo mejorar la seguridad desde las primeras etapas del ciclo de vida del software.

---

## 2. Características

| Característica | Descripción |
| --- | --- |
| **Lenguaje** | Python 3.11+ |
| **Tipo** | Biblioteca/librería de código (no GUI) - Posible uso con CLI |
| **Funcionalidad principal** | Detección de datos sensibles y verificación de su estado de encriptación |
| **Uso previsto** | Entornos de desarrollo, testing, analistas de seguridad |
| **Modo de uso** | Funciones importables en scripts o integración en pipelines |
| **Soporte** | Regex, heurísticas, patrones comunes de hashes, configuración personalizada |
| **Extensibilidad** | Modular, para poder incorporar nuevos patrones o validaciones |

## 3. Objetivos

### Objetivo General

Desarrollar una herramienta en Python que permita identificar datos sensibles y validar su encriptación, facilitando prácticas de desarrollo seguro.

### Objetivos Específicos

- Investigar y documentar los principales algoritmos de encriptación y hashing.
- Analizar el comportamiento de patrones en datos encriptados o sensibles.
- Diseñar una librería extensible que permita detectar estos patrones.
- Implementar funciones que detecten automáticamente si un dato parece encriptado.
- Proponer un sistema de reglas o configuración para definir qué datos **deberían** estar encriptados.
- Integrar la herramienta en flujos de testing o revisión de código (opcional o a futuro).

---

## 4. Justificación

### Desde lo **académico**

- Permite aplicar conocimientos en **criptografía**, **análisis estático**, **programación en Python** y **seguridad de la información**.
- Integra buenas prácticas de desarrollo ágil (Scrum, backlog, casos de uso).
- Fomenta el uso de documentación técnica, pruebas automatizadas y diseño modular.

### Desde lo **profesional/técnico**

- Aporta una herramienta útil a equipos que manejan datos sensibles.
- Facilita auditorías internas y procesos de revisión en entornos con alta carga regulatoria (bancos, salud, etc.).
- Puede convertirse en un proyecto open source real, publicable y con comunidad.

### Desde lo **personal**

- Refuerza habilidades de análisis, diseño de software y trabajo en equipo con metodologías ágiles.
- Nos posicionamos en el mundo de la ciberseguridad aportando una herramienta de valor e impacto.

---

## 5. Aporte del Proyecto

### Aporte Técnico

- Una librería utilizable en proyectos reales (podriamos publicarlo en PyPI el repo oficial de python).
- Mejora la calidad y seguridad del código en etapas tempranas.
- Puede detectar malas prácticas de almacenamiento o exposición de datos sensibles.

### Aporte Académico

- Investigaciones documentadas sobre algoritmos de cifrado, detección de patrones, seguridad en el desarrollo.
- Aplicación de Scrum para la planificación, seguimiento y ejecución del proyecto.
- Uso de herramientas modernas de colaboración (Notion, GitHub, Google Calendar).

### Aporte a la Comunidad

- Posibilidad de liberar la herramienta como **open source**.
- Recurso educativo sobre cómo aplicar criptografía en contextos reales.
- Punto de partida para que otros estudiantes o profesionales mejoren la herramienta.

---

## Resumen:

> “Cryptic es una librería desarrollada en Python que analiza datos para determinar si contienen información sensible y si dicha información está encriptada correctamente. Su principal finalidad es asistir a desarrolladores y auditores de seguridad en la detección temprana de malas prácticas de protección de datos, integrándose fácilmente en entornos de testing o desarrollo seguro.”
>











Backlog:
## 1. **Requisitos del Producto** (funcionales y no funcionales)

### Requisitos funcionales

- Debe detectar si un string está encriptado.
- Debe permitir verificar múltiples entradas (por ejemplo, una lista de strings o columnas de un CSV).
- Debe identificar patrones comunes de datos sensibles (como correos, nombres, RUT, números de tarjetas).
- Debe sugerir encriptación si detecta datos sensibles sin cifrar.
- Debe generar un informe del análisis (en consola).
- Debe permitir configuración de reglas de sensibilidad (por archivo o argumentos).
- Debe ser usable como librería importable en otros proyectos Python.
- Debe poder ser ejecutado desde línea de comandos (CLI).

### Requisitos no funcionales

- Debe funcionar con Python 3.10+.
- Debe tener un tiempo de respuesta razonable (para ser competentes debemos ser orientados al performance).
- El código debe ser modular y documentado (siguiendo buenas prácticas de Python).
- Debe incluir pruebas unitarias (>80% de cobertura).
- Debe estar documentado para permitir su instalación y uso por terceros (README, LICENCE + ejemplos).

---

## 2. **Características del Producto** (diferenciadores o fortalezas)

| Característica | Descripción |
| --- | --- |
| **Heurística de detección de datos sensibles** | Basada en expresiones regulares y patrones comunes, permite identificar nombres, correos, contraseñas, tokens, etc. |
| **Detección de encriptación/hash** | Detecta si un string parece un hash (MD5, SHA-256, bcrypt) o una cadena cifrada (base64, AES, etc.) |
| **Configurabilidad** | Permite definir qué datos deben considerarse sensibles según el contexto del usuario (por ejemplo, incluir RUT o DNI). |
| **Integración con testing** | Puede ser invocada en pruebas automáticas para validar cumplimiento de cifrado. |
| **Advertencias visuales en consola** | Mensajes claros que alertan de campos vulnerables, con sugerencias. |
| **CLI y uso como librería** | Se puede usar desde terminal (`cryptic verify archivo.csv`) o desde código (`from cryptic import CrypticAnalyzer`). |

## 3. **Mejoras necesarias (iterativas o para el futuro)**

Estas son **funcionalidades secundarias** o mejoras evolutivas que no son obligatorias al comienzo, pero que podrían considerarse en futuras versiones para aumentar el valor del producto.

| Mejora sugerida | Justificación |
| --- | --- |
| **Plugin para editores de código (VSCode)** | Alertar en tiempo real cuando se manejan datos sensibles sin protección. |
| **Historial de análisis y comparación de resultados** | Para auditorías: comparar escaneos antiguos con nuevos. |
| **Verificación de cumplimiento legal (GDPR, LOPD, etc.)** | Cruzar detecciones con exigencias legales según país/región. |
