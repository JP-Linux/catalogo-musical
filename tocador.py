import subprocess


def tocar(link, video=False, volume=80):
    imagem = "--no-video"
    if video:
        imagem = ""

    command = [
        'mpv',
        imagem,
        f'--volume={volume}',
        link
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        # print("Comando executado com sucesso")
        result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {e}")
        print(f"Saída de erro: {e.stderr}")
    except FileNotFoundError:
        print("Comando mpv não encontrado. Verifique se está instalado.")
