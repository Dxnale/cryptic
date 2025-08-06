from saludador import saludar

def test_funcion_saludar():
    assert saludar("Mundo") == "Hola Mundo esta es mi primera funcion importable en python!"
    assert saludar("Test") == "Hola Test esta es mi primera funcion importable en python!"
