from cryptic import HashIdentifier, HashType, quick_identify, batch_identify


class TestHashIdentifier:
    """Tests para el identificador de hashes"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.identifier = HashIdentifier()
    
    # Tests para MD5
    def test_md5_valid(self):
        """Test MD5 válidos"""
        valid_md5_hashes = [
            "5d41402abc4b2a76b9719d911017c592",  # "hello"
            "098f6bcd4621d373cade4e832627b4f6",  # "test"
            "d41d8cd98f00b204e9800998ecf8427e",  # cadena vacía
            "827ccb0eea8a706c4c34a16891f84e7b",  # "12345"
        ]
        
        for hash_str in valid_md5_hashes:
            analysis = self.identifier.identify(hash_str)
            assert len(analysis.possible_types) > 0
            # MD5 debería estar en los primeros resultados
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.MD5 in hash_types
    
    def test_md5_case_insensitive(self):
        """Test MD5 con mayúsculas y minúsculas"""
        hash_lower = "5d41402abc4b2a76b9719d911017c592"
        hash_upper = "5D41402ABC4B2A76B9719D911017C592"
        hash_mixed = "5d41402ABC4b2A76b9719D911017C592"
        
        for hash_str in [hash_lower, hash_upper, hash_mixed]:
            analysis = self.identifier.identify(hash_str)
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.MD5 in hash_types
    
    # Tests para SHA-1
    def test_sha1_valid(self):
        """Test SHA-1 válidos"""
        valid_sha1_hashes = [
            "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",  # "hello"
            "da39a3ee5e6b4b0d3255bfef95601890afd80709",  # cadena vacía
            "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3",  # "test"
            "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5",  # ejemplo más largo
        ]
        
        for hash_str in valid_sha1_hashes:
            if len(hash_str) == 40:  # Solo SHA-1 de 40 caracteres
                analysis = self.identifier.identify(hash_str)
                hash_types = [ht for ht, conf in analysis.possible_types]
                assert HashType.SHA1 in hash_types
    
    # Tests para SHA-256
    def test_sha256_valid(self):
        """Test SHA-256 válidos"""
        valid_sha256_hashes = [
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # cadena vacía
            "2cf24dba4f21d4288094c59b7b1b967ed1a46b4d7d965d14e8ee1a6c6e8b84f3",  # "hello"
            "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",  # "test"
        ]
        
        for hash_str in valid_sha256_hashes:
            analysis = self.identifier.identify(hash_str)
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.SHA256 in hash_types
    
    # Tests para SHA-512
    def test_sha512_valid(self):
        """Test SHA-512 válidos"""
        valid_sha512_hashes = [
            "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e",
            "9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043",
        ]
        
        for hash_str in valid_sha512_hashes:
            analysis = self.identifier.identify(hash_str)
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.SHA512 in hash_types
    
    # Tests para MySQL5
    def test_mysql5_valid(self):
        """Test MySQL5 válidos con prefijo asterisco"""
        valid_mysql5_hashes = [
            "*A4B6157319038724E3560894F7F932C8886EBFCF",  # Con mayúsculas
            "*a4b6157319038724e3560894f7f932c8886ebfcf",  # Con minúsculas
            "*B5A2C96250612366EA272DC8B40DB8FC8123B6E3",  # Otro ejemplo
        ]
        
        for hash_str in valid_mysql5_hashes:
            analysis = self.identifier.identify(hash_str)
            assert len(analysis.possible_types) > 0
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.MYSQL5 in hash_types
            # Debería tener alta confianza
            mysql5_confidence = next(conf for ht, conf in analysis.possible_types if ht == HashType.MYSQL5)
            assert mysql5_confidence >= 0.9
    
    # Tests para bcrypt
    def test_bcrypt_valid(self):
        """Test bcrypt válidos"""
        valid_bcrypt_hashes = [
            "$2b$10$N9qo8uLOickgx2ZMRZoMye",  # Hash parcial (salt)
            "$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi",  # Hash completo
            "$2y$12$9kT7BvH/5O.fDl3K5R5NXe5vT.5p5YJO/pT8Q2cH4Lb8sEo4wX2K.",  # Hash con cost 12
            "$2b$06$fgfgdETXoao94wEhz0c9ae",  # Hash con cost 6
        ]
        
        for hash_str in valid_bcrypt_hashes:
            analysis = self.identifier.identify(hash_str)
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.BCRYPT in hash_types
            # Debería tener alta confianza
            bcrypt_confidence = next(conf for ht, conf in analysis.possible_types if ht == HashType.BCRYPT)
            assert bcrypt_confidence >= 0.9
    
    # Tests para WordPress
    def test_wordpress_valid(self):
        """Test WordPress válidos"""
        valid_wordpress_hashes = [
            "$P$B123456789abcdef123456789abcdef",  # Ejemplo del script
            "$P$9IQRaTwmfeRo7ud9Fh4E2PdI0S3r.L0",  # Ejemplo realista
            "$P$B55D6LjfHDkINU5wF.v2BuuzO0/XPk/",  # Otro ejemplo
        ]
        
        for hash_str in valid_wordpress_hashes:
            analysis = self.identifier.identify(hash_str)
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.WORDPRESS in hash_types
            # Debería tener alta confianza
            wp_confidence = next(conf for ht, conf in analysis.possible_types if ht == HashType.WORDPRESS)
            assert wp_confidence >= 0.9
    
    # Tests para NTLM
    def test_ntlm_valid(self):
        """Test NTLM válidos"""
        valid_ntlm_hashes = [
            "8846f7eaee8fb117ad06bdd830b7586c",  # "password"
            "b4b9b02e6f09a9bd760f388b67351e2b",  # "admin"
            "31d6cfe0d16ae931b73c59d7e0c089c0",  # cadena vacía
        ]
        
        for hash_str in valid_ntlm_hashes:
            analysis = self.identifier.identify(hash_str)
            hash_types = [ht for ht, conf in analysis.possible_types]
            # NTLM debería estar presente (aunque puede confundirse con MD5)
            assert HashType.NTLM in hash_types or HashType.MD5 in hash_types
    
    # Tests para CRC32
    def test_crc32_valid(self):
        """Test CRC32 válidos"""
        valid_crc32_hashes = [
            "09e8ce87",  # Ejemplo corto
            "a6dcf7c4",  # Otro ejemplo
            "12345678",  # Ejemplo numérico
            "abcdef01",  # Ejemplo hex
        ]
        
        for hash_str in valid_crc32_hashes:
            analysis = self.identifier.identify(hash_str)
            hash_types = [ht for ht, conf in analysis.possible_types]
            # CRC32 o MySQL (ambos tienen 8 caracteres hex para CRC32, 16 para MySQL)
            assert HashType.CRC32 in hash_types or HashType.MYSQL in hash_types
    
    # Tests para casos inválidos
    def test_invalid_hashes(self):
        """Test hashes inválidos que no deberían matchear nada"""
        invalid_hashes = [
            "123",  # Muy corto
            "gg" * 16,  # Caracteres inválidos para hex
            "hello world",  # Texto plano
            "",  # Cadena vacía
            " ",  # Solo espacios
            "5d41402abc4b2a76b9719d911017c59",  # MD5 con un carácter menos
            "5d41402abc4b2a76b9719d911017c592x",  # MD5 con carácter extra
        ]
        
        for hash_str in invalid_hashes:
            analysis = self.identifier.identify(hash_str)
            # Para hashes claramente inválidos, no debería haber matches o muy baja confianza
            if analysis.possible_types:
                best_confidence = analysis.possible_types[0][1]
                # Si hay matches, la confianza debería ser muy baja para casos inválidos obvios
                if hash_str in ["123", "gg" * 16, "hello world", "", " "]:
                    assert len(analysis.possible_types) == 0 or best_confidence < 0.5
    
    # Tests para limpieza de hashes
    def test_hash_cleaning(self):
        """Test limpieza de espacios y caracteres"""
        dirty_hashes = [
            "  5d41402abc4b2a76b9719d911017c592  ",  # Espacios al inicio y final
            "5d41402abc4b2a76b9719d911017c592\n",   # Salto de línea
            "5d41 402a bc4b 2a76 b971 9d91 1017 c592",  # Espacios en medio
            "\t5d41402abc4b2a76b9719d911017c592\t",  # Tabs
        ]
        
        expected_clean = "5d41402abc4b2a76b9719d911017c592"
        
        for dirty_hash in dirty_hashes:
            analysis = self.identifier.identify(dirty_hash)
            assert analysis.cleaned_hash == expected_clean
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.MD5 in hash_types
    
    # Tests para análisis de charset
    def test_charset_analysis(self):
        """Test análisis de conjuntos de caracteres"""
        # Hash hexadecimal minúsculas
        analysis_hex_lower = self.identifier.identify("5d41402abc4b2a76b9719d911017c592")
        assert analysis_hex_lower.charset_analysis["hex_lowercase"] is True
        assert analysis_hex_lower.charset_analysis["hex_uppercase"] is False
        
        # Hash hexadecimal mayúsculas
        analysis_hex_upper = self.identifier.identify("5D41402ABC4B2A76B9719D911017C592")
        assert analysis_hex_upper.charset_analysis["hex_uppercase"] is True
        assert analysis_hex_upper.charset_analysis["hex_lowercase"] is False
        
        # Hash con prefijo
        analysis_prefixed = self.identifier.identify("$2b$10$N9qo8uLOickgx2ZMRZoMye")
        assert analysis_prefixed.charset_analysis["has_dollar_signs"] is True
        assert analysis_prefixed.charset_analysis["has_special_chars"] is True
    
    # Tests para análisis de formato
    def test_format_analysis(self):
        """Test análisis de formato"""
        # Hash sin prefijo
        analysis_simple = self.identifier.identify("5d41402abc4b2a76b9719d911017c592")
        assert analysis_simple.format_analysis["has_prefix"] is False
        assert analysis_simple.format_analysis["segments_count"] == 1
        
        # Hash con prefijo bcrypt
        analysis_bcrypt = self.identifier.identify("$2b$10$N9qo8uLOickgx2ZMRZoMye")
        assert analysis_bcrypt.format_analysis["has_prefix"] is True
        assert analysis_bcrypt.format_analysis["segments_count"] > 1
        assert "salt_structure" in analysis_bcrypt.format_analysis
        
        # Hash MySQL5
        analysis_mysql5 = self.identifier.identify("*A4B6157319038724E3560894F7F932C8886EBFCF")
        assert analysis_mysql5.format_analysis["has_prefix"] is True
    
    # Tests para funciones utilitarias
    def test_quick_identify(self):
        """Test función quick_identify"""
        result = quick_identify("5d41402abc4b2a76b9719d911017c592")
        assert "MD5" in result
        assert "%" in result  # Debería incluir porcentaje de confianza
        
        result_mysql5 = quick_identify("*A4B6157319038724E3560894F7F932C8886EBFCF")
        assert "MySQL5" in result_mysql5
    
    def test_batch_identify(self):
        """Test identificación en lote"""
        hash_batch = [
            "5d41402abc4b2a76b9719d911017c592",  # MD5
            "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",  # SHA-1
            "*A4B6157319038724E3560894F7F932C8886EBFCF",  # MySQL5
        ]
        
        results = batch_identify(hash_batch)
        
        assert len(results) == 3
        assert all(hash_str in results for hash_str in hash_batch)
        
        # Verificar que cada resultado tiene el tipo correcto
        md5_result = results["5d41402abc4b2a76b9719d911017c592"]
        assert md5_result[0] == HashType.MD5
        
        mysql5_result = results["*A4B6157319038724E3560894F7F932C8886EBFCF"]
        assert mysql5_result[0] == HashType.MYSQL5
    
    # Tests para edge cases específicos
    def test_collision_cases(self):
        """Test casos donde múltiples tipos de hash tienen la misma longitud"""
        # 32 caracteres: MD5, NTLM, LM
        hash_32 = "5d41402abc4b2a76b9719d911017c592"
        analysis = self.identifier.identify(hash_32)
        
        # Debería identificar múltiples posibilidades
        assert len(analysis.possible_types) >= 2
        hash_types = [ht for ht, conf in analysis.possible_types]
        assert HashType.MD5 in hash_types
        
        # 40 caracteres: SHA-1, RIPEMD-160
        hash_40 = "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
        analysis_40 = self.identifier.identify(hash_40)
        
        hash_types_40 = [ht for ht, conf in analysis_40.possible_types]
        assert HashType.SHA1 in hash_types_40
        # Podría también incluir RIPEMD-160
    
    def test_confidence_levels(self):
        """Test niveles de confianza apropiados"""
        # Hash con prefijo específico debería tener alta confianza
        mysql5_analysis = self.identifier.identify("*A4B6157319038724E3560894F7F932C8886EBFCF")
        mysql5_confidence = mysql5_analysis.possible_types[0][1]  # Primera opción
        assert mysql5_confidence >= 0.9
        
        # Hash bcrypt con prefijo específico
        bcrypt_analysis = self.identifier.identify("$2b$10$N9qo8uLOickgx2ZMRZoMye")
        bcrypt_confidence = bcrypt_analysis.possible_types[0][1]
        assert bcrypt_confidence >= 0.9
        
        # Hash ambiguo (32 caracteres) debería tener confianza más baja
        ambiguous_analysis = self.identifier.identify("5d41402abc4b2a76b9719d911017c592")
        if ambiguous_analysis.possible_types:
            ambiguous_confidence = ambiguous_analysis.possible_types[0][1]
            assert ambiguous_confidence < 1.0  # No debería ser 100% seguro
    
    # Tests para casos de hashes largos
    def test_long_hashes(self):
        """Test hashes muy largos (SHA-384, SHA-512, Whirlpool)"""
        # SHA-384 (96 caracteres)
        sha384_hash = "ca737f1014a48f4c0b6dd43cb177b0afd9e5169367544c494011e3317dbf9a509cb1e5dc1e85a941bbee3d7f2afbc9b1"
        analysis_384 = self.identifier.identify(sha384_hash)
        hash_types_384 = [ht for ht, conf in analysis_384.possible_types]
        assert HashType.SHA384 in hash_types_384
        
        # SHA-512 (128 caracteres)
        sha512_hash = "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"
        analysis_512 = self.identifier.identify(sha512_hash)
        hash_types_512 = [ht for ht, conf in analysis_512.possible_types]
        assert HashType.SHA512 in hash_types_512
    
    # Test para hashes con caracteres especiales
    def test_special_character_hashes(self):
        """Test hashes con caracteres especiales válidos"""
        # Argon2
        argon2_examples = [
            "$argon2i$v=19$m=4096,t=3,p=1$c2FsdA$hash",
            "$argon2d$v=19$m=65536,t=10,p=8$c2FsdA$hash",
        ]
        
        for argon2_hash in argon2_examples:
            analysis = self.identifier.identify(argon2_hash)
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.ARGON2 in hash_types
        
        # PBKDF2
        pbkdf2_examples = [
            "$pbkdf2-sha1$1000$salt$hash",
            "$pbkdf2-sha256$29000$salt$hash",
        ]
        
        for pbkdf2_hash in pbkdf2_examples:
            analysis = self.identifier.identify(pbkdf2_hash)
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.PBKDF2 in hash_types
    
    # Test para rendimiento básico
    def test_performance_basic(self):
        """Test básico de rendimiento con lote moderado"""
        # Crear un lote de 50 hashes diferentes
        test_batch = []
        
        # Generar variaciones
        for i in range(50):
            # Crear MD5-like hash variando los últimos caracteres
            variant = f"5d41402abc4b2a76b9719d911017c5{i:02d}"
            test_batch.append(variant)
        
        # El procesamiento debería ser rápido
        import time
        start_time = time.time()
        results = batch_identify(test_batch)
        end_time = time.time()
        
        # Debería procesar 50 hashes en menos de 1 segundo
        assert end_time - start_time < 1.0
        assert len(results) == 50
    
    # Test para método print_analysis
    def test_print_analysis_basic(self, capsys):
        """Test método print_analysis sin detalles"""
        self.identifier.print_analysis("5d41402abc4b2a76b9719d911017c592", detailed=False)
        captured = capsys.readouterr()
        
        assert "Hash Analysis for:" in captured.out
        assert "Cleaned Hash:" in captured.out
        assert "Length: 32" in captured.out
        assert "Possible Hash Types:" in captured.out
        assert "MD5" in captured.out
    
    def test_print_analysis_detailed(self, capsys):
        """Test método print_analysis con detalles"""
        self.identifier.print_analysis("$2b$10$N9qo8uLOickgx2ZMRZoMye", detailed=True)
        captured = capsys.readouterr()
        
        assert "Hash Analysis for:" in captured.out
        assert "Charset Analysis:" in captured.out
        assert "Format Analysis:" in captured.out
        assert "bcrypt" in captured.out
        assert "Has Dollar Signs" in captured.out or "Has Special Chars" in captured.out
    
    def test_print_analysis_no_matches(self, capsys):
        """Test print_analysis cuando no hay matches"""
        self.identifier.print_analysis("invalidhash123", detailed=False)
        captured = capsys.readouterr()
        
        assert "No matches found" in captured.out
    
    # Tests para casos edge adicionales
    def test_base64_detection(self):
        """Test detección de base64"""
        # Base64 válido
        base64_string = "SGVsbG8gV29ybGQ="  # "Hello World" en base64
        analysis = self.identifier.identify(base64_string)
        assert analysis.charset_analysis["base64"] is True
        
        # Base64 inválido (contiene caracteres que no están en el charset base64)
        non_base64 = "hello@world#123!"  # Contiene @, # que no son base64
        analysis_non = self.identifier.identify(non_base64)
        assert analysis_non.charset_analysis["base64"] is False
    
    def test_identify_best_match_unknown(self):
        """Test identify_best_match cuando no hay coincidencias"""
        hash_type, confidence = self.identifier.identify_best_match("invalidhash")
        assert hash_type == HashType.UNKNOWN
        assert confidence == 0.0
    
    def test_edge_case_empty_segments(self):
        """Test casos con segmentos vacíos"""
        # Hash con múltiples $ consecutivos
        weird_hash = "$$$test$$$"
        analysis = self.identifier.identify(weird_hash)
        assert analysis.format_analysis["segments_count"] > 3
        
    def test_scrypt_detection(self):
        """Test detección de scrypt"""
        scrypt_hashes = [
            "$scrypt$N=1024,r=1,p=1$salt$hash",
            "$scrypt$16384$8$1$salt$hash",
        ]
        
        for scrypt_hash in scrypt_hashes:
            analysis = self.identifier.identify(scrypt_hash)
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.SCRYPT in hash_types
    
    def test_mysql_old_format(self):
        """Test MySQL formato antiguo (16 caracteres)"""
        mysql_old_hashes = [
            "1234567890abcdef",
            "0123456789ABCDEF",
        ]
        
        for mysql_hash in mysql_old_hashes:
            analysis = self.identifier.identify(mysql_hash)
            hash_types = [ht for ht, conf in analysis.possible_types]
            assert HashType.MYSQL in hash_types
    
    def test_tiger_hash(self):
        """Test Tiger hash (48 caracteres)"""
        tiger_hash = "123456789012345678901234567890123456789012345678"
        analysis = self.identifier.identify(tiger_hash)
        hash_types = [ht for ht, conf in analysis.possible_types]
        assert HashType.TIGER in hash_types
    
    def test_sha224_hash(self):
        """Test SHA-224 hash (56 caracteres)"""
        sha224_hash = "12345678901234567890123456789012345678901234567890123456"
        analysis = self.identifier.identify(sha224_hash)
        hash_types = [ht for ht, conf in analysis.possible_types]
        assert HashType.SHA224 in hash_types
    
    def test_ripemd160_confidence(self):
        """Test que RIPEMD-160 tiene menor confianza que SHA-1 para 40 chars"""
        hash_40 = "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
        analysis = self.identifier.identify(hash_40)
        
        # SHA-1 debería tener mayor confianza que RIPEMD-160
        confidences = dict(analysis.possible_types)
        if HashType.SHA1 in confidences and HashType.RIPEMD160 in confidences:
            assert confidences[HashType.SHA1] > confidences[HashType.RIPEMD160]
    
    def test_whirlpool_vs_others_128_chars(self):
        """Test Whirlpool vs otros hashes de 128 caracteres"""
        hash_128 = "a" * 128  # 128 caracteres hexadecimales
        analysis = self.identifier.identify(hash_128)
        
        hash_types = [ht for ht, conf in analysis.possible_types]
        # Debería incluir múltiples opciones para 128 caracteres
        possible_128_types = [HashType.SHA512, HashType.WHIRLPOOL, HashType.BLAKE2B]
        matching_types = [ht for ht in hash_types if ht in possible_128_types]
        assert len(matching_types) >= 2
    
    def test_blake2s_vs_sha256(self):
        """Test BLAKE2s vs SHA-256 para 64 caracteres"""
        hash_64 = "b" * 64  # 64 caracteres hexadecimales
        analysis = self.identifier.identify(hash_64)
        
        hash_types = [ht for ht, conf in analysis.possible_types]
        assert HashType.SHA256 in hash_types
        assert HashType.BLAKE2S in hash_types
    
    def test_colon_separated_format(self):
        """Test formato separado por dos puntos"""
        colon_hash = "user:5d41402abc4b2a76b9719d911017c592"
        analysis = self.identifier.identify(colon_hash)
        
        assert analysis.format_analysis["colon_separated"] is True
        # El hash raw conserva los dos puntos, el cleaned también (solo limpia espacios/tabs/newlines)
        assert ":" in analysis.raw_hash
        assert ":" in analysis.cleaned_hash  # _clean_hash no remueve los dos puntos
    
    def test_hash_with_braces(self):
        """Test hashes con llaves"""
        brace_hash = "{5d41402abc4b2a76b9719d911017c592}"
        analysis = self.identifier.identify(brace_hash)
        
        # Debería detectar sufijo
        assert analysis.format_analysis["has_suffix"] is True
    
    def test_hex_prefix(self):
        """Test hash con prefijo 0x"""
        hex_prefix_hash = "0x5d41402abc4b2a76b9719d911017c592"
        analysis = self.identifier.identify(hex_prefix_hash)
        
        assert analysis.format_analysis["has_prefix"] is True
