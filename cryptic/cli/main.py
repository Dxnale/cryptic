"""
CLI principal de Cryptic para detección y análisis de datos sensibles desde terminal.

Este módulo proporciona comandos de línea de comandos para:
- Verificar archivos CSV en busca de datos sensibles
- Analizar entradas individuales
- Generar reportes en lote
- Exportar resultados en múltiples formatos
"""

import sys
import csv
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import asdict

import click

from cryptic import CrypticAnalyzer, DataAnalysis
from cryptic.core.sensitive_detector import SensitiveDataDetector


class Colors:
    """Códigos de color ANSI para output terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'  
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_colored(text: str, color: str = Colors.WHITE, bold: bool = False):
    """Imprime texto con color en terminal"""
    style = f"{Colors.BOLD if bold else ''}{color}"
    click.echo(f"{style}{text}{Colors.END}")


def format_analysis_for_terminal(analysis: DataAnalysis, detailed: bool = False) -> str:
    """Formatea un análisis para mostrar en terminal con colores"""
    
    # Determinar color según estado de protección
    if analysis.protection_status.value == "Protegido":
        status_color = Colors.GREEN
        status_icon = "🔒"
    elif analysis.protection_status.value == "Sin protección":
        status_color = Colors.RED 
        status_icon = "⚠️ "
    elif analysis.protection_status.value == "Parcialmente protegido":
        status_color = Colors.YELLOW
        status_icon = "🟡"
    else:
        status_color = Colors.CYAN
        status_icon = "❓"
    
    # Determinar color según sensibilidad
    if analysis.sensitivity_level.value == "Sensibilidad crítica":
        sensitivity_color = Colors.RED
    elif analysis.sensitivity_level.value == "Sensibilidad alta":
        sensitivity_color = Colors.YELLOW
    elif analysis.sensitivity_level.value == "Sensibilidad media":
        sensitivity_color = Colors.BLUE
    else:
        sensitivity_color = Colors.WHITE
    
    # Formatear salida
    result = []
    
    # Línea principal
    data_preview = analysis.original_data[:50] + "..." if len(analysis.original_data) > 50 else analysis.original_data
    result.append(f"{status_icon} {Colors.BOLD}{data_preview}{Colors.END}")
    
    # Estado y sensibilidad
    result.append(f"   Estado: {status_color}{analysis.protection_status.value}{Colors.END}")
    result.append(f"   Sensibilidad: {sensitivity_color}{analysis.sensitivity_level.value}{Colors.END}")
    result.append(f"   Confianza: {Colors.CYAN}{analysis.confidence:.1%}{Colors.END}")
    
    # Detalles si está en modo detallado
    if detailed:
        if analysis.sensitive_analysis and analysis.sensitive_analysis.matches:
            result.append(f"   {Colors.YELLOW}Datos sensibles encontrados:{Colors.END}")
            for match in analysis.sensitive_analysis.matches[:3]:  # Máximo 3
                validation = "✓" if match.is_validated else "⚠"
                result.append(f"     {validation} {match.data_type.value}: {match.matched_text}")
        
        if analysis.hash_analysis and analysis.hash_analysis.possible_types:
            hash_type = analysis.hash_analysis.possible_types[0][0].value
            result.append(f"   {Colors.GREEN}Hash detectado:{Colors.END} {hash_type}")
    
    return "\n".join(result)


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Mostrar versión')
@click.pass_context
def cli(ctx, version):
    """
    🔐 Cryptic - Herramienta de detección y análisis de datos sensibles
    
    Detecta automáticamente información sensible como emails, RUTs chilenos,
    números de tarjetas de crédito, teléfonos y más.
    """
    if version:
        print_colored("🔐 Cryptic v0.1.0", Colors.CYAN, bold=True)
        print_colored("Biblioteca para detección de datos sensibles", Colors.WHITE)
        return
    
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument('data', type=str)
@click.option('--detailed', '-d', is_flag=True, help='Mostrar análisis detallado')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'yaml']), 
              default='text', help='Formato de salida')
def analyze(data: str, detailed: bool, format: str):
    """
    Analizar una entrada individual de datos.
    
    Ejemplos:
    \b
    cryptic analyze "juan.perez@empresa.cl"
    cryptic analyze "12.345.678-5" --detailed
    cryptic analyze "4111-1111-1111-1111" --format json
    """
    print_colored(f"\n🔍 Analizando: {data}", Colors.CYAN, bold=True)
    print_colored("=" * 60, Colors.CYAN)
    
    try:
        analyzer = CrypticAnalyzer()
        analysis = analyzer.analyze_data(data)
        
        if format == 'json':
            # Convertir análisis a diccionario serializable
            result = {
                'original_data': analysis.original_data,
                'sensitivity_level': analysis.sensitivity_level.value,
                'protection_status': analysis.protection_status.value,
                'confidence': analysis.confidence,
                'analysis_time_ms': analysis.analysis_time_ms,
                'recommendations': analysis.recommendations
            }
            
            # Agregar detalles de datos sensibles si existen
            if analysis.sensitive_analysis and analysis.sensitive_analysis.matches:
                result['sensitive_matches'] = [
                    {
                        'type': match.data_type.value,
                        'text': match.matched_text,
                        'confidence': match.confidence,
                        'validated': match.is_validated
                    }
                    for match in analysis.sensitive_analysis.matches
                ]
            
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif format == 'yaml':
            result = {
                'original_data': analysis.original_data,
                'sensitivity_level': analysis.sensitivity_level.value,
                'protection_status': analysis.protection_status.value,
                'confidence': analysis.confidence,
                'recommendations': analysis.recommendations
            }
            click.echo(yaml.dump(result, default_flow_style=False, allow_unicode=True))
            
        else:  # text format
            click.echo(format_analysis_for_terminal(analysis, detailed))
            
            if analysis.recommendations:
                print_colored(f"\n💡 Recomendaciones:", Colors.YELLOW, bold=True)
                for i, rec in enumerate(analysis.recommendations, 1):
                    click.echo(f"   {i}. {rec}")
                    
            print_colored(f"\n⏱️  Tiempo de análisis: {analysis.analysis_time_ms:.1f}ms", Colors.GREEN)
        
    except Exception as e:
        print_colored(f"\n❌ Error durante el análisis: {str(e)}", Colors.RED, bold=True)
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('--column', '-c', type=str, help='Columna específica a analizar (para CSV)')
@click.option('--detailed', '-d', is_flag=True, help='Mostrar análisis detallado')
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Archivo de salida para reporte')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'yaml']), 
              default='text', help='Formato de salida')
def verify(file_path: Path, column: Optional[str], detailed: bool, 
           output: Optional[Path], format: str):
    """
    Verificar un archivo en busca de datos sensibles.
    
    Soporta archivos de texto plano y CSV.
    
    Ejemplos:
    \b
    cryptic verify datos.csv --column=email
    cryptic verify usuarios.csv --output=reporte.json --format json
    cryptic verify passwords.txt --detailed
    """
    print_colored(f"\n🔍 Verificando archivo: {file_path.name}", Colors.CYAN, bold=True)
    print_colored("=" * 60, Colors.CYAN)
    
    try:
        analyzer = CrypticAnalyzer()
        results = []
        
        if file_path.suffix.lower() == '.csv':
            # Procesar archivo CSV
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows_processed = 0
                
                for row in reader:
                    if column:
                        # Analizar solo la columna especificada
                        if column in row and row[column]:
                            analysis = analyzer.analyze_data(row[column])
                            analysis.original_data = f"Fila {rows_processed + 1}, {column}: {row[column]}"
                            results.append(analysis)
                    else:
                        # Analizar todas las columnas
                        for col_name, value in row.items():
                            if value and value.strip():
                                analysis = analyzer.analyze_data(value)
                                analysis.original_data = f"Fila {rows_processed + 1}, {col_name}: {value}"
                                results.append(analysis)
                    
                    rows_processed += 1
                    
                    # Mostrar progreso cada 100 filas
                    if rows_processed % 100 == 0:
                        print_colored(f"   Procesadas {rows_processed} filas...", Colors.BLUE)
        
        else:
            # Procesar archivo de texto plano
            with open(file_path, 'r', encoding='utf-8') as f:
                line_number = 0
                for line in f:
                    line = line.strip()
                    if line:
                        line_number += 1
                        analysis = analyzer.analyze_data(line)
                        analysis.original_data = f"Línea {line_number}: {line}"
                        results.append(analysis)
        
        # Generar reporte
        report = analyzer.generate_report(results)
        
        # Mostrar resumen
        print_colored(f"\n📊 Resumen del análisis:", Colors.GREEN, bold=True)
        click.echo(f"   Total de elementos analizados: {report['total_analyzed']}")
        click.echo(f"   Elementos protegidos: {report['protected']} ({report['protection_rate']:.1%})")
        click.echo(f"   Elementos sin protección: {report['unprotected']}")
        
        # Mostrar datos sensibles encontrados
        sensitive_count = sum(1 for r in results if r.sensitive_analysis.matches)
        if sensitive_count > 0:
            print_colored(f"   ⚠️  Datos sensibles detectados: {sensitive_count}", Colors.RED, bold=True)
        
        # Mostrar resultados detallados si se solicita
        if detailed and results:
            print_colored(f"\n📋 Análisis detallado:", Colors.YELLOW, bold=True)
            for result in results[:10]:  # Mostrar máximo 10
                click.echo("\n" + format_analysis_for_terminal(result, True))
            
            if len(results) > 10:
                print_colored(f"\n... y {len(results) - 10} más (use --output para ver todos)", Colors.BLUE)
        
        # Guardar reporte si se especifica archivo de salida
        if output:
            save_report(results, report, output, format)
            print_colored(f"\n💾 Reporte guardado en: {output}", Colors.GREEN, bold=True)
    
    except Exception as e:
        print_colored(f"\n❌ Error procesando archivo: {str(e)}", Colors.RED, bold=True)
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), required=True,
              help='Archivo de salida para reporte (requerido)')
@click.option('--format', '-f', type=click.Choice(['json', 'yaml', 'csv']), 
              default='json', help='Formato del reporte')
@click.option('--column', '-c', type=str, help='Columna específica a analizar (para CSV)')
def batch(file_path: Path, output: Path, format: str, column: Optional[str]):
    """
    Procesar un archivo en lote y generar reporte completo.
    
    Optimizado para archivos grandes con reporte detallado.
    
    Ejemplos:
    \b
    cryptic batch datos.csv --output=reporte.json
    cryptic batch usuarios.csv --output=analisis.yaml --format yaml
    cryptic batch passwords.csv --column=password --output=resultados.csv --format csv
    """
    print_colored(f"\n🚀 Procesando en lote: {file_path.name}", Colors.CYAN, bold=True)
    print_colored("=" * 60, Colors.CYAN)
    
    try:
        analyzer = CrypticAnalyzer()
        detector = SensitiveDataDetector()
        results = []
        
        total_rows = 0
        
        # Contar filas primero para mostrar progreso
        if file_path.suffix.lower() == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                total_rows = sum(1 for _ in csv.DictReader(f))
        
        print_colored(f"📈 Iniciando procesamiento de {total_rows} filas...", Colors.BLUE)
        
        processed = 0
        
        if file_path.suffix.lower() == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    if column:
                        # Procesar solo columna especificada
                        if column in row and row[column]:
                            analysis = analyzer.analyze_data(row[column])
                            results.append({
                                'row': processed + 1,
                                'column': column,
                                'original_data': row[column],
                                'analysis': analysis
                            })
                    else:
                        # Procesar todas las columnas
                        for col_name, value in row.items():
                            if value and value.strip():
                                analysis = analyzer.analyze_data(value)
                                results.append({
                                    'row': processed + 1,
                                    'column': col_name,
                                    'original_data': value,
                                    'analysis': analysis
                                })
                    
                    processed += 1
                    
                    # Mostrar progreso
                    if processed % 50 == 0 or processed == total_rows:
                        progress = (processed / total_rows) * 100 if total_rows > 0 else 0
                        print_colored(f"   Progreso: {processed}/{total_rows} ({progress:.1f}%)", Colors.GREEN)
        
        # Generar reporte completo
        analyses = [r['analysis'] for r in results]
        report = analyzer.generate_report(analyses)
        
        print_colored(f"\n📊 Procesamiento completado:", Colors.GREEN, bold=True)
        click.echo(f"   Total procesado: {len(results)} elementos")
        click.echo(f"   Tasa de protección: {report['protection_rate']:.1%}")
        
        # Contar datos sensibles por tipo
        sensitive_by_type = {}
        for result in results:
            if result['analysis'].sensitive_analysis.matches:
                for match in result['analysis'].sensitive_analysis.matches:
                    data_type = match.data_type.value
                    sensitive_by_type[data_type] = sensitive_by_type.get(data_type, 0) + 1
        
        if sensitive_by_type:
            print_colored(f"   ⚠️  Datos sensibles por tipo:", Colors.YELLOW, bold=True)
            for data_type, count in sensitive_by_type.items():
                click.echo(f"      {data_type}: {count}")
        
        # Guardar reporte
        save_batch_report(results, report, output, format)
        print_colored(f"\n💾 Reporte completo guardado en: {output}", Colors.GREEN, bold=True)
        
    except Exception as e:
        print_colored(f"\n❌ Error en procesamiento por lotes: {str(e)}", Colors.RED, bold=True)
        sys.exit(1)


def save_report(results: List[DataAnalysis], report: Dict[str, Any], 
                output_path: Path, format: str):
    """Guarda un reporte de análisis en el formato especificado"""
    
    if format == 'json':
        data = {
            'summary': report,
            'results': [
                {
                    'original_data': r.original_data,
                    'sensitivity_level': r.sensitivity_level.value,
                    'protection_status': r.protection_status.value,
                    'confidence': r.confidence,
                    'analysis_time_ms': r.analysis_time_ms,
                    'recommendations': r.recommendations,
                    'sensitive_matches': [
                        {
                            'type': match.data_type.value,
                            'text': match.matched_text,
                            'confidence': match.confidence,
                            'validated': match.is_validated
                        }
                        for match in (r.sensitive_analysis.matches if r.sensitive_analysis else [])
                    ] if r.sensitive_analysis else []
                }
                for r in results
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    elif format == 'yaml':
        data = {
            'summary': report,
            'results': [
                {
                    'original_data': r.original_data,
                    'sensitivity_level': r.sensitivity_level.value,
                    'protection_status': r.protection_status.value,
                    'confidence': r.confidence,
                    'recommendations': r.recommendations
                }
                for r in results
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def save_batch_report(results: List[Dict], report: Dict[str, Any], 
                      output_path: Path, format: str):
    """Guarda un reporte de procesamiento por lotes"""
    
    if format == 'json':
        data = {
            'summary': report,
            'metadata': {
                'total_rows_processed': len(set(r['row'] for r in results)),
                'total_elements_analyzed': len(results),
                'timestamp': None
            },
            'results': [
                {
                    'row': r['row'],
                    'column': r['column'],
                    'original_data': r['original_data'],
                    'sensitivity_level': r['analysis'].sensitivity_level.value,
                    'protection_status': r['analysis'].protection_status.value,
                    'confidence': r['analysis'].confidence,
                    'sensitive_matches': [
                        {
                            'type': match.data_type.value,
                            'text': match.matched_text,
                            'confidence': match.confidence,
                            'validated': match.is_validated
                        }
                        for match in (r['analysis'].sensitive_analysis.matches if r['analysis'].sensitive_analysis else [])
                    ]
                }
                for r in results
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    elif format == 'csv':
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['row', 'column', 'original_data', 'sensitivity_level', 
                         'protection_status', 'confidence', 'sensitive_types']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for r in results:
                sensitive_types = []
                if r['analysis'].sensitive_analysis and r['analysis'].sensitive_analysis.matches:
                    sensitive_types = [match.data_type.value for match in r['analysis'].sensitive_analysis.matches]
                
                writer.writerow({
                    'row': r['row'],
                    'column': r['column'], 
                    'original_data': r['original_data'],
                    'sensitivity_level': r['analysis'].sensitivity_level.value,
                    'protection_status': r['analysis'].protection_status.value,
                    'confidence': r['analysis'].confidence,
                    'sensitive_types': '; '.join(sensitive_types)
                })
    
    elif format == 'yaml':
        data = {
            'summary': report,
            'results': [
                {
                    'row': r['row'],
                    'column': r['column'],
                    'original_data': r['original_data'],
                    'sensitivity_level': r['analysis'].sensitivity_level.value,
                    'protection_status': r['analysis'].protection_status.value,
                    'confidence': r['analysis'].confidence
                }
                for r in results
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def main():
    """Función principal del CLI"""
    try:
        cli()
    except KeyboardInterrupt:
        print_colored(f"\n\n⚠️  Operación cancelada por el usuario", Colors.YELLOW)
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n❌ Error inesperado: {str(e)}", Colors.RED, bold=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
