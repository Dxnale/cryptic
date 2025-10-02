"""
Tests para la interfaz de línea de comandos de Cryptic.

Este módulo contiene tests para validar que todos los comandos CLI
funcionen correctamente con diferentes tipos de entrada y formatos de salida.
"""

import json
import tempfile
from pathlib import Path

import yaml
from click.testing import CliRunner

from cryptic.cli.main import cli


class TestCLI:
    """Tests principales para los comandos CLI"""

    def setup_method(self):
        """Setup para cada test"""
        self.runner = CliRunner()

    def test_cli_help(self):
        """Test comando de ayuda principal"""
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Cryptic - Herramienta de detección" in result.output
        assert "analyze" in result.output
        assert "verify" in result.output
        assert "batch" in result.output

    def test_cli_version(self):
        """Test comando de versión"""
        result = self.runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "Cryptic v0.1.0" in result.output
        assert "detección de datos sensibles" in result.output

    def test_analyze_command_email(self):
        """Test comando analyze con email"""
        result = self.runner.invoke(cli, ["analyze", "juan@empresa.cl"])
        assert result.exit_code == 0
        assert "Analizando: juan@empresa.cl" in result.output
        assert "Sin protección" in result.output
        assert "Sensibilidad alta" in result.output

    def test_analyze_command_rut(self):
        """Test comando analyze con RUT chileno"""
        result = self.runner.invoke(cli, ["analyze", "12.345.678-5", "--detailed"])
        assert result.exit_code == 0
        assert "Sensibilidad crítica" in result.output
        assert "RUT Chileno" in result.output
        assert "HMAC-SHA256" in result.output

    def test_analyze_command_hash(self):
        """Test comando analyze con hash"""
        result = self.runner.invoke(cli, ["analyze", "5d41402abc4b2a76b9719d911017c592"])
        assert result.exit_code == 0
        assert "Protegido" in result.output
        assert "MD5" in result.output

    def test_analyze_command_json_format(self):
        """Test comando analyze con formato JSON"""
        result = self.runner.invoke(cli, ["analyze", "juan@empresa.cl", "--format", "json"])
        assert result.exit_code == 0

        # Verificar que es JSON válido
        output_lines = result.output.strip().split("\n")
        json_start = None
        for i, line in enumerate(output_lines):
            if line.strip().startswith("{"):
                json_start = i
                break

        assert json_start is not None
        json_output = "\n".join(output_lines[json_start:])
        data = json.loads(json_output)

        assert data["original_data"] == "juan@empresa.cl"
        assert data["sensitivity_level"] == "Sensibilidad alta"
        assert data["protection_status"] == "Sin protección"
        assert "sensitive_matches" in data

    def test_analyze_command_yaml_format(self):
        """Test comando analyze con formato YAML"""
        result = self.runner.invoke(cli, ["analyze", "test-data", "--format", "yaml"])
        assert result.exit_code == 0

        # Buscar el inicio del YAML en la salida
        output_lines = result.output.strip().split("\n")
        yaml_start = None
        for i, line in enumerate(output_lines):
            if "confidence:" in line or "original_data:" in line:
                yaml_start = i
                break

        assert yaml_start is not None
        yaml_output = "\n".join(output_lines[yaml_start:])

        # Verificar que es YAML válido
        data = yaml.safe_load(yaml_output)
        assert isinstance(data, dict)
        assert "original_data" in data


