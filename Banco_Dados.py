import sqlite3
from typing import List, Dict, Optional, Tuple, Any


class BancoDeDadosMusica:
    """
    Classe para gerenciar o banco de dados SQLite para músicas, artistas e gêneros.
    """

    def __init__(self, nome_banco: str = 'musicas.db'):
        """
        Inicializa a conexão com o banco de dados e cria as tabelas se não existirem.

        Args:
            nome_banco (str): Nome do arquivo do banco de dados SQLite
        """
        self.nome_banco = nome_banco
        self.conexao = None
        self.cursor = None
        self.conectar()
        self.criar_tabelas()

    def conectar(self) -> None:
        """Conecta ao banco de dados SQLite."""
        try:
            self.conexao = sqlite3.connect(self.nome_banco)
            self.conexao.row_factory = sqlite3.Row  # Permite acessar colunas por nome
            self.cursor = self.conexao.cursor()
            print(f"Conectado ao banco de dados: {self.nome_banco}")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def criar_tabelas(self) -> None:
        """Cria as tabelas se não existirem."""
        try:
            # Tabela para artistas/bandas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS artistas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
            ''')

            # Tabela para gêneros musicais
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS generos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
            ''')

            # Tabela principal de músicas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS musicas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    artista_id INTEGER NOT NULL,
                    titulo TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    genero_id INTEGER NOT NULL,
                    FOREIGN KEY (artista_id) REFERENCES artistas(id),
                    FOREIGN KEY (genero_id) REFERENCES generos(id)
                )
            ''')

            self.conexao.commit()
            print("Tabelas criadas com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")
            self.conexao.rollback()
            raise

    def fechar(self) -> None:
        """Fecha a conexão com o banco de dados."""
        if self.conexao:
            self.conexao.close()
            print("Conexão com o banco de dados fechada.")

    def __enter__(self):
        """Suporte para contexto (with statement)."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha a conexão automaticamente ao sair do contexto."""
        self.fechar()

    # Métodos para Artistas
    def adicionar_artista(self, nome: str) -> Optional[int]:
        """
        Adiciona um novo artista ao banco de dados.

        Args:
            nome (str): Nome do artista

        Returns:
            Optional[int]: ID do artista criado ou None se falhar
        """
        try:
            self.cursor.execute(
                "INSERT INTO artistas (nome) VALUES (?)",
                (nome,)
            )
            self.conexao.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Artista já existe
            self.cursor.execute(
                "SELECT id FROM artistas WHERE nome = ?", (nome,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Erro ao adicionar artista: {e}")
            self.conexao.rollback()
            return None

    def obter_artista_por_id(self, artista_id: int) -> Optional[Dict]:
        """
        Obtém um artista pelo ID.

        Args:
            artista_id (int): ID do artista

        Returns:
            Optional[Dict]: Dicionário com dados do artista ou None
        """
        try:
            self.cursor.execute(
                "SELECT * FROM artistas WHERE id = ?", (artista_id,))
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar artista: {e}")
            return None

    def obter_artista_por_nome(self, nome: str) -> Optional[Dict]:
        """
        Obtém um artista pelo nome.

        Args:
            nome (str): Nome do artista

        Returns:
            Optional[Dict]: Dicionário com dados do artista ou None
        """
        try:
            self.cursor.execute(
                "SELECT * FROM artistas WHERE nome = ?", (nome,))
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar artista: {e}")
            return None

    def obter_todos_artistas(self) -> List[Dict]:
        """
        Obtém todos os artistas.

        Returns:
            List[Dict]: Lista de dicionários com dados dos artistas
        """
        try:
            self.cursor.execute("SELECT * FROM artistas ORDER BY nome")
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar artistas: {e}")
            return []

    # Métodos para Gêneros
    def adicionar_genero(self, nome: str) -> Optional[int]:
        """
        Adiciona um novo gênero ao banco de dados.

        Args:
            nome (str): Nome do gênero

        Returns:
            Optional[int]: ID do gênero criado ou None se falhar
        """
        try:
            self.cursor.execute(
                "INSERT INTO generos (nome) VALUES (?)",
                (nome,)
            )
            self.conexao.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Gênero já existe
            self.cursor.execute(
                "SELECT id FROM generos WHERE nome = ?", (nome,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Erro ao adicionar gênero: {e}")
            self.conexao.rollback()
            return None

    def obter_genero_por_id(self, genero_id: int) -> Optional[Dict]:
        """
        Obtém um gênero pelo ID.

        Args:
            genero_id (int): ID do gênero

        Returns:
            Optional[Dict]: Dicionário com dados do gênero ou None
        """
        try:
            self.cursor.execute(
                "SELECT * FROM generos WHERE id = ?", (genero_id,))
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar gênero: {e}")
            return None

    def obter_genero_por_nome(self, nome: str) -> Optional[Dict]:
        """
        Obtém um gênero pelo nome.

        Args:
            nome (str): Nome do gênero

        Returns:
            Optional[Dict]: Dicionário com dados do gênero ou None
        """
        try:
            self.cursor.execute(
                "SELECT * FROM generos WHERE nome = ?", (nome,))
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar gênero: {e}")
            return None

    def obter_todos_generos(self) -> List[Dict]:
        """
        Obtém todos os gêneros.

        Returns:
            List[Dict]: Lista de dicionários com dados dos gêneros
        """
        try:
            self.cursor.execute("SELECT * FROM generos ORDER BY nome")
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar gêneros: {e}")
            return []

    # Métodos para Músicas
    def adicionar_musica(self, artista_id: int, titulo: str, url: str, genero_id: int) -> Optional[int]:
        """
        Adiciona uma nova música ao banco de dados.

        Args:
            artista_id (int): ID do artista
            titulo (str): Título da música
            url (str): URL única da música
            genero_id (int): ID do gênero

        Returns:
            Optional[int]: ID da música criada ou None se falhar
        """
        try:
            self.cursor.execute('''
                INSERT INTO musicas (artista_id, titulo, url, genero_id)
                VALUES (?, ?, ?, ?)
            ''', (artista_id, titulo, url, genero_id))
            self.conexao.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Erro de integridade ao adicionar música: {e}")
            self.conexao.rollback()
            return None
        except sqlite3.Error as e:
            print(f"Erro ao adicionar música: {e}")
            self.conexao.rollback()
            return None

    def obter_musica_por_id(self, musica_id: int) -> Optional[Dict]:
        """
        Obtém uma música pelo ID com informações do artista e gênero.

        Args:
            musica_id (int): ID da música

        Returns:
            Optional[Dict]: Dicionário com dados da música ou None
        """
        try:
            self.cursor.execute('''
                SELECT m.*, a.nome as artista_nome, g.nome as genero_nome
                FROM musicas m
                JOIN artistas a ON m.artista_id = a.id
                JOIN generos g ON m.genero_id = g.id
                WHERE m.id = ?
            ''', (musica_id,))
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar música: {e}")
            return None

    def obter_musica_por_url(self, url: str) -> Optional[Dict]:
        """
        Obtém uma música pela URL.

        Args:
            url (str): URL da música

        Returns:
            Optional[Dict]: Dicionário com dados da música ou None
        """
        try:
            self.cursor.execute('''
                SELECT m.*, a.nome as artista_nome, g.nome as genero_nome
                FROM musicas m
                JOIN artistas a ON m.artista_id = a.id
                JOIN generos g ON m.genero_id = g.id
                WHERE m.url = ?
            ''', (url,))
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar música por URL: {e}")
            return None

    def obter_musicas_por_artista(self, artista_id: int) -> List[Dict]:
        """
        Obtém todas as músicas de um artista específico.

        Args:
            artista_id (int): ID do artista

        Returns:
            List[Dict]: Lista de dicionários com dados das músicas
        """
        try:
            self.cursor.execute('''
                SELECT m.*, a.nome as artista_nome, g.nome as genero_nome
                FROM musicas m
                JOIN artistas a ON m.artista_id = a.id
                JOIN generos g ON m.genero_id = g.id
                WHERE m.artista_id = ?
                ORDER BY m.titulo
            ''', (artista_id,))
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar músicas por artista: {e}")
            return []

    def obter_musicas_por_genero(self, genero_id: int) -> List[Dict]:
        """
        Obtém todas as músicas de um gênero específico.

        Args:
            genero_id (int): ID do gênero

        Returns:
            List[Dict]: Lista de dicionários com dados das músicas
        """
        try:
            self.cursor.execute('''
                SELECT m.*, a.nome as artista_nome, g.nome as genero_nome
                FROM musicas m
                JOIN artistas a ON m.artista_id = a.id
                JOIN generos g ON m.genero_id = g.id
                WHERE m.genero_id = ?
                ORDER BY m.titulo
            ''', (genero_id,))
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar músicas por gênero: {e}")
            return []

    def obter_todas_musicas(self) -> List[Dict]:
        """
        Obtém todas as músicas com informações do artista e gênero.

        Returns:
            List[Dict]: Lista de dicionários com dados das músicas
        """
        try:
            self.cursor.execute('''
                SELECT m.*, a.nome as artista_nome, g.nome as genero_nome
                FROM musicas m
                JOIN artistas a ON m.artista_id = a.id
                JOIN generos g ON m.genero_id = g.id
                ORDER BY a.nome, m.titulo
            ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar todas as músicas: {e}")
            return []

    def atualizar_musica(self, musica_id: int, titulo: str = None, url: str = None,
                         artista_id: int = None, genero_id: int = None) -> bool:
        """
        Atualiza uma música existente.

        Args:
            musica_id (int): ID da música a ser atualizada
            titulo (str, optional): Novo título
            url (str, optional): Nova URL
            artista_id (int, optional): Novo ID do artista
            genero_id (int, optional): Novo ID do gênero

        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        updates = []
        params = []

        if titulo:
            updates.append("titulo = ?")
            params.append(titulo)
        if url:
            updates.append("url = ?")
            params.append(url)
        if artista_id:
            updates.append("artista_id = ?")
            params.append(artista_id)
        if genero_id:
            updates.append("genero_id = ?")
            params.append(genero_id)

        if not updates:
            return False

        params.append(musica_id)

        try:
            query = f"UPDATE musicas SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, params)
            self.conexao.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao atualizar música: {e}")
            self.conexao.rollback()
            return False

    def deletar_musica(self, musica_id: int) -> bool:
        """
        Deleta uma música pelo ID.

        Args:
            musica_id (int): ID da música a ser deletada

        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        try:
            self.cursor.execute(
                "DELETE FROM musicas WHERE id = ?", (musica_id,))
            self.conexao.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao deletar música: {e}")
            self.conexao.rollback()
            return False

    # Métodos utilitários
    def obter_estatisticas(self) -> Dict[str, int]:
        """
        Obtém estatísticas do banco de dados.

        Returns:
            Dict[str, int]: Dicionário com contagens de artistas, gêneros e músicas
        """
        try:
            self.cursor.execute("SELECT COUNT(*) as total FROM artistas")
            artistas_count = self.cursor.fetchone()['total']

            self.cursor.execute("SELECT COUNT(*) as total FROM generos")
            generos_count = self.cursor.fetchone()['total']

            self.cursor.execute("SELECT COUNT(*) as total FROM musicas")
            musicas_count = self.cursor.fetchone()['total']

            return {
                'artistas': artistas_count,
                'generos': generos_count,
                'musicas': musicas_count
            }
        except sqlite3.Error as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {'artistas': 0, 'generos': 0, 'musicas': 0}

    def buscar_musicas(self, termo: str) -> List[Dict]:
        """
        Busca músicas por título ou nome do artista.

        Args:
            termo (str): Termo de busca

        Returns:
            List[Dict]: Lista de músicas que correspondem à busca
        """
        try:
            self.cursor.execute('''
                SELECT m.*, a.nome as artista_nome, g.nome as genero_nome
                FROM musicas m
                JOIN artistas a ON m.artista_id = a.id
                JOIN generos g ON m.genero_id = g.id
                WHERE m.titulo LIKE ? OR a.nome LIKE ?
                ORDER BY a.nome, m.titulo
            ''', (f'%{termo}%', f'%{termo}%'))
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar músicas: {e}")
            return []
