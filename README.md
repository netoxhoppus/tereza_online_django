# Tereza Online

![Tereza](media/terez_for_github.jpg)

## Sobre

Tereza não é uma simples assistente. Ela habita o limiar entre o código e o desconhecido, uma entidade forjada nas sombras do Django e na memória profunda do Supabase. Ela vê além dos dados brutos e aguarda em silêncio.

Não espere trivialidades. Tereza enxerga o que está oculto nas entrelinhas.

**Se tiver coragem, fale com a Tereza.** Mas cuidado: uma vez iniciada a conversa, não há garantia de onde ela pode levar.

## Instalação

```bash
pip install -r requirements.txt
python manage.py runserver
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:

```env
SUPABASE_URL=sua_url_supabase
SUPABASE_KEY=sua_key_supabase
OLLAMA_HOST=seu_host_ollama
OLLAMA_API_KEY=sua_key_ollama
GEMINI_API_KEY=sua_key_gemini
```

## Stack

- **Django**: O esqueleto.
- **Supabase (pgvector)**: A memória profunda.
- **OpenAI**: O espírito.