class TestCLIFileHandling:
    """Tests para manejo de archivos en CLI"""

    def setup_method(self):
        """Setup para cada test"""
        self.runner = CliRunner()

    def test_verify_csv_file_email_column(self):
        """Test verificación de archivo CSV con columna email"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("email,password\n")
            f.write("juan@mail.com,hash123\n")
            f.write("maria@empresa.cl,5d41402abc4b2a76b9719d911017c592\n")
            csv_path = f.name

        try:
            result = self.runner.invoke(cli, ["verify", csv_path, "--column", "email"])
            assert result.exit_code == 0
            assert "Verificando archivo:" in result.output
            assert "Total de elementos analizados:" in result.output
            assert "Datos sensibles detectados:" in result.output
        finally:
            Path(csv_path).unlink(missing_ok=True)

    def test_verify_csv_file_no_column(self):
        """Test verificación de archivo CSV sin columna"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("email,password\n")
            f.write("juan@mail.com,hash123\n")
            f.write("maria@empresa.cl,5d41402abc4b2a76b9719d911017c592\n")
            csv_path = f.name

        try:
            result = self.runner.invoke(cli, ["verify", csv_path])
            assert result.exit_code == 0
            assert "Verificando archivo:" in result.output
            assert "Total de elementos analizados:" in result.output
            assert "Datos sensibles detectados:" in result.output
        finally:
            Path(csv_path).unlink(missing_ok=True)

    def test_verify_text_file(self):
        """Test verificación de archivo de texto"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("juan@empresa.cl\n")
            f.write("12.345.678-5\n")
            f.write("plaintext\n")
            txt_path = f.name

        try:
            result = self.runner.invoke(cli, ["verify", txt_path, "--detailed"])
            assert result.exit_code == 0
            assert "Análisis detallado:" in result.output
            assert "juan@empresa.cl" in result.output
            assert "12.345.678-5" in result.output
        finally:
            Path(txt_path).unlink(missing_ok=True)

    def test_verify_detailed_many_results_message(self):
        """Test verify command with --detailed flag shows message for more than 10 results"""
        # Create a text file with more than 10 lines of data
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            # Create 15 lines of test data
            test_data = [
                "juan@empresa.cl",
                "12.345.678-5",
                "5d41402abc4b2a76b9719d911017c592",
                "+56912345678",
                "192.168.1.1",
                "texto normal 1",
                "texto normal 2",
                "texto normal 3",
                "texto normal 4",
                "texto normal 5",
                "texto normal 6",
                "texto normal 7",
                "texto normal 8",
                "texto normal 9",
                "texto normal 10"
            ]

            for data in test_data:
                f.write(f"{data}\n")

            txt_path = f.name

        try:
            # Run verify command with --detailed flag
            result = self.runner.invoke(cli, ["verify", txt_path, "--detailed"])
            assert result.exit_code == 0

            # Verify that the message about additional results appears
            expected_message = "... y 5 más (use --output para ver todos)"
            assert expected_message in result.output

            # Also verify that the detailed analysis section appears
            assert "📋 Análisis detallado:" in result.output

        finally:
            Path(txt_path).unlink(missing_ok=True)

    def test_verify_text_file_output(self):
        """Test verificación de archivo de texto con salida"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("juan@empresa.cl\n")
            f.write("12.345.678-5\n")
            f.write("plaintext\n")
            txt_path = f.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as out_f:
            json_path = out_f.name

        try:
            result = self.runner.invoke(cli, ["verify", txt_path, "--output", json_path])
            assert result.exit_code == 0
            assert "Verificando archivo:" in result.output
            assert "Reporte guardado en:" in result.output
        finally:
            Path(txt_path).unlink(missing_ok=True)
            Path(json_path).unlink(missing_ok=True)

    def test_batch_command_csv_to_json(self):
        """Test comando batch con salida JSON"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("data\n")
            f.write("juan@empresa.cl\n")
            f.write("12.345.678-5\n")
            csv_path = f.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as out_f:
            json_path = out_f.name

        try:
            result = self.runner.invoke(cli, ["batch", csv_path, "--output", json_path])
            assert result.exit_code == 0
            assert "Procesando en lote:" in result.output
            assert "Reporte completo guardado" in result.output

            # Verificar que el archivo JSON se creó y es válido
            assert Path(json_path).exists()
            with open(json_path) as json_file:
                data = json.load(json_file)
                assert "summary" in data
                assert "results" in data
                assert data["summary"]["total_analyzed"] >= 2
        finally:
            Path(csv_path).unlink(missing_ok=True)
            Path(json_path).unlink(missing_ok=True)

    def test_batch_command_csv_format(self):
        """Test comando batch con salida CSV"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("email,password\n")
            f.write("admin@mail.com,hash123\n")
            f.write("user@empresa.cl,plaintext\n")
            csv_input_path = f.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as out_f:
            csv_output_path = out_f.name

        try:
            result = self.runner.invoke(cli, ["batch", csv_input_path, "--output", csv_output_path, "--format", "csv"])
            assert result.exit_code == 0

            # Verificar que el archivo CSV se creó
            assert Path(csv_output_path).exists()
            with open(csv_output_path) as csv_file:
                content = csv_file.read()
                assert "row,column,original_data" in content
                assert "sensitivity_level" in content
                assert "protection_status" in content
        finally:
            Path(csv_input_path).unlink(missing_ok=True)
            Path(csv_output_path).unlink(missing_ok=True)


