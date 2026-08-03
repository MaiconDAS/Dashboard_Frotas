# README - Dashboard Frota
# Arquivo de contexto para continuidade do projeto em novas conversas com IA
# Atualizado: 2026-08-02
# Caminho do projeto: C:\Users\amari\Desktop\Dashboard

# ============================================================
# 1. VISAO GERAL
# ============================================================
Dashboard Frota e um aplicativo desktop Windows para controle de atividades de veiculos.
Funcionalidades: cadastro de veiculos (placa, modelo, categoria), registro de atividades
(veiculo, data, quantidade, observacoes), dashboard com KPIs e graficos, historico
filtravel com paginacao, geracao de relatorio PDF, envio de e-mail SMTP e agendamento
semanal automatico (segunda-feira 08:00).

# ============================================================
# 2. STACK TECNICA EXATA
# ============================================================
Python 3.14.6
PySide6 >= 6.10.1 (GUI, Signal em vez de pyqtSignal)
SQLite + SQLAlchemy >= 2.0.40 (ORM, session_scope contextmanager)
PyQtGraph >= 0.14.0 (graficos de barra e linha no dashboard)
ReportLab >= 4.3.1 (geracao de PDF)
smtplib (envio de e-mail)
APScheduler >= 3.11.0 (agendamento semanal)
PyInstaller 6.21.0 (build do executavel)
Inno Setup 7 (instalador .exe)
qtawesome (icones FontAwesome, fallback para QIcon vazio se nao instalado)
cryptography (ofuscacao de senha SMTP via Fernet ou XOR fallback)

# ============================================================
# 3. ESTRUTURA DE PASTAS E ARQUIVOS
# ============================================================
Dashboard/
  run.py                          # Entry point
  requirements.txt                # Dependencias pip
  backup_projeto.md               # Backup de contexto
  README.md                       # Este arquivo
  DashboardFrota.spec             # Spec PyInstaller (onedir, inclui app/)
  installer.iss                   # Script Inno Setup 7
  build_installer.ps1             # Script PowerShell de build automatizado
  LICENSE.txt                     # Licenca comercial Maicon do Amarilho Silveira
  logo.ico                        # Icone do app (256,128,64,48,32,16px)
  logo.bmp                        # Imagem wizard Inno Setup (164x314)
  logo_small.bmp                  # Imagem pequena wizard Inno Setup (55x55)
  logo.png / logo.svg             # Fontes do icone
  data/
    app.db                        # Banco SQLite (nao versionar, criado automaticamente)
    config.json                   # Configuracoes do usuario (tema, SMTP, empresa)
    logs/
      app.log                     # Logs da aplicacao
  app/
    main.py                       # Inicializacao: init_db, services, QApplication, MainWindow
    __init__.py
    core/
      config_store.py             # AppConfig dataclass + criptografia simples de senha SMTP
      database.py                 # engine SQLite, SessionLocal, session_scope, init_db
      logging_config.py           # RotatingFileHandler + console, formato padrao
      paths.py                    # get_data_dir(), get_db_path(), get_config_path(), get_logs_dir()
      utils.py                    # normalize_plate(), is_valid_plate(), clamp_int(), start/end_of_day(), previous_week_monday_to_sunday()
      __init__.py
    models/
      base.py                     # DeclarativeBase
      vehicle.py                  # Vehicle: id, placa, modelo, marca, ano, categoria, status, observacoes, created_at
      activity.py                 # Activity: id, veiculo_id FK, data_hora, quantidade, observacoes, created_at
      setting.py                  # Setting: id, chave, valor
      __init__.py
    services/
      vehicle_service.py          # CRUD, retorna dicts, valida placa (ABC-1234 ou ABC1D23)
      activity_service.py         # CRUD, filtros, paginacao, KPIs, retorna dicts
      report_service.py           # Gera PDF com ReportLab, recebe List[Tuple[dict, dict]]
      email_service.py            # SMTP TLS/SSL, test_connection, send_report com anexo PDF
      scheduler_service.py        # APScheduler BackgroundScheduler, job semanal, startup_catch_up
      __init__.py
    ui/
      theme.py                    # make_palette() dark/light + apply_theme(app, theme) com stylesheet global
      icons.py                    # icon(name) via qtawesome, fallback QIcon()
      main_window.py              # QMainWindow com sidebar QListWidget + QStackedWidget, conecta sinais
      __init__.py
      dialogs/
        vehicle_dialog.py         # Recebe dict (nao ORM), formulario placa/modelo/categoria/obs
        activity_dialog.py        # Recebe vehicles list[dict] + activity dict opcional
        __init__.py
      models/
        vehicle_table_model.py    # QAbstractTableModel, recebe list[dict]
        activity_table_model.py   # QAbstractTableModel, recebe List[Tuple[dict, dict]]
        __init__.py
      pages/
        dashboard_page.py         # KPIs + graficos PyQtGraph, filtro veiculo/data/categoria, on_vehicles_changed()
        vehicles_page.py          # Tabela + CRUD, emite Signal vehicle_changed ao add/edit/delete
        activity_register_page.py # Formulario rapido de registro de atividade
        history_page.py           # Tabela paginada, filtros, PDF, e-mail, editar/excluir atividade
        settings_page.py          # SMTP, tema, empresa, logo, agendamento semanal
        __init__.py

