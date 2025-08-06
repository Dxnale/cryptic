import subprocess

COMMAND_NAME = "saludador"

def test_cli_con_argumento():
    result = subprocess.run(
        [COMMAND_NAME, "Amigo"],
        capture_output=True,
        text=True,
        check=True
    )
    assert result.stdout.strip() == "Hola Amigo esta es mi primera funcion importable en python!"

def test_cli_sin_argumento_falla():
    result = subprocess.run(
        [COMMAND_NAME],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0
    assert 'error: the following arguments are required: name' in result.stderr
