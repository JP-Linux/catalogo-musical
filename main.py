from dataclasses import dataclass
from typing import List, Optional
from Banco_Dados import BancoDeDadosMusica
from tocador import tocar
from random import shuffle


@dataclass
class Artista:
    id: int
    nome: str

    def __str__(self):
        return self.nome


@dataclass
class Genero:
    id: int
    nome: str

    def __str__(self):
        return self.nome


@dataclass
class Musica:
    id: int
    titulo: str
    url: str
    artista_id: int
    genero_id: int
    artista_nome: Optional[str] = None
    genero_nome: Optional[str] = None

    def tocar(self, video=False, volume=80):
        """Comportamento da música"""
        print(f"Tocando: {self.titulo}")
        tocar(link=self.url, video=video, volume=volume)

    def __str__(self):
        return f"{self.artista_nome or ''} - {self.titulo}"


class CatalogoMusical:
    """Gerencia o catálogo de músicas"""

    def __init__(self):
        self.db = BancoDeDadosMusica("musicas.db")
        self._musicas = []
        self._artistas = []
        self._generos = []

    def adicionar_musica(self, titulo: str, url: str, artista: str, genero: str) -> Musica:
        """Adiciona uma nova música ao catálogo"""
        artista_id = self.db.adicionar_artista(artista)
        genero_id = self.db.adicionar_genero(genero)
        musica_id = self.db.adicionar_musica(
            artista_id, titulo, url, genero_id)

        musica = Musica(
            id=musica_id,
            titulo=titulo,
            url=url,
            artista_id=artista_id,
            genero_id=genero_id,
            artista_nome=artista,
            genero_nome=genero
        )
        self._musicas.append(musica)
        return musica

    def buscar_musicas(self) -> List[Musica]:
        """Retorna todas as músicas"""
        dados = self.db.obter_todas_musicas()
        return [
            Musica(
                id=m['id'],
                titulo=m['titulo'],
                url=m['url'],
                artista_id=m['artista_id'],
                genero_id=m['genero_id'],
                artista_nome=m['artista_nome'],
                genero_nome=m['genero_nome']
            ) for m in dados
        ]

    def buscar_por_artista(self, artista_id: int) -> List[Musica]:
        """Busca músicas por artista"""
        dados = self.db.obter_musicas_por_artista(artista_id)
        return [
            Musica(
                id=m['id'],
                titulo=m['titulo'],
                url=m['url'],
                artista_id=m['artista_id'],
                genero_id=m['genero_id'],
                artista_nome=m['artista_nome'],
                genero_nome=m['genero_nome']
            ) for m in dados
        ]

    def buscar_por_genero(self, genero_id: int) -> List[Musica]:
        """Busca músicas por gênero"""
        dados = self.db.obter_musicas_por_genero(genero_id)
        return [
            Musica(
                id=m['id'],
                titulo=m['titulo'],
                url=m['url'],
                artista_id=m['artista_id'],
                genero_id=m['genero_id'],
                artista_nome=m['artista_nome'],
                genero_nome=m['genero_nome']
            ) for m in dados
        ]

    def listar_artistas(self) -> List[Artista]:
        """Lista todos os artistas"""
        dados = self.db.obter_todos_artistas()
        return [Artista(id=a['id'], nome=a['nome']) for a in dados]

    def listar_generos(self) -> List[Genero]:
        """Lista todos os gêneros"""
        dados = self.db.obter_todos_generos()
        return [Genero(id=g['id'], nome=g['nome']) for g in dados]

    def estatisticas(self) -> dict:
        """Retorna estatísticas do catálogo"""
        return self.db.obter_estatisticas()

    def fechar(self):
        """Fecha a conexão com o banco"""
        self.db.fechar()


class Player:
    """Controla a reprodução de músicas"""

    def __init__(self):
        self.video = False
        self.volume = 80
        self._playlist_atual = []

    def criar_playlist(self, musicas: List[Musica]):
        """Cria uma nova playlist"""
        self._playlist_atual = musicas

    def exibir_playlist(self):
        """Exibe a playlist atual"""
        print("\n===--- Playlist ---===\n")
        for i, musica in enumerate(self._playlist_atual, 1):
            print(f"[{i}] {musica}")

    def tocar_playlist(self):
        """Toca a playlist atual"""
        if not self._playlist_atual:
            print("Playlist vazia!")
            return

        self.exibir_playlist()
        for musica in self._playlist_atual:
            musica.tocar(video=self.video, volume=self.volume)

    def tocar_musicas(self, musicas: List[Musica], aleatorio: bool):
        """Toca uma lista de músicas"""
        if aleatorio:
            shuffle(musicas)
        self.criar_playlist(musicas)
        self.tocar_playlist()


class ServicoMusical:
    """Orquestra os serviços musicais"""

    def __init__(self):
        self.catalogo = CatalogoMusical()
        self.player = Player()

    def adicionar_musica(self, titulo: str, url: str, artista: str, genero: str):
        """Adiciona uma música ao catálogo"""
        return self.catalogo.adicionar_musica(titulo, url, artista, genero)

    def tocar_todas(self):
        """Toca todas as músicas do catálogo"""
        musicas = self.catalogo.buscar_musicas()
        self.player.tocar_musicas(musicas)

    def tocar_por_artista(self, artista_id: int, aleatorio: bool):
        """Toca músicas de um artista"""
        musicas = self.catalogo.buscar_por_artista(artista_id)
        self.player.tocar_musicas(musicas, aleatorio)

    def tocar_por_genero(self, genero_id: int, aleatorio: bool):
        """Toca músicas de um gênero"""
        musicas = self.catalogo.buscar_por_genero(genero_id)
        self.player.tocar_musicas(musicas, aleatorio)

    def fechar(self):
        """Fecha todos os recursos"""
        self.catalogo.fechar()


