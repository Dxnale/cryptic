#!/usr/bin/env python3
"""
Ejemplo básico de uso de la librería Cryptic.

Este script demuestra las funcionalidades principales de Cryptic
para identificación de hashes y análisis de datos sensibles.
"""

from cryptic import HashIdentifier, CrypticAnalyzer, quick_identify, batch_identify


def demo_hash_identification():
    """Demuestra la identificación de hashes"""
    print("=" * 60)
    print("DEMO: Identificación de Hashes")
    print("=" * 60)
    
    # Crear instancia del identificador
    identifier = HashIdentifier()
    
    # Ejemplos de hashes para identificar
    test_hashes = [
        "5d41402abc4b2a76b9719d911017c592",  # MD5
        "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",  # SHA-1
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # SHA-256
        "*A4B6157319038724E3560894F7F932C8886EBFCF",  # MySQL5
        "$2b$10$N9qo8uLOickgx2ZMRZoMye",  # bcrypt
        "$P$B123456789abcdef123456789abcdef",  # WordPress
    ]
    
    print("Identificación individual:")
    for hash_str in test_hashes[:3]:
        print(f"  {hash_str} -> {quick_identify(hash_str)}")
    
    print("\nAnálisis detallado:")
    identifier.print_analysis(test_hashes[0], detailed=True)
    
    print("Identificación en lote:")
    batch_results = batch_identify(test_hashes)
    for hash_str, (hash_type, confidence) in batch_results.items():
        print(f"  {hash_str[:32]}... -> {hash_type.value} ({confidence:.1%})")


def demo_cryptic_analyzer():
    """Demuestra el analizador principal de Cryptic"""
    print("=" * 60)
    print("DEMO: Analizador Cryptic")
    print("=" * 60)
    
    analyzer = CrypticAnalyzer()
    
    # Datos de ejemplo
    test_data = [
        "5d41402abc4b2a76b9719d911017c592",  # Hash MD5
        "$2b$10$N9qo8uLOickgx2ZMRZoMye",      # Hash bcrypt
        "plain_password",                     # Texto plano
        "*A4B6157319038724E3560894F7F932C8886EBFCF",  # MySQL5
    ]
    
    print("Análisis individual:")
    analysis = analyzer.analyze_data(test_data[0])
    analyzer.print_analysis(analysis, detailed=True)
    
    print("\nAnálisis en lote:")
    batch_analyses = analyzer.analyze_batch(test_data)
    
    print("Reporte resumen:")
    report = analyzer.generate_report(batch_analyses)
    print(f"  Total analizado: {report['total_analyzed']}")
    print(f"  Elementos protegidos: {report['protected']}")
    print(f"  Tasa de protección: {report['protection_rate']:.1%}")
    print(f"  Tipos de hash detectados: {list(report['hash_types_detected'].keys())}")


def demo_compatibility():
    """Demuestra compatibilidad con la API anterior"""
    print("=" * 60)
    print("DEMO: Compatibilidad con API anterior")
    print("=" * 60)
    
    # Las funciones de conveniencia mantienen compatibilidad
    test_hash = "5d41402abc4b2a76b9719d911017c592"
    
    # Identificación rápida
    result = quick_identify(test_hash)
    print(f"quick_identify: {result}")
    
    # Identificación en lote
    batch = [test_hash, "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"]
    results = batch_identify(batch)
    print(f"batch_identify: {len(results)} resultados procesados")


if __name__ == "__main__":
    print("Cryptic - Biblioteca de análisis de datos sensibles")
    print("Desarrollado por Los Leones Team")
    print()
    
    # Ejecutar demos
    demo_hash_identification()
    print()
    demo_cryptic_analyzer()
    print()
    demo_compatibility()
    
    print("\n" + "=" * 60)
    print("Demo completado. Consulta la documentación para más funcionalidades.")
    print("=" * 60)
