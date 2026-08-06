BACKUP PROJETO - Dashboard de Controle de Atividades de Veiculos
Atualizado: 2026-08-05
Caminho: C:\Dashboard_Frota_Dev

================================================================================
CHANGELOG v2.0.0 - REVAMP VISUAL + LOGIN ADMINISTRATIVO + CATEGORIAS CUSTOMIZAVEIS
================================================================================

[LOGIN ADMINISTRATIVO]
- Tela de login (LoginDialog) exibida ao abrir o software
- Logo MADEMAXI reposicionado com scaled(220, 170, KeepAspectRatio)
- Texto "MADEMAXI" removido do login (ja presente no logo)
- Subtitulo "Dashboard de Controle de Frotas" movido para abaixo do logo
- Autenticacao via AdminService.authenticate() com PBKDF2
- Atalho F1 abre cadastro de administrador via QShortcut (ApplicationShortcut)
- Possui uma senha mestre para acesso ao cadastro de admins (nao divulgada)
- AdminRegisterDialog: cadastro com nome_completo, username, senha (min 6 chars), checkbox is_master
- AdminEditDialog: edicao completa (nome, username, nova senha, checkbox is_master, botao excluir)
- AdminManagementPage: tabela de admins com botao "Alterar Cadastro"
- Soft delete: is_active=False ao excluir (nao remove do banco)
- MainWindow recebe admin_data e exibe aba "Gestao" apenas se is_master=True
- Titulo da janela: "Dashboard Frotas — MADEMAXI | Logado: {nome_completo}"

[REVAMP VISUAL]
- Padrao de espacamento aprovado:
  * Margins: 40, 28, 40, 28 (dialogs) / 20, 16, 20, 16 (pages)
  * Entre label e input: colado (sem addSpacing)
  * Entre campos (input -> proxima label): 16px
  * Entre ultimo campo e botoes: 28px
  * Botoes: height 44, padding 0 28px
  * Titulo + linha vermelha + 24px antes do primeiro campo
- LoginDialog: logo em container com FixedHeight(200), sem hint de cadastro
- VehicleDialog: removidos Modelo, Marca, Ano. Somente Placa, Categoria, Status, Observacoes
- VehicleDialog: botoes reposicionados abaixo do campo observacoes
- ActivityRegisterPage: layout vertical espacoso, labels acima dos inputs
- HistoryPage: filtros em QGridLayout com colunas proporcionais, datas nao cortadas
- AdminRegisterDialog: espacamento generoso (520x580), campos nao amontoados
- AdminEditDialog: espacamento generoso (540x620), botao Excluir vermelho
- Theme.py: QDateEdit min-width 140px, drop-down visivel com subcontrol-position
- Theme.py: QComboBox::drop-down e QDateEdit::drop-down com down-arrow CSS
- Sidebar: highlight #E53935, hover #1f1f1f, itens com border-radius 8px

[CATEGORIAS CUSTOMIZAVEIS]
- CategoryService: persistencia via tabela Setting (chave="vehicle_categories")
- CategoryService.list(): retorna lista de categorias do banco (JSON)
- CategoryService.add/update/delete: CRUD completo de categorias
- AdminManagementPage: secao "Categorias de Veiculos" com QListWidget
- Botoes: Adicionar, Editar, Excluir para gerenciar categorias
- VehicleDialog: categorias carregadas dinamicamente via CategoryService.list()
- DashboardPage: filtro de categoria carrega dinamicamente
- HistoryPage: filtro de categoria carrega dinamicamente
- Fallback: se CategoryService falhar, usa ["Carga Pesada", "Carga Leve", "Outros"]
- Migration: removido CHECK constraint ck_veiculos_categoria do SQLite
- Vehicle model: categoria sem CHECK constraint (VARCHAR(20) livre)

