# Release v2.2.0 - Dashboard Frotas MADEMAXI

**Data:** 06 de agosto de 2026
**Desenvolvedor:** Maicon do Amarilho Silveira
**Empresa:** MADEMAXI - Materiais de Construcao e Ferragem

---

## Download

- [Dashboard_Frotas_MADEMAXI_Setup_v2.2.0.exe](https://github.com/MaiconDAS/Dashboard_Frotas/releases/download/v2.2.0/Dashboard_Frotas_MADEMAXI_Setup_v2.2.0.exe)

---

## O que ha de novo

### v2.2.0 - Nome/Identificacao do Veiculo + Memoria de Registro
- Campo "Nome / Identificacao" editavel no cadastro de veiculos
- Memoria persistente no registro de atividades (veiculo e data mantidos apos salvar)
- Combo de veiculo no historico passou a ser somente leitura

### v2.1.0 - Sistema de Auditoria de Atividades
- Tabela de auditoria completa (CREATE / UPDATE / DELETE)
- Dialog de auditoria com filtros e tabela paginada
- Logs detalhados com nome do veiculo, placa e quantidade
- Botao "Auditoria" visivel apenas para administradores master

### v2.0.0 - Login Administrativo + Categorias Customizaveis
- Tela de login com autenticacao PBKDF2
- Cadastro de administradores via atalho F1 + senha mestra
- Perfis: Administrador (master) e Funcionario
- Aba "Gestao" visivel apenas para master
- Categorias de veiculos customizaveis (add/edit/delete)
- Revamp visual completo

### v1.1.0 - Sistema de Login e Cadastro Administrativo
- LoginDialog com logo MADEMAXI
- Autenticacao com hash PBKDF2 + salt
- Senha mestra para cadastro de novos admins
- Soft delete (is_active=False)
- AdminEditDialog com edicao completa

---

## Stack Tecnica

- Python 3.14.6
- PySide6 >= 6.10.1
- SQLite + SQLAlchemy >= 2.0.40
- PyQtGraph >= 0.14.0
- ReportLab >= 4.3.1
- APScheduler >= 3.11.0
- PyInstaller + Inno Setup 7

---

## Instalacao

Execute o instalador `Dashboard_Frotas_MADEMAXI_Setup_v2.2.0.exe`.

Caso ja possua uma versao anterior instalada, o instalador detectara
automaticamente e perguntara se deseja remove-la. Voce tambem podera
escolher manter ou remover o banco de dados existente (veiculos,
registros de atividades, cadastros e senha mestra).

---

## Licenca

Este software e propriedade exclusiva da MADEMAXI.
Distribuicao nao autorizada e estritamente proibida.
Consulte o EULA exibido durante a instalacao.

---

*Dashboard Frotas - MADEMAXI (C) 2026*
