#!/usr/bin/env python3
"""
Módulo para ejecutar todas las verificaciones de calidad del código de Cryptic.

Proporciona comandos unificados para:
- Linting (Ruff)
- Formateo (Ruff)
- Verificación de tipos (MyPy)
- Tests (Pytest)

Uso:
    uv run check-all          # Ejecutar todo
    uv run lint              # Solo linting
    uv run test              # Solo tests
    uv run type-check        # Solo verificación de tipos
    uv run format            # Solo formateo
"""

import subprocess
import sys

from typing import List


def run_command(cmd: List[str], description: str) -> bool:
    """Ejecutar comando con manejo de errores."""
    print(f"\n🔄 {description}...")
    try:
        _ = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} falló: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Comando no encontrado: {' '.join(cmd)}")
        print("   Asegúrate de que las dependencias estén instaladas con: uv sync --extra dev")
        return False


def lint_code() -> bool:
    """Ejecutar linting con Ruff."""
    checks = [
        (["uv", "run", "ruff", "check", "cryptic", "tests"], "Verificación de estilo (Ruff)"),
        (["uv", "run", "ruff", "format", "--check", "cryptic", "tests"], "Verificación de formato (Ruff)"),
    ]

    all_passed = True
    for cmd, description in checks:
        if not run_command(cmd, description):
            all_passed = False

    return all_passed


def check_types() -> bool:
    """Ejecutar verificación de tipos con MyPy."""
    return run_command(
        ["uv", "run", "mypy", "."],
        "Verificación de tipos (MyPy)"
    )


def run_tests() -> bool:
    """Ejecutar tests con Pytest."""
    return run_command(
        ["uv", "run", "pytest", "tests/"],
        "Ejecución de tests (Pytest)"
    )


def format_code() -> bool:
    """Formatear código con Ruff."""
    return run_command(
        ["uv", "run", "ruff", "format", "cryptic", "tests"],
        "Formateo de código (Ruff)"
    )


def main() -> int:
    """Ejecutar todas las verificaciones de calidad."""
    print("🚀 Ejecutando verificaciones completas de Cryptic")
    print("=" * 60)

    # Lista de verificaciones a ejecutar
    checks = [
        (lint_code, "Linting y Formato"),
        (check_types, "Verificación de Tipos"),
        (run_tests, "Tests"),
    ]

    all_passed = True
    for check_func, _ in checks:
        print(f"\n📋 Ejecutando: {_}")
        print("-" * 40)
        if not check_func():
            all_passed = False

    # Resumen final
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ¡Todas las verificaciones pasaron!")
        print("✅ Código listo para producción")
        return 0
    else:
        print("❌ Algunas verificaciones fallaron")
        print("🔧 Revisa los errores arriba e intenta nuevamente")
        return 1


def lint_only() -> int:
    """Solo ejecutar linting."""
    print("🔍 Ejecutando solo linting...")
    return 0 if lint_code() else 1


def test_only() -> int:
    """Solo ejecutar tests."""
    print("🧪 Ejecutando solo tests...")
    return 0 if run_tests() else 1


def type_check_only() -> int:
    """Solo ejecutar verificación de tipos."""
    print("🔤 Ejecutando solo verificación de tipos...")
    return 0 if check_types() else 1


def format_only() -> int:
    """Solo formatear código."""
    print("🎨 Formateando código...")
    return 0 if format_code() else 1


# Función de conveniencia para desarrollo rápido
def quick_check() -> int:
    """Verificación rápida (linting + tests, sin tipos para velocidad)."""
    print("⚡ Verificación rápida (linting + tests)...")

    checks = [
        (lint_code, "Linting"),
        (run_tests, "Tests"),
    ]

    all_passed = True
    for check_func, _ in checks:
        if not check_func():
            all_passed = False

    return 0 if all_passed else 1


if __name__ == "__main__":
    # Determinar qué función ejecutar basado en argumentos
    if len(sys.argv) > 1:
        command = sys.argv[1]
        functions = {
            "lint": lint_only,
            "test": test_only,
            "type-check": type_check_only,
            "format": format_only,
            "quick": quick_check,
        }

        if command in functions:
            sys.exit(functions[command]())
        else:
            print(f"❌ Comando desconocido: {command}")
            print(f"💡 Comandos disponibles: {', '.join(functions.keys())}")
            sys.exit(1)

    # Sin argumentos: ejecutar todo
    sys.exit(main())