================================================================================

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
  migrate_categories.py (migration: remove CHECK constraint categoria)
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
  app/models/admin.py (login administrativo, is_master, is_active)
  app/models/base.py (DeclarativeBase)
  app/models/vehicle.py (placa, modelo, marca, ano, categoria, status, observacoes, activities relationship)
  app/models/activity.py (veiculo_id FK, data_hora, quantidade, observacoes, vehicle relationship)
  app/models/setting.py (chave/valor generico - usado para categorias)
  app/services/admin_service.py (CRUD admin, auth PBKDF2, senha mestra oculta, is_master, update_admin, delete_admin)
  app/services/vehicle_service.py (CRUD, retorna dicts, valida placa, aceita status)
  app/services/activity_service.py (CRUD, filtros, paginacao, KPIs, retorna dicts)
  app/services/category_service.py (CRUD categorias via Setting, JSON persistencia)
  app/services/report_service.py (PDF profissional MADEMAXI com logo, cards, zebra, generated_by)
  app/services/email_service.py (SMTP TLS/SSL, HTML alternativo, generated_by)
  app/services/scheduler_service.py (APScheduler, envio semanal HTML profissional)
  app/ui/theme.py (dark/light palette + stylesheet global, QDateEdit/QComboBox drop-down visivel)
  app/ui/icons.py (qtawesome mapping)
  app/ui/main_window.py (sidebar com logo MADEMAXI + stack + signals, admin_conditional, nav_order fixo)
  app/ui/dialogs/login_dialog.py (tela login, logo MADEMAXI, F1 -> senha mestra, QInputDialog)
  app/ui/dialogs/admin_register_dialog.py (cadastro admin, checkbox is_master, spacing padrao)
  app/ui/dialogs/admin_edit_dialog.py (edicao completa + checkbox is_master + botao excluir, spacing padrao)
  app/ui/dialogs/vehicle_dialog.py (placa, categoria dinamica, status, observacoes, spacing padrao)
  app/ui/dialogs/activity_dialog.py (formulario veiculo/data/quantidade/obs)
  app/ui/models/vehicle_table_model.py
  app/ui/models/activity_table_model.py
  app/ui/models/admin_table_model.py
  app/ui/pages/dashboard_page.py (KPIs + graficos, filtro categoria dinamica)
  app/ui/pages/vehicles_page.py (tabela + CRUD, emite Signal vehicle_changed)
  app/ui/pages/activity_register_page.py (registro direto, layout espacoso vertical)
  app/ui/pages/history_page.py (tabela paginada, filtros, categoria dinamica, PDF, e-mail HTML)
  app/ui/pages/admin_management_page.py (gestao de logins + categorias, tabela admins, spacing padrao)
  app/ui/pages/settings_page.py (SMTP, tema, empresa, logo, agendamento)