class InterfaceUsuario:
    """Gerencia a interface com o usuário"""

    def __init__(self):
        self.servico = ServicoMusical()
        self.executando = True

    def exibir_menu(self):
        """Exibe o menu principal"""
        print("\n" + "="*40)
        print("🎵  PLAYER MUSICAL  🎵")
        print("="*40)
        print("[1] Adicionar Música")
        print("[2] Listar Todas as Músicas")
        print("[3] Tocar Todas as Músicas")
        print("[4] Tocar por Gênero")
        print("[5] Tocar por Artista")
        print("[6] Estatísticas")
        print("[7] Sair")
        print("-"*40)

    def selecionar_opcao(self, opcoes: list, titulo: str = "Selecione uma opção"):
        """Exibe uma lista de opções para seleção"""
        print(f"\n=== {titulo} ===")
        for i, opcao in enumerate(opcoes, 1):
            print(f"[{i}] {opcao}")
        print(f"[{len(opcoes) + 1}] Cancelar")

        try:
            escolha = int(input(f"\nOpção [1-{len(opcoes) + 1}]: "))
            if 1 <= escolha <= len(opcoes):
                return opcoes[escolha - 1]
        except ValueError:
            pass
        return None

    def adicionar_musica(self):
        """Interface para adicionar música"""
        print("\n➕ ADICIONAR MÚSICA")
        print("-"*30)

        titulo = input("Título: ")
        url = input("URL: ")

        # Sugerir artista existente ou novo
        artistas = self.servico.catalogo.listar_artistas()
        if artistas:
            artista_obj = self.selecionar_opcao(
                artistas,
                "Selecione o artista ou adicione novo"
            )
            artista = artista_obj.nome if artista_obj else input("Artista: ")
        else:
            artista = input("Artista: ")

        # Sugerir gênero existente ou novo
        generos = self.servico.catalogo.listar_generos()
        if generos:
            genero_obj = self.selecionar_opcao(
                generos,
                "Selecione o gênero ou adicione novo"
            )
            genero = genero_obj.nome if genero_obj else input("Gênero: ")
        else:
            genero = input("Gênero: ")

        # Confirmação
        print("\n📋 RESUMO:")
        print(f"Título: {titulo}")
        print(f"Artista: {artista}")
        print(f"Gênero: {genero}")

        if input("\nConfirmar? (s/n): ").lower() == 's':
            musica = self.servico.adicionar_musica(
                titulo, url, artista, genero)
            print(f"✅ Música '{musica.titulo}' adicionada com sucesso!")

    def listar_musicas(self):
        """Lista todas as músicas"""
        musicas = self.servico.catalogo.buscar_musicas()
        print("\n📋 TODAS AS MÚSICAS")
        print("-"*50)
        for musica in musicas:
            print(f"• {musica}")

    def tocar_por_genero(self):
        """Interface para tocar por gênero"""
        generos = self.servico.catalogo.listar_generos()
        if not generos:
            print("Nenhum gênero cadastrado!")
            return

        genero = self.selecionar_opcao(generos, "SELECIONE UM GÊNERO")
        if genero:
            self.servico.tocar_por_genero(genero.id, self.modo_aleatorio)

    def tocar_por_artista(self):
        """Interface para tocar por artista"""
        artistas = self.servico.catalogo.listar_artistas()
        if not artistas:
            print("Nenhum artista cadastrado!")
            return

        artista = self.selecionar_opcao(artistas, "SELECIONE UM ARTISTA")
        if artista:
            self.servico.tocar_por_artista(artista.id, self.modo_aleatorio)

    def mostrar_estatisticas(self):
        """Mostra estatísticas do catálogo"""
        stats = self.servico.catalogo.estatisticas()
        print("\n📊 ESTATÍSTICAS")
        print("-"*30)
        print(f"🎵 Músicas: {stats['musicas']}")
        print(f"🎤 Artistas: {stats['artistas']}")
        print(f"🎭 Gêneros: {stats['generos']}")

    def aleatorio(self):
        ativar = input("Ativar modo aleatório?[S/n]: ").lower()
        if "s" in ativar:
            return True
        return False

    def executar(self):
        """Loop principal da aplicação"""
        while self.executando:
            self.exibir_menu()

            try:
                opcao = int(input("\nEscolha uma opção: "))

                if opcao >= 3 and opcao <= 5:
                    # Opção para tocar músicas de forma aleatória
                    self.modo_aleatorio = self.aleatorio()

                if opcao == 1:
                    self.adicionar_musica()
                elif opcao == 2:
                    self.listar_musicas()
                elif opcao == 3:
                    self.servico.tocar_todas(self.modo_aleatorio)
                elif opcao == 4:
                    self.tocar_por_genero()
                elif opcao == 5:
                    self.tocar_por_artista()
                elif opcao == 6:
                    self.mostrar_estatisticas()
                elif opcao == 7:
                    self.executando = False
                else:
                    print("Opção inválida!")

            except ValueError:
                print("Por favor, digite um número válido!")
            except Exception as e:
                print(f"Erro: {e}")

        # Encerramento
        self.servico.fechar()
        print("\n👋 Até logo!")


if __name__ == "__main__":
    app = InterfaceUsuario()
    app.executar()