# ============================================================
# 4. SCHEMA DO BANCO (SQLite)
# ============================================================
Tabela veiculos:
  id INTEGER PRIMARY KEY AUTOINCREMENT
  placa VARCHAR(10) UNIQUE NOT NULL
  modelo VARCHAR(80) NOT NULL
  marca VARCHAR(80)
  ano INTEGER
  categoria VARCHAR(20) NOT NULL DEFAULT 'Outros' CHECK ('Carga Pesada','Carga Leve','Outros')
  status VARCHAR(20) NOT NULL DEFAULT 'Ativo' CHECK ('Ativo','Inativo','Em Manutencao')
  observacoes TEXT
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  Index: ix_veiculos_categoria_status (categoria, status)

Tabela atividades:
  id INTEGER PRIMARY KEY AUTOINCREMENT
  veiculo_id INTEGER NOT NULL REFERENCES veiculos(id)
  data_hora DATETIME NOT NULL
  quantidade INTEGER NOT NULL DEFAULT 1
  observacoes TEXT
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  Index: ix_atividades_veiculo_data (veiculo_id, data_hora)

Tabela configuracoes:
  id INTEGER PRIMARY KEY AUTOINCREMENT
  chave VARCHAR(80) UNIQUE NOT NULL
  valor TEXT

# ============================================================
# 5. REGRAS CRITICAS DE IMPLEMENTACAO (NAO QUEBRAR)
# ============================================================
REGRA 1: NUNCA retornar objetos ORM fora de session_scope. Sempre converter para dict
         dentro do contexto do with session_scope() as s. Todos os metodos publicos dos
         services (VehicleService, ActivityService) retornam dicts ou listas de dicts.
         Isso evita DetachedInstanceError quando a UI acessa atributos fora da sessao.

REGRA 2: PySide6 usa Signal (nao pyqtSignal). Exemplo: from PySide6.QtCore import Signal.
         pyqtSignal e do PyQt5 e causa ImportError no PySide6.

REGRA 3: VehicleDialog recebe dict (parametro vehicle: dict | None), NAO objeto ORM.
         Acesso via vehicle.get("placa"), vehicle.get("modelo"), etc.

REGRA 4: ActivityTableModel recebe List[Tuple[dict, dict]] e NAO converte ORM.
         O service ja converte antes de retornar.

REGRA 5: Todos os services usam session_scope contextmanager de app.core.database.
         Nunca criar Session manualmente fora do contextmanager.

REGRA 6: Tema dark e o padrao. Tema light usa fundo #f3f4f6, texto #111827, highlight #2563eb.
         O apply_theme() aplica tanto QPalette quanto stylesheet global para todos os widgets.
         O stylesheet e ESSENCIAL para legibilidade no light (inputs, tabelas, botoes).

REGRA 7: Sinais de atualizacao: VehiclesPage emite vehicle_changed Signal. MainWindow conecta
         esse sinal em ActivityRegisterPage.refresh_vehicles(), DashboardPage.on_vehicles_changed()
         e HistoryPage.refresh_vehicles(). Isso garante sincronizacao automatica dos dropdowns.

REGRA 8: O report_service.py recebe List[Tuple[dict, dict]] e acessa via .get() em dicts.
         Nunca acessar atributos ORM (a.data_hora, v.placa) no report.

REGRA 9: O scheduler_service busca kpis["quantidade_total"] (NAO "km_total"). O campo
         km_total no ReportSummary e apenas um nome legacy, mas o valor vem de quantidade_total.

REGRA 10: O build do PyInstaller usa onedir (COLLECT), NAO onefile. O executavel final
          fica em dist/DashboardFrota/DashboardFrota.exe. O instalador empacota a pasta inteira.
          Hiddenimports obrigatorios: sqlalchemy, apscheduler, reportlab, pyqtgraph, cryptography, pydoc.
          NAO excluir pydoc dos excludes (causa erro no pyqtgraph).

# ============================================================
# 6. HISTORICO COMPLETO DE PROBLEMAS E SOLUCOES
# ============================================================
Problema: pyqtSignal nao existe no PySide6
  Solucao: trocar para Signal em todos os arquivos

Problema: DetachedInstanceError ao acessar objetos ORM fora da sessao
  Solucao: converter para dicts dentro do session_scope em VehicleService e ActivityService

Problema: history_page quebrava ao acessar v.id em objeto ORM
  Solucao: usar v["id"] (dict) em _report_payload()

