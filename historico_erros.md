# Histórico de Erros - Projeto Automação de Email (GWS)

Este arquivo documenta os principais erros mapeados ao longo do desenvolvimento e operação da rotina matinal. Ele serve como base de conhecimento para facilitar consultas e depurações futuras, tanto por você quanto pelo agente de desenvolvimento.

---

## 1. UnicodeEncodeError: 'charmap' codec can't encode character (Falha no Windows)
**Status:** [A Ser Corrigido]
**Sintomas:** Ao rodar `gmail_triage.py` localmente no Windows, o script falha abruptamente e lança a exceção:
`UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f5a4' in position 32: character maps to <undefined>`
**Causa Raiz:** O terminal padrão do Windows utiliza a codificação `CP1252` (Windows-1252), que não suporta caracteres Unicode complexos (como emojis, ex: 🖤). Quando o script tenta imprimir o assunto de um e-mail que contém um emoji, o Python tenta converter o caractere para `CP1252` e trava.
**Solução:** Adicionar a instrução `sys.stdout.reconfigure(encoding='utf-8')` no início dos scripts Python executores para forçar a saída padrão a usar UTF-8, independentemente do sistema operacional.

---

## 2. Silenciamento de Erros e Falsos Positivos no GitHub Actions (Swallowed Exceptions)
**Status:** [A Ser Corrigido]
**Sintomas:** O workflow `Rotina Matinal do Gmail` roda no GitHub Actions, finaliza com um check verde de sucesso, porém os e-mails não são organizados, as tarefas não são extraídas e os eventos do calendário não aparecem. O relatório final fica vazio (com a mensagem "Não houve e-mails de rotina...").
**Causa Raiz:** Nos executores (ex: `gmail_triage.py`), o comando `subprocess.run` do GWS CLI é capturado por um bloco `try/except`. Caso o CLI falhe (seja por rate limit, versão incompatível ou queda da API), o bloco `except` apenas imprime a mensagem de erro no log e retorna um objeto vazio (`return result_obj.to_dict()`). O arquivo `run_routine.py` entende que os dados vazios são válidos e encerra com código `0`, fazendo o GitHub Actions relatar sucesso (círculo verde), mascarando o erro real.
**Solução:**
* Propagar o erro `subprocess.CalledProcessError` ao invés de suprimi-lo no bloco `except`, ou
* Adicionar verificações em `run_routine.py` e forçar uma saída com `sys.exit(1)` caso qualquer processo essencial do GWS falhe.

---

## 3. Falha de Autenticação em Ambiente Headless (GitHub Actions)
**Status:** [Corrigido no commit `c940c99` e `a3ed919`]
**Sintomas:** O comando GWS falhava no GitHub Actions com erro de `invalid_client` ou não conseguia acessar os tokens corretos.
**Causa Raiz:** Antigamente, utilizavam-se múltiplas variáveis de ambiente para `CLIENT_ID` e `SECRET` acopladas com tokens passados via `echo`, o que introduzia quebras de linha ou espaços indesejados nas chaves. Além disso, no Ubuntu o chaveiro (keyring) do sistema não está disponível em um ambiente sem interface gráfica.
**Solução (Como foi corrigido):**
* Foi configurado o payload monolítico gravando o Secret via bloco `cat << 'EOF' > credenciais_gws.json` para manter a formatação intacta.
* Passou-se a usar a variável de ambiente `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE="credenciais_gws.json"`.
* A variável `GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND="file"` foi forçada no workflow para que o CLI não tente usar o chaveiro gráfico do sistema.

---

## 4. Quebra por Atualização Inesperada do CLI (Regressão de Versão)
**Status:** [A Ser Corrigido]
**Sintomas:** O sistema funciona perfeitamente por um tempo e, de um dia para o outro, começa a falhar silenciosamente no GitHub Actions sem nenhuma alteração no código fonte.
**Causa Raiz:** O GitHub Actions roda o comando `npm install -g @googleworkspace/cli`, o que força a instalação da última versão disponível (`@latest`). Em caso de atualizações no pacote que quebrem compatibilidade ou introduzam bugs com o keyring backend em ambientes headless (como nas transições para as versões 0.22.4 e 0.22.5), a rotina quebra repentinamente.
**Solução:** Alterar o arquivo `.github/workflows/rotina_matinal.yml` para congelar (pin) a versão exata do pacote do GWS que é sabidamente estável localmente (por exemplo: `@googleworkspace/cli@0.22.3`).

---

## 5. ModuleNotFoundError (Módulos não encontrados no GitHub Actions)
**Status:** [Corrigido no commit `3e1013d`]
**Sintomas:** Ao rodar `run_routine.py` no GitHub Actions, o script não conseguia encontrar arquivos dentro dos diretórios dos agentes (`agents/...`), retornando `ModuleNotFoundError`.
**Causa Raiz:** O caminho de busca do Python (`sys.path`) não compreendia a árvore de diretórios do ambiente de container Ubuntu de forma automática como no desenvolvimento local. E caminhos hardcoded para o diretório Windows falhavam no Linux.
**Solução (Como foi corrigido):**
* A variável de ambiente `PYTHONPATH` foi declarada no GitHub Actions apontando os caminhos relativos: `.:agents/morning-email-triage/execution:agents/daily-standup-generator/execution`.
* O código do `run_routine.py` foi ajustado para usar `os.path.dirname(os.path.abspath(__file__))` para montar as rotas dos arquivos de forma dinâmica.

---
*Este histórico deve ser mantido atualizado a cada novo problema mapeado e resolvido.*
