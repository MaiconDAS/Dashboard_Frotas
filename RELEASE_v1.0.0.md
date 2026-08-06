# Release v1.0.0 - Dashboard de Controle de Atividades de Veiculos

## MADEMAXI - Materiais de Construcao e Ferragem

---

## Sobre

Aplicacao desktop completa para cadastro de veiculos, registro de atividades com quantidade, dashboard com KPIs e graficos interativos, historico filtravel com paginacao, geracao de relatorios PDF profissionais e envio por e-mail (incluindo agendamento semanal automatico).

---

## Funcionalidades

- **Cadastro de Veiculos**: CRUD completo com validacao de placa, categorias (Carga Pesada, Carga Leve, Outros) e status (Ativo, Inativo, Em Manutencao)
- **Registro de Atividades**: Registro direto e instantaneo, sem confirmacoes desnecessarias, vinculado ao veiculo com data/hora e quantidade
- **Dashboard com KPIs**: Cards de metricas + graficos de barra e linha, filtros ergonomicos com dropdown somente leitura
- **Historico Paginado**: Tabela com filtros avancados, ordenacao, exportacao para PDF e envio de e-mail HTML
- **Relatorios PDF Profissionais**: Layout MADEMAXI com logo, cards de metricas, tabela detalhada com zebra striping e rodape
- **E-mail HTML Profissional**: Template compativel com Gmail/Outlook, com identidade visual da empresa
- **Agendamento Automatico**: Envio semanal de relatorio por e-mail toda segunda-feira as 08:00 via APScheduler
- **Temas Dark/Light**: Interface moderna com paleta escura padrao e modo claro com alto contraste
- **Criptografia de Senha**: Senha SMTP armazenada com criptografia simples
- **Build Automatizado**: Script unico que gera o instalador .exe via PyInstaller + Inno Setup

---

## Stack Tecnica

| Tecnologia | Versao |
|------------|--------|
| Python | 3.14.6 |
| PySide6 | >= 6.10.1 |
| SQLite + SQLAlchemy | >= 2.0.40 |
| PyQtGraph | >= 0.14.0 |
| ReportLab | >= 4.3.1 |
| APScheduler | >= 3.11.0 |
| PyInstaller + Inno Setup | 7 |

---

## Instalacao

1. Baixe o arquivo `Dashboard_Frotas_MADEMAXI_Setup_v1.0.0.exe` nos Assets abaixo
2. Execute o instalador (detecta versao anterior e pergunta se deseja remover)
3. O atalho sera criado automaticamente no Menu Iniciar e Area de Trabalho
4. Pronto para usar

> O banco de dados SQLite (`data/app.db`) e arquivos de configuracao (`data/config.json`) sao criados automaticamente na primeira execucao e nao sao incluidos no instalador.

---

## Estrutura do Projeto

```
Dashboard_Frota_Dev/
├── run.py                          # Entry point
├── requirements.txt
├── README.md
├── build_installer.py              # Script de build completo
├── Dashboard_Frotas.iss            # Script Inno Setup
├── data/
│   ├── app.db                      # Banco SQLite (runtime)
│   ├── config.json                 # Configuracoes (runtime)
│   └── logs/app.log                # Logs (runtime)
├── app/
│   ├── main.py
│   ├── assets/logo_mademaxi.png
│   ├── core/                       # Config, DB, logging, paths, utils
│   ├── models/                     # Veiculos, Atividades, Settings
│   ├── services/                   # CRUD, relatorios, e-mail, agendador
│   └── ui/                         # Temas, paginas, dialogos, models
└── dist_installer/
    └── Dashboard_Frotas_MADEMAXI_Setup_v1.0.0.exe
```

---

## Regras de Implementacao Aplicadas

- Nenhum objeto ORM sai do `session_scope` — tudo convertido para dict
- Signal do PySide6 (nao pyqtSignal)
- Dialogos recebem dict, nao objetos ORM
- Sincronizacao automatica via `vehicle_changed` e `activity_changed`
- Tema dark padrao, light com fundo #f3f4f6 e texto #111827
- Highlight da sidebar em azul (#3b82f6 / #2563eb)

---

## Problemas Resolvidos nesta Versao

| Problema | Solucao |
|----------|---------|
| pyqtSignal inexistente no PySide6 | Migracao para Signal |
| DetachedInstanceError em objetos ORM | Conversao para dict dentro do session_scope |
| history_page quebrava com .id em dict | Uso de ["id"] |
| vehicle_dialog esperava objeto ORM | Adaptado para receber dict |
| scheduler_service buscava km_total inexistente | Corrigido para quantidade_total |
| Tema light ilegivel | Stylesheet global com contraste adequado |
| Dropdown de veiculo permitia digitacao | setEditable(False) |
| Layout do Dashboard amontoado | Reorganizado em QGridLayout proporcional |
| PDF sem identidade visual | Layout profissional com cores MADEMAXI |
| E-mail com CSS flexbox quebrava no Gmail | Reescrito com tabelas HTML puras |
| config.json corrompido com BOM | Salvamento via [System.IO.File]::WriteAllBytes |
| Instalador compilava sem PyInstaller | Script build_installer.py com etapa completa |

---

## Roadmap Futuro

- [ ] Exportar CSV do historico
- [ ] Filtros avancados no historico
- [ ] Notificacoes visuais no dashboard
- [ ] Backup automatico do banco de dados
- [ ] Multi-usuario com perfis

---

## Desenvolvedor

**Maicon do Amarilho Silveira**
GitHub: https://github.com/MaiconDAS

---

## Licenca

Todos os direitos reservados — MADEMAXI - Materiais de Construcao e Ferragem

---

*Release gerado em 03 de agosto de 2026.*