REGRAS CRITICAS DE IMPLEMENTACAO
1. NUNCA retornar objetos ORM fora de session_scope. Sempre converter para dict.
2. VehicleService e ActivityService ja retornam dicts em todos os metodos publicos.
3. PySide6 usa Signal (nao pyqtSignal).
4. VehicleDialog recebe dict (nao objeto ORM).
5. Todos os services usam session_scope contextmanager.
6. Tema dark padrao. Tema light com fundo cinza claro (#f3f4f6) e texto escuro (#111827).
7. Highlight da sidebar: vermelho MADEMAXI (#E53935).
8. Sinais de sincronizacao: vehicle_changed e activity_changed.
9. Relatorios PDF e e-mail devem constar "Gerado por: {username}" no rodape/corpo.
10. Categorias de veiculos sao customizaveis via CategoryService (persistido em Setting).
11. Aba "Gestao" (ex-"Gestao de Logins") so aparece para is_master=True.

SCHEMA DO BANCO
Tabela veiculos: id PK, placa VARCHAR(10) UNIQUE, modelo VARCHAR(80), marca VARCHAR(80),
ano INTEGER, categoria VARCHAR(20), status VARCHAR(20), observacoes TEXT, created_at DATETIME.
Tabela atividades: id PK, veiculo_id INTEGER FK, data_hora DATETIME, quantidade INTEGER,
observacoes TEXT, created_at DATETIME.
Tabela admins: id PK, username VARCHAR(50) UNIQUE, password_hash VARCHAR(128),
nome_completo VARCHAR(100), is_master INTEGER DEFAULT 0, is_active INTEGER DEFAULT 1,
created_at DATETIME.
Tabela configuracoes: id PK, chave VARCHAR(50) UNIQUE, valor TEXT.
Index: ix_atividades_veiculo_data (veiculo_id, data_hora).

LOGIN E AUTENTICACAO
- Ao abrir o software, aparece tela de login (LoginDialog) com logo MADEMAXI.
- Usuario e senha validados via AdminService.authenticate() (PBKDF2).
- Atalho F1 na tela de login abre prompt de senha mestra.
- Senha mestra correta abre AdminRegisterDialog para cadastro de administradores.
- Checkbox "Administrador" (is_master) no cadastro: conta master pode gerenciar usuarios e categorias.
- run.py: QApplication criado ANTES do LoginDialog. Se login aceito, abre MainWindow.
- MainWindow recebe admin_data, mostra aba "Gestao" apenas se is_master=True.
- AdminManagementPage: tabela com todos os admins + secao de categorias customizaveis.
- AdminEditDialog: edita nome_completo, username, nova senha, checkbox is_master, excluir cadastro.
- NUNCA exibe senha antiga. Somente permite definir nova senha.
- Botao "Excluir Cadastro" vermelho com confirmacao. Soft delete (is_active=False).
- Somente administrador pode acessar Gestao.

CATEGORIAS CUSTOMIZAVEIS
- CategoryService persiste categorias na tabela Setting (chave="vehicle_categories", valor=JSON).
- Padrao inicial: ["Carga Pesada", "Carga Leve", "Outros"].
- Admin pode adicionar, editar ou excluir categorias na pagina Gestao.
- VehicleDialog, DashboardPage e HistoryPage carregam categorias dinamicamente.
- Migration remove CHECK constraint ck_veiculos_categoria para permitir qualquer categoria.

MUDANCAS REALIZADAS (2026-08-05)
1. LOGIN ADMINISTRATIVO
   - admin.py: modelo Admin com username, password_hash, nome_completo, is_master, is_active
   - admin_service.py: CRUD, autenticacao PBKDF2, senha mestra oculta, is_master, update_admin, delete_admin
   - login_dialog.py: tela de login com logo MADEMAXI, F1 -> senha mestra, QInputDialog
   - admin_register_dialog.py: cadastro com checkbox is_master, spacing padrao
   - admin_edit_dialog.py: edicao completa + checkbox is_master + botao excluir, spacing padrao
   - admin_management_page.py: tabela admins + secao categorias, botao "Alterar Cadastro"
   - admin_table_model.py: modelo de tabela para lista de admins
   - database.py: importa app.models.admin no init_db()
   - main_window.py: nav_order fixo, aba admin condicional, titulo com nome logado
   - run.py: QApplication primeiro, depois LoginDialog, depois MainWindow com admin_data

2. REVAMP VISUAL
   - theme.py: QDateEdit min-width 140px, drop-down visivel, QComboBox arrow CSS
   - login_dialog.py: logo scaled(220,170), sem texto MADEMAXI duplicado, sem hint de cadastro
   - vehicle_dialog.py: removidos Modelo/Marca/Ano, somente Placa/Categoria/Status/Obs
   - vehicle_dialog.py: botoes abaixo de observacoes, spacing padrao
   - activity_register_page.py: layout vertical espacoso, labels acima dos inputs
   - history_page.py: filtros em QGridLayout, datas nao cortadas, botoes visiveis
   - admin_register_dialog.py: 520x580, spacing 16 entre campos
   - admin_edit_dialog.py: 540x620, spacing 16 entre campos
   - login_dialog.py: 420x520, logo container FixedHeight(200)

3. CATEGORIAS CUSTOMIZAVEIS
   - category_service.py: CRUD categorias via tabela Setting (JSON)
   - admin_management_page.py: QListWidget + botoes Adicionar/Editar/Excluir
   - vehicle_dialog.py: categorias dinamicas via CategoryService.list()
   - dashboard_page.py: filtro categoria dinamico
   - history_page.py: filtro categoria dinamico
   - migrate_categories.py: remove CHECK constraint ck_veiculos_categoria
   - vehicle.py: categoria sem CHECK constraint

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
  Solucao: mudar para vermelho MADEMAXI (#E53935).
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
- Problema: README.md corrompido no copy-paste do chat.
  Solucao: gerar arquivo no servidor via ipython, baixar pronto e colar na pasta.
- Problema: login nao funcionava (admin_data nao acessivel).
  Solucao: guardar _admin_data no LoginDialog e acessar em run.py.
- Problema: QWidget nao importado no login_dialog.py.
  Solucao: adicionar QWidget aos imports.
- Problema: coluna is_master nao existia no banco antigo.
  Solucao: script migrate_admin.py executa ALTER TABLE ADD COLUMN.
- Problema: QApplication criado depois do LoginDialog.
  Solucao: inverter ordem em run.py: QApplication primeiro, LoginDialog depois.
- Problema: abas trocadas na sidebar (Gestao de Logins mostrava Configuracoes).
  Solucao: nav_order fixo, adicionar widgets ao stack na mesma ordem da sidebar.
- Problema: tabela de admins com linhas amontoadas.
  Solucao: setMinimumSectionSize(52), padding nas celulas, gridline-color visivel.
- Problema: botao "Alterar Cadastro" ilegivel na tabela.
  Solucao: aumentar padding para 10px 20px, fonte 13px, bold.
- Problema: dialog de edicao com campos amontoados e ilegiveis.
  Solucao: spacing padrao (16px entre campos, 28px antes de botoes).
- Problema: dialog de edicao sem opcao de excluir.
  Solucao: adicionar botao "Excluir Cadastro" vermelho com QMessageBox de confirmacao.
- Problema: Ctrl+Alt+C nao funcionava com foco em QLineEdit.
  Solucao: trocar para F1 com QShortcut(ApplicationShortcut).
- Problema: QMessageBox.getText nao existe no PySide6.
  Solucao: usar QInputDialog.getText.
- Problema: botao de calendario invisivel no QDateEdit.
  Solucao: theme.py com QDateEdit::drop-down visivel e min-width 140px.
- Problema: vehicle_dialog enviava marca/ano inesperados para VehicleService.create().
  Solucao: remover marca e ano do dict values().
- Problema: VehicleService.create() nao aceitava status.
  Solucao: adicionar parametro status ao metodo create.
- Problema: Qt nao importado em activity_register_page.py.
  Solucao: adicionar Qt ao import de PySide6.QtCore.
- Problema: login_dialog com texto "MADEMAXI" sobreposto ao logo.
  Solucao: remover label "MADEMAXI", manter apenas logo + subtitulo.
- Problema: hint de cadastro visivel na tela de login.
  Solucao: remover QLabel com dica de atalho.
- Problema: campo de data cortado horizontalmente no history_page.
  Solucao: QGridLayout com colunas proporcionais, QDateEdit min-width 140px no theme.
- Problema: combo de veiculo ocupava tela inteira no history_page.
  Solucao: columnStretch(0,1) columnStretch(1,2) no grid de filtros.
- Problema: Setting model usa chave/valor (portugues), nao key/value.
  Solucao: CategoryService usar chave= e valor= ao filtrar/criar Setting.
- Problema: QInputDialog nao importado em admin_management_page.py.
  Solucao: adicionar QInputDialog aos imports.
- Problema: CHECK constraint ck_veiculos_categoria bloqueava categorias customizadas.
  Solucao: migration migrate_categories.py remove constraint, vehicle.py sem CHECK.

O QUE JA FUNCIONA
- Cadastro completo de veiculos (CRUD) com categorias customizaveis
- Registro de atividades vinculadas a veiculo (salva direto, sem confirmacao)
- Sincronizacao automatica de dropdowns via Signal vehicle_changed
- Sincronizacao automatica Historico/Dashboard via Signal activity_changed
- Dashboard com KPIs e graficos de barra/linha
- Dropdown de veiculo no Dashboard somente leitura
- Historico paginado com filtros e ordenacao
- Geracao de PDF profissional com identidade MADEMAXI e "Gerado por: {username}"
- Envio de e-mail SMTP com corpo HTML profissional e "Gerado por: {username}"
- Agendamento semanal automatico com catch-up e e-mail HTML
- Tema dark e light com stylesheet global
- Criptografia simples de senha SMTP
- Logo MADEMAXI no software e nos relatorios
- Build automatizado PyInstaller + Inno Setup
- Login administrativo com tela de login
- Cadastro de admin via F1 + senha mestra oculta
- Contas administradoras (is_master) com permissao de gestao de logins e categorias
- Edicao completa de cadastro admin (nome, username, senha, is_master)
- Exclusao de cadastro admin com confirmacao (soft delete)
- Botao "Alterar Cadastro" grande e legivel na tabela
- Categorias de veiculos customizaveis (add/edit/delete) na pagina Gestao
- Filtros de categoria dinamicos no Dashboard e Historico

O QUE AINDA FALTA / IDEIAS FUTURAS
- Botao de logout na sidebar (fixo embaixo, proximo ao rodape)
- Exportar CSV do historico
- Filtros avancados no historico
- Notificacoes visuais no dashboard
- Backup automatico do banco de dados
- Log de auditoria de acoes

AMBIENTE DE DESENVOLVIMENTO
cd C:\Dashboard_Frota_Dev
.venv\Scripts\Activate.ps1
python run.py

BUILD DO INSTALADOR
C:\Dashboard_Frota_Dev\.venv\Scripts\python.exe C:\Dashboard_Frota_Dev\build_installer.py
Saida: C:\Dashboard_Frota_Dev\dist_installer\Dashboard_Frotas_MADEMAXI_Setup_v1.0.0.exe

MIGRACAO BANCO (categorias customizaveis)
C:\Dashboard_Frota_Dev\.venv\Scripts\python.exe C:\Dashboard_Frota_Dev\migrate_categories.py

DESENVOLVEDOR
Maicon do Amarilho Silveira
GitHub: https://github.com/MaiconDAS

CONTEXTO DO USUARIO
- Brasil, valores em BRL
- Prefere comandos PowerShell unicos e automatizados
- Recebe arquivos completos (nunca snippets)
- Prioriza eficiencia de memoria
- Backup usado como contexto para IA em novas conversas
- Projeto em C:\Dashboard_Frota_Dev
- README gerado via ipython no servidor (nao via PowerShell)



================================================================================
CHANGELOG v2.1.0 - SISTEMA DE AUDITORIA DE ATIVIDADES
================================================================================

[NOVO] Sistema de Auditoria
- Modelo AuditLog (app/models/audit_log.py): tabela auditoria com id, usuario, acao, entidade, entidade_id, descricao, data_hora, data_retroativa
- AuditService (app/services/audit_service.py): metodos log() e list_all() para registrar e consultar auditoria
- AuditDialog (app/ui/dialogs/audit_dialog.py): tabela QTableWidget exibindo registros de auditoria ordenados do mais recente
- Botao Auditoria adicionado na AdminManagementPage (aba Gestao), visivel apenas para is_master=True
- ActivityService.create/update/delete agora aceitam parametro opcional username e registram log de auditoria automaticamente
- ActivityRegisterPage recebe admin_data e passa username ao criar atividade
- HistoryPage passa username ao editar e excluir atividades
- MainWindow passa admin_data para ActivityRegisterPage e HistoryPage
- database.py: importa app.models.audit_log no init_db() para criacao da tabela
- Correcao database is locked: chamadas AuditService.log() movidas para FORA dos blocos with session_scope em ActivityService, garantindo que o commit da transacao principal ocorra antes de abrir nova sessao para o log

================================================================================
ARQUIVOS DE CONTEXTO DESTE CHAT - MODELS
================================================================================

--- FILE: app/models/base.py ---
from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

--- FILE: app/models/activity.py ---
from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
if TYPE_CHECKING:
    from app.models.vehicle import Vehicle
class Activity(Base):
    __tablename__ = "atividades"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    veiculo_id: Mapped[int] = mapped_column(ForeignKey("veiculos.id"), nullable=False)
    data_hora: Mapped[datetime] = mapped_column(nullable=False)
    quantidade: Mapped[int] = mapped_column(default=1)
    observacoes: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    vehicle: Mapped["Vehicle"] = relationship("Vehicle", back_populates="activities")

--- FILE: app/models/admin.py ---
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.models.base import Base
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    nome_completo = Column(String(100), nullable=False)
    is_master = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

--- FILE: app/models/audit_log.py (NOVO) ---
from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
class AuditLog(Base):
    __tablename__ = "auditoria"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    acao: Mapped[str] = mapped_column(String(20), nullable=False)
    entidade: Mapped[str] = mapped_column(String(50), nullable=False)
    entidade_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    data_hora: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    data_retroativa: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


================================================================================
ARQUIVOS DE CONTEXTO DESTE CHAT - DATABASE E SERVICES
================================================================================

--- FILE: app/core/database.py ---
[NOTA: contem imports de models com noqa F401. Ver arquivo fonte para pragma WAL completo.]
from __future__ import annotations
import logging
from contextlib import contextmanager
from typing import Iterator
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.paths import get_db_path
from app.models.base import Base
logger = logging.getLogger(__name__)
def _sqlite_engine() -> Engine:
    db_path = get_db_path()
    url = f"sqlite+pysqlite:///{db_path.as_posix()}"
    engine = create_engine(url, future=True, echo=False, connect_args={"check_same_thread": False})
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.close()
    return engine
engine = _sqlite_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
def init_db() -> None:
    from app.models.activity import Activity
    from app.models.admin import Admin
    from app.models.audit_log import AuditLog
    from app.models.setting import Setting
    from app.models.vehicle import Vehicle
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    logger.info("Banco inicializado em %s", db_path)
@contextmanager
def session_scope() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

--- FILE: app/services/vehicle_service.py ---
from __future__ import annotations
import logging
import re
from typing import List
from app.core.database import session_scope
from app.models.vehicle import Vehicle
logger = logging.getLogger(__name__)
_PLACA_MERCOSUL = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")
_PLACA_ANTIGA = re.compile(r"^[A-Z]{3}-?[0-9]{4}$")
def validar_placa(placa: str) -> bool:
    p = placa.strip().upper().replace("-", "")
    return bool(_PLACA_MERCOSUL.match(p) or _PLACA_ANTIGA.match(p))
def normalize_plate(placa: str) -> str:
    p = placa.strip().upper().replace("-", "")
    if _PLACA_ANTIGA.match(p) and len(p) == 7:
        return f"{p[:3]}-{p[3:]}"
    return p
class VehicleService:
    @staticmethod
    def create(*, placa: str, modelo: str | None = None, marca: str | None = None, ano: int | None = None, categoria: str = "Outros", status: str = "Ativo", observacoes: str | None = None) -> dict:
        placa = normalize_plate(placa)
        if not validar_placa(placa):
            raise ValueError("Placa invalida.")
        with session_scope() as session:
            existing = session.query(Vehicle).filter_by(placa=placa).first()
            if existing:
                raise ValueError(f"Placa '{placa}' ja cadastrada.")
            v = Vehicle(placa=placa, modelo=modelo or placa, marca=marca, ano=ano, categoria=categoria, status=status, observacoes=observacoes)
            session.add(v)
            session.flush()
            session.refresh(v)
            return _to_dict(v)
    @staticmethod
    def update(vehicle_id: int, **kwargs) -> dict:
        with session_scope() as session:
            v = session.get(Vehicle, vehicle_id)
            if not v:
                raise ValueError("Veiculo nao encontrado.")
            if "placa" in kwargs:
                kwargs["placa"] = normalize_plate(kwargs["placa"])
                if not validar_placa(kwargs["placa"]):
                    raise ValueError("Placa invalida.")
            for key, value in kwargs.items():
                if hasattr(v, key):
                    setattr(v, key, value)
            session.flush()
            session.refresh(v)
            return _to_dict(v)
    @staticmethod
    def delete(vehicle_id: int) -> None:
        with session_scope() as session:
            v = session.get(Vehicle, vehicle_id)
            if not v:
                raise ValueError("Veiculo nao encontrado.")
            session.delete(v)
    @staticmethod
    def list(search: str = "") -> List[dict]:
        with session_scope() as session:
            query = session.query(Vehicle)
            if search:
                s = f"%{search}%"
                query = query.filter((Vehicle.placa.ilike(s)) | (Vehicle.modelo.ilike(s)) | (Vehicle.categoria.ilike(s)))
            query = query.order_by(Vehicle.placa)
            return [_to_dict(v) for v in query.all()]
def _to_dict(v: Vehicle) -> dict:
    return {"id": v.id, "placa": v.placa, "modelo": v.modelo, "marca": v.marca, "ano": v.ano, "categoria": v.categoria, "status": v.status, "observacoes": v.observacoes, "created_at": v.created_at}

--- FILE: app/services/admin_service.py ---
[NOTA: contem hash PBKDF2 e split de salt. Ver arquivo fonte para detalhes completos.]
from __future__ import annotations
import hashlib
import logging
import secrets
from typing import Optional
from app.core.database import session_scope
from app.models.admin import Admin
from app.models.setting import Setting
logger = logging.getLogger(__name__)
class AdminService:
    _MASTER_KEY = "master_password_hash"
    @staticmethod
    def _hash_password(password: str, salt: bytes | None = None) -> tuple[str, bytes]:
        if salt is None:
            salt = secrets.token_bytes(16)
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return key.hex(), salt
    @staticmethod
    def _verify_password(password: str, stored_hash: str, salt: bytes) -> bool:
        key, _ = AdminService._hash_password(password, salt)
        return secrets.compare_digest(key, stored_hash)
    @staticmethod
    def get_master_password_hash() -> str | None:
        with session_scope() as session:
            s = session.query(Setting).filter_by(chave=AdminService._MASTER_KEY).first()
            return s.valor if s else None
    @staticmethod
    def set_master_password(password: str) -> None:
        hash_hex, salt = AdminService._hash_password(password)
        stored = f"{hash_hex}:{salt.hex()}"
        with session_scope() as session:
            s = session.query(Setting).filter_by(chave=AdminService._MASTER_KEY).first()
            if s:
                s.valor = stored
            else:
                session.add(Setting(chave=AdminService._MASTER_KEY, valor=stored))
    @staticmethod
    def validate_master_password(password: str) -> bool:
        stored = AdminService.get_master_password_hash()
        if not stored:
            return False
        try:
            hash_hex, salt_hex = stored.split(":")
            return AdminService._verify_password(password, hash_hex, bytes.fromhex(salt_hex))
        except Exception:
            return False
    @staticmethod
    def create_admin(*, username: str, password: str, nome_completo: str, is_master: bool = False) -> dict:
        with session_scope() as session:
            existing = session.query(Admin).filter_by(username=username).first()
            if existing:
                raise ValueError(f"Usuario '{username}' ja existe.")
            hash_hex, salt = AdminService._hash_password(password)
            admin = Admin(username=username, password_hash=f"{hash_hex}:{salt.hex()}", nome_completo=nome_completo, is_master=int(is_master), is_active=1)
            session.add(admin)
            session.flush()
            session.refresh(admin)
            return _to_dict(admin)
    @staticmethod
    def authenticate(username: str, password: str) -> dict | None:
        with session_scope() as session:
            admin = session.query(Admin).filter_by(username=username, is_active=1).first()
            if not admin:
                return None
            try:
                hash_hex, salt_hex = admin.password_hash.split(":")
                if AdminService._verify_password(password, hash_hex, bytes.fromhex(salt_hex)):
                    return _to_dict(admin)
            except Exception:
                logger.exception("Falha na verificacao de senha")
            return None
    @staticmethod
    def get_all() -> list[dict]:
        with session_scope() as session:
            admins = session.query(Admin).order_by(Admin.id).all()
            return [_to_dict(a) for a in admins]
    @staticmethod
    def update_admin(admin_id: int, *, nome_completo: str, username: str, new_password: str | None = None) -> None:
        with session_scope() as session:
            admin = session.get(Admin, admin_id)
            if not admin:
                raise ValueError("Administrador nao encontrado.")
            if admin.username != username:
                existing = session.query(Admin).filter_by(username=username).first()
                if existing:
                    raise ValueError(f"Usuario '{username}' ja existe.")
            admin.nome_completo = nome_completo
            admin.username = username
            if new_password:
                hash_hex, salt = AdminService._hash_password(new_password)
                admin.password_hash = f"{hash_hex}:{salt.hex()}"
    @staticmethod
    def deactivate_admin(admin_id: int) -> bool:
        with session_scope() as session:
            admin = session.get(Admin, admin_id)
            if not admin:
                return False
            admin.is_active = 0
            return True
    @staticmethod
    def hard_delete_admin(admin_id: int) -> bool:
        with session_scope() as session:
            admin = session.get(Admin, admin_id)
            if not admin:
                return False
            session.delete(admin)
            return True
def _to_dict(admin: Admin) -> dict:
    return {"id": admin.id, "username": admin.username, "nome_completo": admin.nome_completo, "is_master": bool(admin.is_master), "is_active": bool(admin.is_active), "created_at": admin.created_at}

--- FILE: app/services/audit_service.py (NOVO) ---
from __future__ import annotations
import logging
from datetime import datetime
from typing import List
from app.core.database import session_scope
from app.models.audit_log import AuditLog
logger = logging.getLogger(__name__)
class AuditService:
    @staticmethod
    def log(*, username: str, acao: str, entidade: str, entidade_id: int | None, descricao: str, data_retroativa: datetime | None = None) -> None:
        with session_scope() as session:
            log = AuditLog(usuario=username, acao=acao, entidade=entidade, entidade_id=entidade_id, descricao=descricao, data_retroativa=data_retroativa)
            session.add(log)
            logger.info("Auditoria: %s por %s (entidade=%s id=%s)", acao, username, entidade, entidade_id)
    @staticmethod
    def list_all(limit: int = 2000) -> List[dict]:
        with session_scope() as session:
            logs = session.query(AuditLog).order_by(AuditLog.data_hora.desc()).limit(limit).all()
            return [{"id": l.id, "usuario": l.usuario, "acao": l.acao, "entidade": l.entidade, "entidade_id": l.entidade_id, "descricao": l.descricao, "data_hora": l.data_hora, "data_retroativa": l.data_retroativa} for l in logs]


================================================================================
ARQUIVOS DE CONTEXTO DESTE CHAT - ACTIVITY SERVICE E PAGES
================================================================================


--- FILE: app/services/activity_service.py (MODIFICADO - hooks de auditoria) ---
[NOTA: contem dataclass ActivityFilters e funcoes _apply_filters, _activity_to_dict, _vehicle_to_dict. Ver arquivo fonte para metodos list_all, list_paginated, kpis completos.]
from __future__ import annotations
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy import func, select, desc, asc
from app.core.database import session_scope
from app.models.activity import Activity
from app.models.vehicle import Vehicle
from app.services.audit_service import AuditService
logger = logging.getLogger(__name__)
@dataclass
class ActivityFilters:
    vehicle_id: Optional[int] = None
    start_dt: Optional[datetime] = None
    end_dt: Optional[datetime] = None
    categoria: Optional[str] = None
class ActivityService:
    def create(self, *, veiculo_id: int, data_hora: datetime, quantidade: int, observacoes: str | None, username: str | None = None) -> dict:
        if quantidade < 0:
            raise ValueError("Quantidade nao pode ser negativa.")
        placa = "?"
        with session_scope() as s:
            a = Activity(veiculo_id=veiculo_id, data_hora=data_hora, quantidade=quantidade, observacoes=(observacoes or "").strip() or None)
            s.add(a)
            s.flush()
            s.refresh(a)
            v = s.get(Vehicle, veiculo_id)
            if v:
                placa = v.placa
            logger.info("Atividade criada (id=%s)", a.id)
            result = _activity_to_dict(a)
        if username:
            agora = datetime.now()
            desc = f"{username} registrou {quantidade} atividade(s) do veiculo de placa {placa} no dia {agora.strftime('%d/%m/%Y')} as {agora.strftime('%H:%M')}h para o dia {data_hora.strftime('%d/%m/%Y')}"
            AuditService.log(username=username, acao="CREATE", entidade="activity", entidade_id=result["id"], descricao=desc, data_retroativa=data_hora)
        return result
    def update(self, activity_id: int, *, veiculo_id: int, data_hora: datetime, quantidade: int, observacoes: str | None, username: str | None = None) -> None:
        if quantidade < 0:
            raise ValueError("Quantidade nao pode ser negativa.")
        placa = "?"
        with session_scope() as s:
            a = s.get(Activity, activity_id)
            if not a:
                raise ValueError("Atividade nao encontrada.")
            a.veiculo_id = veiculo_id
            a.data_hora = data_hora
            a.quantidade = quantidade
            a.observacoes = (observacoes or "").strip() or None
            v = s.get(Vehicle, veiculo_id)
            if v:
                placa = v.placa
            logger.info("Atividade atualizada (id=%s)", activity_id)
        if username:
            agora = datetime.now()
            desc = f"{username} editou atividade do veiculo de placa {placa} no dia {agora.strftime('%d/%m/%Y')} as {agora.strftime('%H:%M')}h (data retroativa: {data_hora.strftime('%d/%m/%Y')})"
            AuditService.log(username=username, acao="UPDATE", entidade="activity", entidade_id=activity_id, descricao=desc, data_retroativa=data_hora)
    def delete(self, activity_id: int, username: str | None = None) -> None:
        placa = "?"
        data_hora = None
        with session_scope() as s:
            a = s.get(Activity, activity_id)
            if not a:
                return
            v = s.get(Vehicle, a.veiculo_id)
            if v:
                placa = v.placa
            data_hora = a.data_hora
            s.delete(a)
            logger.info("Atividade removida (id=%s)", activity_id)
        if username and data_hora:
            agora = datetime.now()
            desc = f"{username} excluiu atividade do veiculo de placa {placa} no dia {agora.strftime('%d/%m/%Y')} as {agora.strftime('%H:%M')}h (data retroativa: {data_hora.strftime('%d/%m/%Y')})"
            AuditService.log(username=username, acao="DELETE", entidade="activity", entidade_id=activity_id, descricao=desc, data_retroativa=data_hora)

--- FILE: app/ui/pages/activity_register_page.py (MODIFICADO - recebe admin_data) ---
[NOTA: contem imports PySide6. Layout vertical espacoso padrao. Ver arquivo fonte para stylesheet completo.]
from __future__ import annotations
import logging
from datetime import datetime
from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import QComboBox, QDateEdit, QHBoxLayout, QLabel, QMessageBox, QPushButton, QSpinBox, QTextEdit, QVBoxLayout, QWidget
from app.services.activity_service import ActivityService
from app.services.vehicle_service import VehicleService
from app.ui.icons import icon
logger = logging.getLogger(__name__)
class ActivityRegisterPage(QWidget):
    activity_changed = Signal()
    def __init__(self, *, vehicle_service: VehicleService, activity_service: ActivityService, admin_data: dict | None = None, parent=None) -> None:
        super().__init__(parent)
        self.vehicle_service = vehicle_service
        self.activity_service = activity_service
        self.admin_data = admin_data or {}
        # ... layout UI padrao com title, subtitle, campos veiculo/data/quantidade/observacoes ...
    def refresh_vehicles(self) -> None:
        try:
            vehicles = self.vehicle_service.list("")
            self.cb_vehicle.clear()
            self.cb_vehicle.addItem("-- Selecione um veiculo --", None)
            for v in vehicles:
                self.cb_vehicle.addItem(f"{v['placa']} - {v['modelo']}", v["id"])
        except Exception:
            logger.exception("Falha ao carregar veiculos para cadastro de atividade")
    def clear_form(self) -> None:
        self.cb_vehicle.setCurrentIndex(0)
        self.dt.setDate(QDate.currentDate())
        self.sp_quantidade.setValue(1)
        self.ed_obs.clear()
    def save(self) -> None:
        if self.cb_vehicle.currentData() is None:
            QMessageBox.warning(self, "Validacao", "Selecione um veiculo cadastrado.")
            return
        try:
            data_py = self.dt.date().toPython()
            agora = datetime.now()
            data_hora = datetime(year=data_py.year, month=data_py.month, day=data_py.day, hour=agora.hour, minute=agora.minute, second=agora.second)
            self.activity_service.create(
                veiculo_id=int(self.cb_vehicle.currentData()),
                data_hora=data_hora,
                quantidade=self.sp_quantidade.value(),
                observacoes=self.ed_obs.toPlainText().strip() or None,
                username=self.admin_data.get("username"),
            )
            self.clear_form()
            self.activity_changed.emit()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))

--- FILE: app/ui/pages/history_page.py (MODIFICADO - passa username) ---
[NOTA: contem filtros em QGridLayout, paginacao, botoes PDF/email/config. Ver arquivo fonte para layout completo e metodos generate_pdf/generate_and_send_email.]
from __future__ import annotations
import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Callable
from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QComboBox, QCompleter, QDateEdit, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton, QSpinBox, QTableView, QVBoxLayout, QWidget
from app.core.config_store import ConfigStore
from app.services.activity_service import ActivityFilters, ActivityService
from app.services.category_service import CategoryService
from app.services.email_service import EmailService
from app.services.report_service import ReportService, ReportSummary
from app.services.vehicle_service import VehicleService
from app.ui.dialogs.activity_dialog import ActivityDialog
from app.ui.icons import icon
from app.ui.models.activity_table_model import ActivityTableModel
logger = logging.getLogger(__name__)
class HistoryPage(QWidget):
    def __init__(self, *, vehicle_service: VehicleService, activity_service: ActivityService, report_service: ReportService, email_service: EmailService, config_store: ConfigStore, open_settings: Callable[[], None], admin_data: dict | None = None, parent=None) -> None:
        super().__init__(parent)
        self.vehicle_service = vehicle_service
        self.activity_service = activity_service
        self.report_service = report_service
        self.email_service = email_service
        self.config_store = config_store
        self.open_settings = open_settings
        self.admin_data = admin_data or {}
        self._generated_by = self.admin_data.get("username", "")
        # ... layout UI completo com filtros, tabela, paginacao ...
    def edit_selected(self) -> None:
        sel = self._selected()
        if not sel:
            QMessageBox.information(self, "Selecionar", "Selecione uma atividade.")
            return
        a, v = sel
        vehicles = self.vehicle_service.list("")
        dlg = ActivityDialog(self, vehicles=vehicles, activity=a)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self.activity_service.update(a["id"], username=self.admin_data.get("username"), **dlg.values())
            self.refresh()
        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))
    def delete_selected(self) -> None:
        sel = self._selected()
        if not sel:
            QMessageBox.information(self, "Selecionar", "Selecione uma atividade.")
            return
        a, v = sel
        dh = a.get("data_hora")
        data_str = dh.strftime("%d/%m/%Y") if hasattr(dh, "strftime") else str(dh)[:10] if dh else ""
        r = QMessageBox.question(self, "Confirmar", f"Excluir a atividade de {v.get('placa','')} em {data_str}?")
        if r != QMessageBox.Yes:
            return
        try:
            self.activity_service.delete(a["id"], username=self.admin_data.get("username"))
            self.refresh()
        except Exception:
            logger.exception("Falha ao excluir atividade")
            QMessageBox.critical(self, "Erro", "Falha ao excluir. Veja o log.")


================================================================================
ARQUIVOS DE CONTEXTO DESTE CHAT - ADMIN PAGE, DIALOGS E MAIN WINDOW
================================================================================
