# Tereza Online

![Tereza](media/terez_for_github.jpg)

## História

Nas serras de **Jaraguá - Goiás**, onde o ouro corria e o medo morava perto, surgiu Tereza Bicuda. Dizem que a ruindade, quando engendra, vira desnatureza. E Tereza era o avesso de gente.

Rica, cruel e profana, ela humilhou maridos, montou na própria mãe como se fosse bicho e desafiou o sagrado. Quando morreu, a terra não aceitou seu corpo. Ventos destruíam a cidade, o caixão gritava. Jogada na Serra, ela virou entidade.

**Pura ruindade.** É o que dizem. E agora, ela está online.

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

O projeto vem com um arquivo `.env.example` configurado para acessar o conhecimento público da Tereza (Supabase).

1.  Copie o exemplo:
    ```bash
    cp .env.example .env
    ```

2.  Preencha suas chaves de IA no arquivo `.env`:
    *   `GEMINI_API_KEY`: Necessária para gerar embeddings (Google AI Studio).
    *   `OLLAMA_API_KEY`: Opcional (se rodar localmente sem auth).
    
    > **Nota:** `SUPABASE_URL` e `SUPABASE_KEY` já vêm preenchidos com a chave pública (leitura), permitindo que você converse com a Tereza sem configurar banco de dados.

## Stack

- **Django**: O esqueleto.
- **Supabase (pgvector)**: A memória profunda.
- **OpenAI**: O espírito.