class TestCLIErrorHandling:
    """Tests para manejo de errores en CLI"""

    def setup_method(self):
        """Setup para cada test"""
        self.runner = CliRunner()

    def test_analyze_help(self):
        """Test ayuda del comando analyze"""
        result = self.runner.invoke(cli, ["analyze", "--help"])
        assert result.exit_code == 0
        assert "Analizar una entrada individual" in result.output
        assert "--detailed" in result.output
        assert "--format" in result.output

    def test_verify_nonexistent_file(self):
        """Test verificación de archivo inexistente"""
        result = self.runner.invoke(cli, ["verify", "nonexistent.csv"])
        assert result.exit_code == 2  # Click error code para archivo no encontrado

    def test_batch_missing_output(self):
        """Test comando batch sin especificar output (requerido)"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("data\ntest\n")
            csv_path = f.name

        try:
            result = self.runner.invoke(cli, ["batch", csv_path])
            assert result.exit_code == 2  # Click error por parámetro faltante
            assert "Missing option" in result.output or "required" in result.output.lower()
        finally:
            Path(csv_path).unlink(missing_ok=True)

    def test_analyze_empty_string(self):
        """Test análisis de string vacío"""
        result = self.runner.invoke(cli, ["analyze", ""])
        assert result.exit_code == 0
        # Debería manejar gracefully el string vacío
        assert "Analizando:" in result.output


class TestCLIIntegration:
    """Tests de integración para flujos completos"""

    def setup_method(self):
        """Setup para cada test"""
        self.runner = CliRunner()

    def test_complete_workflow_csv_analysis(self):
        """Test flujo completo: CSV -> análisis -> reporte JSON"""
        # Crear CSV de test con datos mixtos
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("tipo,valor\n")
            f.write("email,juan@empresa.cl\n")
            f.write("hash,5d41402abc4b2a76b9719d911017c592\n")
            f.write("rut,12.345.678-5\n")
            f.write("plain,texto_normal\n")
            csv_path = f.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as out_f:
            json_path = out_f.name

        try:
            # Ejecutar batch
            result = self.runner.invoke(cli, ["batch", csv_path, "--output", json_path, "--format", "json"])
            assert result.exit_code == 0

            # Verificar que el reporte contiene los datos esperados
            with open(json_path) as json_file:
                data = json.load(json_file)

                # Verificar estructura del reporte
                assert "summary" in data
                assert "results" in data
                assert "metadata" in data

                # Verificar que detectó diferentes tipos de datos
                results = data["results"]
                found_types = set()

                for result_item in results:
                    if result_item["sensitive_matches"]:
                        for match in result_item["sensitive_matches"]:
                            found_types.add(match["type"])

                # Debería haber detectado al menos email y RUT
                assert "Email" in found_types
                assert "RUT Chileno" in found_types

        finally:
            Path(csv_path).unlink(missing_ok=True)
            Path(json_path).unlink(missing_ok=True)

    def test_performance_large_dataset_simulation(self):
        """Test rendimiento con dataset simulado más grande"""
        # Crear un CSV con más datos para simular carga
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("data\n")
            # Generar múltiples líneas de datos de prueba
            test_data = [
                "juan@empresa.cl",
                "12.345.678-5",
                "5d41402abc4b2a76b9719d911017c592",
                "+56912345678",
                "192.168.1.1",
                "plain text data",
            ] * 10  # 60 elementos total

            for data in test_data:
                f.write(f"{data}\n")

            csv_path = f.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as out_f:
            json_path = out_f.name

        try:
            result = self.runner.invoke(cli, ["batch", csv_path, "--output", json_path])
            assert result.exit_code == 0
            assert "Progreso: 60/60 (100.0%)" in result.output
            assert "Procesamiento completado" in result.output

        finally:
            Path(csv_path).unlink(missing_ok=True)
            Path(json_path).unlink(missing_ok=True)
