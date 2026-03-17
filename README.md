# 🌅 Morning Routine Automation

Sistema inteligente para automação de rotina matinal, integrando triagem de e-mails via Gmail API e organização de compromissos via Google Calendar API.

## 🚀 Funcionalidades

- **Triagem Inteligente de E-mails:**
  - Categorização automática (Importante, Promoção, Newsletter, Outros).
  - Identificação de boletos e assuntos críticos.
  - E-mails importantes são mantidos como não lidos na Inbox para sua atenção.
  - Outros e-mails são etiquetados e arquivados automaticamente.
- **Standup de Calendário:**
  - Consolidação de compromissos de múltiplos calendários (Principal, Equipe, etc.).
- **Briefing Premium Minimalism:**
  - Geração de um relatório HTML elegante e minimalista.
  - Conteúdo motivacional diário.
  - Envio automático do briefing para o seu e-mail.

## 🛠️ Pré-requisitos

1. **GWS CLI:** Certifique-se de ter o [Google Workspace CLI](https://github.com/googleworkspace/cli) instalado e configurado.
2. **Python 3.10+:** O projeto utiliza scripts Python para orquestração.
3. **Dependências:**
   ```bash
   pip install python-dotenv
   ```

## ⚙️ Configuração

1. Clone o repositório.
2. Crie um arquivo `.env` na raiz do projeto com suas credenciais do GWS CLI:
   ```env
   GOOGLE_WORKSPACE_CLI_CLIENT_ID=seu_client_id
   GOOGLE_WORKSPACE_CLI_CLIENT_SECRET=seu_client_secret
   ```
3. Configure os IDs dos calendários no arquivo `agents/daily-standup-generator/execution/calendar_standup.py`.

## 📖 Como Usar

Para executar a rotina completa:

```bash
python run_routine.py
```

O sistema irá processar os e-mails, buscar a agenda de hoje, gerar o briefing e enviá-lo para o e-mail configurado.

## 🎨 Design

O layout segue o padrão **Premium Minimalism v2**, focado em legibilidade e estética profissional. Um modelo de exemplo pode ser visualizado em `morning_briefing_v2_preview.html`.

---
*Desenvolvido com Antigravity.*
