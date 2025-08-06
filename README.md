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

### 2.2.1 Panorama general de herramientas

### 2.2.2 Herramientas de desarrollo

## 2.2 Ciberseguridad

### 2.2.1 Errores comunes

### 2.2.2 Prácticas de desarrollo seguro

## 2.3 Terminología

### 2.3.1 Algoritmos

# 3  Investigación

## 3.1 Requerimientos

### 3.1.1 Requerimientos Funcionales

### 3.1.2 Requerimientos No Funcionales

## 3.2 Casos de uso

### 3.1.1 Desarrollo

### 3.1.2 Testing

### 3.1.3 Auditoría

## 3.3 Análisis de viabilidad

### 3.3.1 Necesidades

## 3.4 Procesos

### 3.4.1 Enfoque en performance

# 4  Implementación

## 4.1 Diseño

Entre los recursos que se han utilizado para el desarrollo de este proyecto, están los siguientes:
- Python 3.11+
- Pytest
- Ruff
- PyPI
- Notion
- Google Calendar
- GitHub

### 4.1.1 API

## 4.2 Modularidad

### 4.2.1 Packaging

## 4.3 Demostración

## 4.4 Proceso de desarrollo

### 4.4.1 Prácticas de desarrollo seguro

### 4.4.2 Herramientas de desarrollo

### 4.4.3 Metodología de desarrollo

## 4.5 Trazabilidad

### 4.4.1 Medidas de trazabilidad

# 5  Conclusión

## 5.1 Evaluación

### 5.1.1 Ventajas

### 5.1.2 Desventajas


BIBLIOGRAFÍA






















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
| **CLI y uso como librería** | Se puede usar desde terminal (`cryptic verify archivo.csv`) o desde código (`from cryptic import verify_string`). |

## 3. **Mejoras necesarias (iterativas o para el futuro)**

Estas son **funcionalidades secundarias** o mejoras evolutivas que no son obligatorias al comienzo, pero que podrían considerarse en futuras versiones para aumentar el valor del producto.

| Mejora sugerida | Justificación |
| --- | --- |
| **Plugin para editores de código (VSCode)** | Alertar en tiempo real cuando se manejan datos sensibles sin protección. |
| **Historial de análisis y comparación de resultados** | Para auditorías: comparar escaneos antiguos con nuevos. |
| **Verificación de cumplimiento legal (GDPR, LOPD, etc.)** | Cruzar detecciones con exigencias legales según país/región. |