Problema: vehicle_dialog esperava objeto ORM (vehicle.placa)
  Solucao: adaptar VehicleDialog para receber dict (vehicle.get("placa"))

Problema: report_service referenciava campos inexistentes (km_inicial, tipo, motorista, destino, descricao)
  Solucao: adaptar ao schema simplificado: Data/Hora, Placa, Modelo, Categoria, Quantidade, Observacoes

Problema: scheduler_service buscava kpis["km_total"] inexistente
  Solucao: usar kpis["quantidade_total"]

Problema: tema light ilegivel (fundo branco puro, texto escuro sem contraste)
  Solucao: stylesheet global com fundo #f3f4f6, inputs #ffffff, texto #111827, bordas #d1d5db

Problema: highlight verde na sidebar (#22c55e) feio
  Solucao: mudar para azul (#3b82f6 dark, #2563eb light) no QPalette e stylesheet

Problema: grafico de top veiculos mostrava placa no eixo X
  Solucao: agrupar por Vehicle.modelo em vez de Vehicle.placa no KPI

Problema: sidebar com spacing 2 fazia highlight sobrepor abas adjacentes
  Solucao: aumentar setSpacing(8) no QListWidget da sidebar

Problema: editar atividade no historico dava NameError: QDialog not defined
  Solucao: adicionar QDialog nos imports de history_page.py

Problema: build PyInstaller falhava com No module named 'pydoc'
  Solucao: remover 'pydoc' dos excludes do spec e adicionar aos hiddenimports

Problema: build_installer.ps1 nao encontrava pyinstaller (nao estava no PATH)
  Solucao: detectar caminho automatico em pythoncore-3.14-64\Scripts\pyinstaller.exe

Problema: build_installer.ps1 nao encontrava Inno Setup 7
  Solucao: adicionar C:\Program Files\Inno Setup 7\ISCC.exe nos candidatos de busca

# ============================================================
# 7. O QUE FUNCIONA (ESTADO ATUAL)
# ============================================================
- Cadastro completo de veiculos (CRUD) com validacao de placa
- Registro de atividades vinculadas a veiculo
- Sincronizacao automatica de dropdowns via Signal vehicle_changed
- Dashboard com KPIs e graficos de barra/linha (por nome do veiculo)
- Historico paginado com filtros, ordenacao, edicao e exclusao
- Geracao de PDF com ReportLab
- Envio de e-mail SMTP com TLS/SSL
- Agendamento semanal automatico com catch-up na inicializacao
- Tema dark e light com stylesheet global
- Criptografia simples de senha SMTP (Fernet ou XOR fallback)
- Build PyInstaller funcionando (onedir)
- Instalador Inno Setup 7 com deteccao de versao anterior
- Logo colorido no estilo referencia (caminhao, van, carro + grafico)

# ============================================================
# 8. O QUE AINDA FALTA / IDEIAS FUTURAS
# ============================================================
- Exportar CSV do historico
- Filtros avancados no historico (por quantidade minima/maxima)
- Notificacoes visuais na UI (toast)
- Backup automatico do banco SQLite
- Multi-usuario com autenticacao
- Relatorio mensal além do semanal

# ============================================================
# 9. AMBIENTE DE DESENVOLVIMENTO
# ============================================================
# Novo PC - preparar ambiente:
cd C:\Projetos\Dashboard
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py

# Build executavel + instalador:
.\build_installer.ps1
# Requisitos: PyInstaller instalado, Inno Setup 7 instalado
# Output: dist_installer\DashboardFrota_Setup_v1.0.0.exe

# ============================================================
# 10. PADROES DE CODIGO
# ============================================================
- Services: metodos publicos retornam dicts, usam session_scope
- UI Pages: recebem services via constructor injection
- Dialogs: recebem dicts, retornam dicts via .values()
- TableModels: QAbstractTableModel, set_items()/set_rows() com beginResetModel/endResetModel
- Sinais: emitidos em operacoes que alteram dados (vehicle_changed)
- Temas: apply_theme(app, theme) aplica palette + stylesheet global
- Paths: sempre usar app.core.paths para data/config/logs (funciona em dev e frozen)

# ============================================================
# 11. CONTEXTO DO USUARIO
# ============================================================
- Nome: Maicon do Amarilho Silveira
- Pais: Brasil (valores em BRL quando aplicavel)
- E-mail: maiconamarilho@gmail.com
- Licenca comercial pertence exclusivamente a Maicon do Amarilho Silveira
- Prefere comandos PowerShell para automatizacao
- Recebe arquivos COMPLETOS (nunca snippets ou trechos parciais)
- Prioriza eficiencia de memoria (generators, lazy evaluation, dicts em vez de objetos ORM)
- Backup usado como contexto para IA em novas conversas
- Projeto local em C:\Users\amari\Desktop\Dashboard (PC atual)
- Repositorio remoto: https://github.com/MaiconDAS/NarratoAI (sincronizar a cada alteracao)
