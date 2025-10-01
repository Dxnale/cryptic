from cryptic.core.analyzer import CrypticAnalyzer, DataSensitivity, ProtectionStatus


class TestCrypticAnalyzer:
    """Tests para el analizador principal de Cryptic"""

    def setup_method(self):
        """Setup para cada test"""
        self.analyzer = CrypticAnalyzer()

    def test_analyze_hash_data(self):
        """Test análisis de datos que son hashes"""
        # Hash MD5 conocido
        md5_hash = "5d41402abc4b2a76b9719d911017c592"
        analysis = self.analyzer.analyze_data(md5_hash)

        assert analysis.original_data == md5_hash
        assert analysis.protection_status == ProtectionStatus.PROTECTED
        assert analysis.sensitivity_level == DataSensitivity.MEDIUM
        assert analysis.hash_analysis is not None
        assert analysis.confidence > 0.7
        assert "MD5" in str(analysis.recommendations[0])

    def test_analyze_non_hash_data(self):
        """Test análisis de datos que no son hashes"""
        non_hash = "plaintext_password"
        analysis = self.analyzer.analyze_data(non_hash)

        assert analysis.original_data == non_hash
        assert analysis.protection_status == ProtectionStatus.UNKNOWN
        assert analysis.sensitivity_level == DataSensitivity.NONE
        assert analysis.confidence == 0.0

    def test_analyze_batch(self):
        """Test análisis en lote"""
        test_data = [
            "5d41402abc4b2a76b9719d911017c592",  # MD5
            "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",  # SHA-1
            "plaintext",  # No hash
        ]

        results = self.analyzer.analyze_batch(test_data)

        assert len(results) == 3
        assert results[0].protection_status == ProtectionStatus.PROTECTED
        assert results[1].protection_status == ProtectionStatus.PROTECTED
        assert results[2].protection_status == ProtectionStatus.UNKNOWN

    def test_generate_report(self):
        """Test generación de reportes"""
        test_data = [
            "5d41402abc4b2a76b9719d911017c592",  # MD5
            "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",  # SHA-1
            "*A4B6157319038724E3560894F7F932C8886EBFCF",  # MySQL5
            "plaintext",  # No hash
        ]

        analyses = self.analyzer.analyze_batch(test_data)
        report = self.analyzer.generate_report(analyses)

        assert report["total_analyzed"] == 4
        assert report["protected"] == 3
        assert report["unprotected"] == 0  # plaintext es UNKNOWN, no UNPROTECTED
        assert report["protection_rate"] == 0.75
        assert "hash_types_detected" in report
        assert "MD5" in report["hash_types_detected"]
        assert "SHA-1" in report["hash_types_detected"]

    def test_print_analysis(self, capsys):
        """Test impresión de análisis"""
        hash_data = "5d41402abc4b2a76b9719d911017c592"
        analysis = self.analyzer.analyze_data(hash_data)

        self.analyzer.print_analysis(analysis, detailed=True)
        captured = capsys.readouterr()

        assert "Cryptic Analysis for:" in captured.out
        assert "Sensitivity Level:" in captured.out
        assert "Protection Status:" in captured.out
        assert "Hash Analysis:" in captured.out
        assert "Recommendations:" in captured.out
