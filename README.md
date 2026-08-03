# 🚛 Dashboard Frotas — MADEMAXI

<p align="center">
  <img src="app/assets/logo_mademaxi.png" alt="MADEMAXI Logo" width="180">
</p>

<p align="center">
  <b>Sistema de Gestão de Atividades de Veículos</b><br>
  <i>MADEMAXI — Materiais de Construção e Ferragem</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/PySide6-6.10+-green?logo=qt&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/License-Proprietary-red">
</p>

---

## 📋 Sobre

O **Dashboard Frotas** é um aplicativo desktop desenvolvido para a **MADEMAXI** com o objetivo de centralizar o controle de atividades realizadas pela frota de veículos da empresa.

O sistema permite o cadastro completo de veículos, registro ágil de atividades (quantidade de serviços realizados), acompanhamento em tempo real via dashboard com KPIs e gráficos, geração de relatórios PDF profissionais e envio automatizado por e-mail com agendamento semanal.

> ⚠️ Este software é propriedade exclusiva da **MADEMAXI**. Todos os direitos reservados © 2026.

---

## ✨ Funcionalidades

| Módulo | Descrição | Status |
|--------|-----------|--------|
| 🚗 **Cadastro de Veículos** | CRUD completo com placa, modelo, marca, ano, categoria e status | ✅ |
| 📝 **Registro de Atividades** | Vinculação rápida de atividades a veículos com data e quantidade | ✅ |
| 📊 **Dashboard** | KPIs em tempo real, gráficos de barras (top veículos) e linha (atividades por dia) | ✅ |
| 📜 **Histórico** | Tabela paginada com filtros por veículo, período, categoria e ordenação | ✅ |
| 📄 **Relatórios PDF** | Geração de PDFs profissionais com identidade visual MADEMAXI | ✅ |
| 📧 **E-mail SMTP** | Envio manual ou automático de relatórios com corpo HTML responsivo | ✅ |
| ⏰ **Agendamento** | Envio semanal automático às segundas-feiras às 08:00 com catch-up | ✅ |
| 🎨 **Temas** | Suporte a tema Dark (padrão) e Light com paleta global | ✅ |

---

## 🛠 Stack Técnica

- **Python** 3.14.6 — Linguagem principal
- **PySide6** >= 6.10.1 — Framework GUI (Qt6)
- **SQLite + SQLAlchemy** >= 2.0.40 — Banco de dados local
- **PyQtGraph** >= 0.14.0 — Gráficos interativos
- **ReportLab** >= 4.3.1 — Geração de PDFs
- **APScheduler** >= 3.11.0 — Agendamento de tarefas
- **PyInstaller** — Compilação para executável standalone
- **Inno Setup** — Gerador de instalador Windows

---

## 🚀 Instalação para Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/MaiconDAS/Dashboard_Frotas.git
cd Dashboard_Frotas

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo
python run.py
```

---

## 📦 Instalação para Usuário Final

Baixe o instalador mais recente na seção **Releases** e execute o arquivo `Dashboard_Frotas_MADEMAXI_Setup_vX.X.X.exe`.

O instalador irá:

- Verificar se existe uma versão anterior instalada e oferecer remoção
- Instalar o software em `C:\Program Files\Dashboard_Frotas`
- Criar atalhos no Menu Iniciar e Área de Trabalho
- Inicializar o banco de dados e configurações limpas

---

## 📁 Estrutura do Projeto

```
Dashboard_Frotas/
├── app/
│   ├── assets/              # Logo e recursos visuais
│   ├── core/                # Config, database, logging, utils
│   ├── models/              # ORM (Veiculo, Atividade, Configuracao)
│   ├── services/            # Regras de negócio (CRUD, PDF, E-mail, Agendador)
│   └── ui/                  # Interface gráfica (páginas, dialogs, models)
├── data/                    # Banco SQLite e configurações (gerado em runtime)
├── dist/                    # Executável compilado (PyInstaller)
├── dist_installer/          # Instalador final (Inno Setup)
├── build_installer.py       # Script de build automatizado
├── Dashboard_Frotas.iss     # Script do Inno Setup
├── credits.txt              # Créditos e direitos autorais
├── requirements.txt         # Dependências Python
├── run.py                   # Ponto de entrada da aplicação
└── README.md                # Este arquivo
```

---

## 🖼 Screenshots

<p align="center">
  <i>Dashboard com KPIs e gráficos em tempo real</i>
</p>

<p align="center">
  <i>Relatório PDF profissional com identidade MADEMAXI</i>
</p>

---

## ⚙️ Configurações

Acesse a aba **Configurações** no software para ajustar:

- **SMTP** — Servidor, porta, remetente e destinatário de e-mail
- **Tema** — Alternar entre Dark e Light
- **Empresa** — Nome e logo personalizado para relatórios
- **Agendamento** — Ativar/desativar envio semanal automático

---

## 🧑‍💻 Desenvolvedor

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/MaiconDAS">
        <img src="https://github.com/MaiconDAS.png?size=100" width="100" style="border-radius: 50%"><br>
        <sub><b>Maicon do Amarilho Silveira</b></sub>
      </a>
    </td>
  </tr>
</table>

🔗 **GitHub:** [github.com/MaiconDAS](https://github.com/MaiconDAS)

---

## 📝 Licença

Este software é propriedade exclusiva da **MADEMAXI — Materiais de Construção e Ferragem**.

Todos os direitos reservados © 2026 MADEMAXI.

É estritamente proibida a reprodução, distribuição ou modificação deste software sem autorização expressa por escrita da MADEMAXI.

Para suporte técnico, entre em contato com o desenvolvedor através do GitHub.

<p align="center">
  <sub>Feito com ❤️ para a <strong>MADEMAXI</strong></sub>
</p>
