# Catálogo Musical

Um sistema completo para gerenciar, organizar e reproduzir músicas com interface de linha de comando (CLI) e banco de dados SQLite.

## Funcionalidades

### Gerenciamento de Catálogo
- **Cadastro de músicas** com título, URL, artista e gênero
- **Artistas e gêneros** com cadastro automático e reutilização
- **Busca inteligente** por músicas, artistas e gêneros
- **Estatísticas completas** do acervo musical

### Sistema de Reprodução
- **Reprodução automática** via mpv
- **Controle de volume** (0-100%)
- **Modo vídeo/áudio** configurável
- **Playlists dinâmicas** por artista, gênero ou todas as músicas

### Banco de Dados
- **SQLite** com três tabelas relacionadas
- **Artistas** com nomes únicos
- **Gêneros musicais** organizados
- **Músicas** com links únicos e referências

## Tecnologias Utilizadas

- **Python 3.8+**
- **SQLite3** - Banco de dados embutido
- **mpv** - Player de mídia externo
- **Dataclasses** - Para estruturas de dados
- **Type Hints** - Tipagem estática opcional

## Estrutura do Projeto

```
catalogo-musical/
├── Banco_Dados.py     # Gerenciador do banco de dados
├── main.py           # Sistema principal e interfaces
├── tocador.py        # Integração com mpv
└── musicas.db        # Banco de dados (gerado automaticamente)
```

## Instalação e Configuração

### 1. Pré-requisitos
```bash
# Instalar mpv (Linux/macOS)
sudo apt-get install mpv  # Debian/Ubuntu
brew install mpv          # macOS

# Windows: Baixar do site oficial https://mpv.io/
```

### 2. Clonar/Configurar
```bash
# Criar ambiente virtual (opcional)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependências (apenas Python padrão necessário)
# Nenhuma instalação adicional é necessária além do mpv
```

## Como Usar

### Executar o Sistema
```bash
python main.py
```

### Menu Principal
```
🎵  CATÁLOGO MUSICAL  🎵
[1] Adicionar Música
[2] Listar Todas as Músicas
[3] Tocar Todas as Músicas
[4] Tocar por Gênero
[5] Tocar por Artista
[6] Estatísticas
[7] Sair
```

### Exemplo de Uso

1. **Adicionar uma música:**
   - Título: "Bohemian Rhapsody"
   - URL: https://www.youtube.com/watch?v=fJ9rUzIMcZQ
   - Artista: "Queen" (sugere existentes ou novo)
   - Gênero: "Rock" (sugere existentes ou novo)

2. **Reproduzir por gênero:**
   - Seleciona "Rock" na lista
   - Todas as músicas de rock são reproduzidas automaticamente

3. **Ver estatísticas:**
   ```
   📊 ESTATÍSTICAS
   🎵 Músicas: 42
   🎤 Artistas: 15
   🎭 Gêneros: 8
   ```

## Classes Principais

### `BancoDeDadosMusica`
Gerencia todas as operações do banco de dados:
- CRUD completo para músicas, artistas e gêneros
- Consultas otimizadas com JOINs
- Tratamento de erros e rollback automático

### `CatalogoMusical`
Camada de abstração sobre o banco:
- Converte dados brutos em objetos Python
- Gerencia cache local de dados
- Fornece interface amigável para operações

### `Player`
Controle de reprodução:
- Gerenciamento de playlists
- Configuração de volume e modo vídeo
- Interface unificada para o tocador

### `InterfaceUsuario`
CLI interativa:
- Menus intuitivos com validação
- Seleção por números
- Confirmações e resumos

## Recursos Avançados

### Sugestões Inteligentes
- Ao adicionar música, sugere artistas e gêneros existentes
- Evita duplicações automaticamente
- Permite rápido cadastro de novos itens

### Busca Flexível
```python
# No código, é possível buscar por:
- Todas as músicas
- Músicas por artista
- Músicas por gênero
- Música específica por URL
```

### Performance
- Conexão persistente com banco de dados
- Cache de objetos em memória
- Operações assíncronas de reprodução

## Solução de Problemas

### "Comando mpv não encontrado"
```bash
# Verificar instalação
mpv --version

# Linux: instalar via gerenciador de pacotes
sudo apt update && sudo apt install mpv

# Windows: adicionar ao PATH
# 1. Baixar mpv do site oficial
# 2. Extrair para C:\mpv
# 3. Adicionar C:\mpv ao PATH do sistema
```

### "Erro de banco de dados"
- Verifique permissões de escrita na pasta
- O arquivo `musicas.db` é criado automaticamente
- Em caso de corrupção, delete o arquivo para recriar

### "URL não reproduzindo"
- Teste a URL manualmente no mpv
- Verifique conexão com internet
- Alguns serviços podem requerer cookies/autenticação

## Migração de Dados

### Exportar dados:
```python
# No código, adicione:
import json
dados = db.obter_todas_musicas()
with open('backup.json', 'w') as f:
    json.dump(dados, f, indent=2)
```

### Importar de outros sistemas:
- Estrutura simples (artista, título, URL, gênero)
- Suporte a CSV via adaptador personalizado

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## Créditos

Desenvolvido para amantes de música que preferem controle total sobre seu acervo musical.

**Dica:** Para URLs do YouTube, use links de vídeos ou playlists. O mpv suporta a maioria dos formatos online!

---
**Aproveite sua música do seu jeito!**
