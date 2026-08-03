BACKUP PROJETO - Dashboard de Controle de Atividades de Veiculos
Atualizado: 2026-08-03
Caminho: C:\Dashboard_Frota_Dev

OBJETIVO
Aplicacao desktop para cadastro de veiculos, registro de atividades (quantidade),
dashboard com KPIs e graficos, historico filtravel com paginacao, geracao de relatorio
PDF e envio por e-mail (inclui agendamento semanal as segundas 08:00).

EMPRESA
MADEMAXI - Materiais de Construcao e Ferragem
Logo: app/assets/logo_mademaxi.png (vermelho #E53935 + preto #1a1a1a)

STACK TECNICA
Python 3.14.6, PySide6 >= 6.10.1, SQLite + SQLAlchemy >= 2.0.40, PyQtGraph >= 0.14.0,
ReportLab >= 4.3.1, smtplib, APScheduler >= 3.11.0, PyInstaller, Inno Setup 7.

ESTRUTURA DE PASTAS
Dashboard_Frota_Dev/
  run.py
  requirements.txt
  README.md
  backup_projeto.md
  build_installer.py
  Dashboard_Frotas.iss
  credits.txt
  data/app.db (SQLite - NAO INCLUIR NO INSTALADOR)
  data/config.json (NAO INCLUIR NO INSTALADOR)
  data/logs/app.log (NAO INCLUIR NO INSTALADOR)
  app/main.py
  app/assets/logo_mademaxi.png
  app/core/config_store.py (criptografia simples de senha SMTP)
  app/core/database.py (SQLAlchemy engine + session_scope)
  app/core/logging_config.py
  app/core/paths.py
  app/core/utils.py (validacao de placa, datas)
  app/models/base.py (DeclarativeBase)
  app/models/vehicle.py (placa, modelo, marca, ano, categoria, status, observacoes)
  app/models/activity.py (veiculo_id FK, data_hora, quantidade, observacoes)
  app/models/setting.py (chave/valor generico)
  app/services/vehicle_service.py (CRUD, retorna dicts, valida placa)
  app/services/activity_service.py (CRUD, filtros, paginacao, KPIs, retorna dicts)
  app/services/report_service.py (PDF profissional MADEMAXI com logo, cards, zebra)
  app/services/email_service.py (SMTP TLS/SSL, suporte a HTML alternativo)
  app/services/scheduler_service.py (APScheduler, envio semanal HTML profissional)
  app/ui/theme.py (dark/light palette + stylesheet global)
  app/ui/icons.py (qtawesome mapping)
  app/ui/main_window.py (sidebar com logo MADEMAXI + stack + signals)
  app/ui/dialogs/vehicle_dialog.py (formulario placa/modelo/categoria/obs)
  app/ui/dialogs/activity_dialog.py (formulario veiculo/data/quantidade/obs)
  app/ui/models/vehicle_table_model.py
  app/ui/models/activity_table_model.py
  app/ui/pages/dashboard_page.py (KPIs + graficos, filtro veiculo somente leitura)
  app/ui/pages/vehicles_page.py (tabela + CRUD, emite Signal vehicle_changed)
  app/ui/pages/activity_register_page.py (registro direto SEM confirmacao)
  app/ui/pages/history_page.py (tabela paginada, filtros, PDF, e-mail HTML)
  app/ui/pages/settings_page.py (SMTP, tema, empresa, logo, agendamento)

REGRAS CRITICAS DE IMPLEMENTACAO
1. NUNCA retornar objetos ORM fora de session_scope. Sempre converter para dict.
2. VehicleService e ActivityService ja retornam dicts em todos os metodos publicos.
3. PySide6 usa Signal (nao pyqtSignal).
4. VehicleDialog recebe dict (nao objeto ORM).
5. Todos os services usam session_scope contextmanager.
6. Tema dark padrao. Tema light com fundo cinza claro (#f3f4f6) e texto escuro (#111827).
7. Highlight da sidebar: azul (#3b82f6 dark, #2563eb light).
8. Sinais de sincronizacao: vehicle_changed e activity_changed.

SCHEMA DO BANCO
Tabela veiculos: id PK, placa VARCHAR(10) UNIQUE, modelo VARCHAR(80), marca VARCHAR(80),
ano INTEGER, categoria VARCHAR(20) CHECK('Carga Pesada','Carga Leve','Outros'),
status VARCHAR(20) CHECK('Ativo','Inativo','Em Manutencao'), observacoes TEXT, created_at DATETIME.
Tabela atividades: id PK, veiculo_id INTEGER FK, data_hora DATETIME, quantidade INTEGER,
observacoes TEXT, created_at DATETIME.
Index: ix_atividades_veiculo_data (veiculo_id, data_hora).

MUDANCAS REALIZADAS (2026-08-03)
1. SINCRONIZACAO AUTOMATICA
   - activity_register_page.py: adicionado Signal activity_changed
   - main_window.py: conecta activity_changed a history_page.refresh e dashboard_page.refresh
   - Ao registrar uma atividade, Historico e Dashboard atualizam automaticamente

2. REGISTRO DIRETO SEM CONFIRMACAO
   - activity_register_page.py: removido QMessageBox.question de confirmacao
   - Removido QMessageBox.information de sucesso (sem som, sem janela extra)
   - Salva direto ao clicar "Salvar", mantendo apenas validacao de veiculo

3. DASHBOARD REFORMULADO
   - dashboard_page.py: filtros reorganizados em grid 2x4 ergonômico
   - Veiculo ocupa 3x mais espaco (columnStretch 3 vs 1 dos outros)
   - Dropdown de veiculo: setEditable(False) - somente selecao, sem digitacao
   - Removido QCompleter e setInsertPolicy (desnecessarios sem edicao)

4. PDF PROFISSIONAL MADEMAXI
   - report_service.py: layout completo reformulado
   - Cabecalho centralizado com logo (2.8cm) + nome da empresa
   - Linha decorativa vermelha #E53935 abaixo do cabecalho
   - Cards de metricas com 4 colunas: Atividades, Quantidade, Veiculos, Media
   - Tabela detalhada com cabecalho preto #1a1a1a e linha vermelha
   - Zebra striping (branco / #f9fafb)
   - Rodape com numero de pagina + "MADEMAXI - Todos os direitos reservados"
   - Fallback de logo: app/assets/logo_mademaxi.png se config.logo_path nao existir
   - Funcao _get_logo_path() para resolucao de caminho do logo

5. E-MAIL HTML PROFISSIONAL
   - email_service.py: suporte a html_body (multipart alternative)
   - scheduler_service.py: template HTML com tabelas (compativel Gmail/Outlook)
   - history_page.py: mesmo template HTML para envio manual
   - Layout: header preto + borda vermelha, cards em tabela 4 colunas, detalhes em tabela
   - Cores: #1a1a1a (texto), #E53935 (destaque), #f3f4f6 (fundo), #fafafa (cards)
   - Nome da empresa: "MADEMAXI - Materiais de Construcao e Ferragem"

6. LOGO MADEMAXI NO SOFTWARE
   - main_window.py: logo exibido no topo da sidebar (180px largura)
   - Nome "MADEMAXI" em vermelho #E53935 + subtitulo abaixo
   - Logo tambem usado como icone do aplicativo

7. BUILD E INSTALADOR
   - build_installer.py: script Python que automatiza todo o processo
   - Etapa 1: limpeza de dados sensiveis (app.db, logs, __pycache__, *.pyc)
   - Etapa 2: PyInstaller --onefile --windowed com icon do logo
   - Etapa 3: geracao de credits.txt e Dashboard_Frotas.iss
   - Etapa 4: compilacao com Inno Setup
   - Instalador detecta versao anterior e pergunta se remove antes
   - Créditos na tela final com dados do desenvolvedor
   - Tamanho do instalador: ~76 MB

HISTORICO DE PROBLEMAS E SOLUCOES
- Problema: pyqtSignal nao existe no PySide6. Solucao: usar Signal.
- Problema: DetachedInstanceError ao acessar objetos ORM fora da sessao.
  Solucao: converter para dicts dentro do session_scope em todos os services.
- Problema: history_page quebrava ao acessar v.id em dict.
  Solucao: usar v["id"].
- Problema: vehicle_dialog esperava objeto ORM.
  Solucao: adaptar para receber dict.
- Problema: report_service referenciava campos inexistentes.
  Solucao: adaptar ao schema simplificado.
- Problema: scheduler_service buscava kpis["km_total"] inexistente.
  Solucao: usar kpis["quantidade_total"].
- Problema: tema light ilegivel.
  Solucao: stylesheet global com cores de contraste adequadas.
- Problema: highlight verde na sidebar.
  Solucao: mudar para azul (#3b82f6 dark, #2563eb light).
- Problema: grafico de top veiculos mostrava placa.
  Solucao: agrupar por modelo no KPI.
- Problema: Historico nao atualizava ao registrar atividade.
  Solucao: adicionar Signal activity_changed e conectar em main_window.
- Problema: Registro exigia 2 confirmacoes.
  Solucao: remover QMessageBox.question e QMessageBox.information do save().
- Problema: Dropdown de veiculo no Dashboard permitia digitacao.
  Solucao: setEditable(False).
- Problema: Layout do Dashboard amontoado.
  Solucao: reorganizar em QGridLayout com columnStretch proporcional.
- Problema: PDF sem identidade visual.
  Solucao: criar layout profissional com cores MADEMAXI, logo, cards, zebra.
- Problema: E-mail com CSS flexbox quebrava no Gmail mobile.
  Solucao: reescrever com tabelas HTML puras (compatibilidade universal).
- Problema: E-mail mostrava "Loja de Materiais de Construcao".
  Solucao: atualizar config.json company_name e fallback nos services.
- Problema: config.json corrompido com BOM pelo PowerShell.
  Solucao: usar [System.IO.File]::WriteAllBytes para salvar sem BOM.
- Problema: Instalador compilava em 1 segundo (sem PyInstaller).
  Solucao: criar build_installer.py com etapa PyInstaller antes do Inno Setup.

O QUE JA FUNCIONA
- Cadastro completo de veiculos (CRUD)
- Registro de atividades vinculadas a veiculo (salva direto, sem confirmacao)
- Sincronizacao automatica de dropdowns via Signal vehicle_changed
- Sincronizacao automatica Historico/Dashboard via Signal activity_changed
- Dashboard com KPIs e graficos de barra/linha
- Dropdown de veiculo no Dashboard somente leitura
- Historico paginado com filtros e ordenacao
- Geracao de PDF profissional com identidade MADEMAXI
- Envio de e-mail SMTP com corpo HTML profissional
- Agendamento semanal automatico com catch-up e e-mail HTML
- Tema dark e light com stylesheet global
- Criptografia simples de senha SMTP
- Logo MADEMAXI no software e nos relatorios
- Build automatizado PyInstaller + Inno Setup

O QUE AINDA FALTA / IDEIAS FUTURAS
- Exportar CSV do historico
- Filtros avancados no historico
- Notificacoes visuais no dashboard
- Backup automatico do banco de dados
- Multi-usuario com perfis

AMBIENTE DE DESENVOLVIMENTO
cd C:\Dashboard_Frota_Dev
.venv\Scripts\Activate.ps1
python run.py

BUILD DO INSTALADOR
C:\Dashboard_Frota_Dev\.venv\Scripts\python.exe C:\Dashboard_Frota_Dev\build_installer.py
Saida: C:\Dashboard_Frota_Dev\dist_installer\Dashboard_Frotas_MADEMAXI_Setup_v1.0.0.exe

DESENVOLVEDOR
Maicon do Amarilho Silveira
GitHub: https://github.com/MaiconDAS

CONTEXTO DO USUARIO
- Brasil, valores em BRL
- Prefere comandos PowerShell unicos e automatizados
- Recebe arquivos completos (nunca snippets)
- Prioriza eficiencia de memoria
- Backup usado como contexto para IA em novas conversas
- Projeto movido de C:\Users\amari\Desktop\Dashboard para C:\Dashboard_Frota_Dev
