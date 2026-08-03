# \# 🚛 Dashboard Frotas — MADEMAXI

# 

# \&lt;p align="center"\&gt;

# &#x20; \&lt;img src="app/assets/logo\_mademaxi.png" alt="MADEMAXI Logo" width="180"\&gt;

# \&lt;/p\&gt;

# 

# \&lt;p align="center"\&gt;

# &#x20; \&lt;b\&gt;Sistema de Gestao de Atividades de Veiculos\&lt;/b\&gt;\&lt;br\&gt;

# &#x20; \&lt;i\&gt;MADEMAXI — Materiais de Construcao e Ferragem\&lt;/i\&gt;

# \&lt;/p\&gt;

# 

# \&lt;p align="center"\&gt;

# &#x20; \&lt;img src="https://img.shields.io/badge/Python-3.14-blue?logo=python\&logoColor=white"\&gt;

# &#x20; \&lt;img src="https://img.shields.io/badge/PySide6-6.10+-green?logo=qt\&logoColor=white"\&gt;

# &#x20; \&lt;img src="https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite\&logoColor=white"\&gt;

# &#x20; \&lt;img src="https://img.shields.io/badge/License-Proprietary-red"\&gt;

# \&lt;/p\&gt;

# 

# \---

# 

# \## 📋 Sobre

# 

# O \*\*Dashboard Frotas\*\* e um aplicativo desktop desenvolvido para a \*\*MADEMAXI\*\* com o objetivo de centralizar o controle de atividades realizadas pela frota de veiculos da empresa.

# 

# O sistema permite o cadastro completo de veiculos, registro agil de atividades (quantidade de servicos realizados), acompanhamento em tempo real via dashboard com KPIs e graficos, geracao de relatorios PDF profissionais e envio automatizado por e-mail com agendamento semanal.

# 

# \&gt; ⚠️ Este software e propriedade exclusiva da \*\*MADEMAXI\*\*. Todos os direitos reservados (C) 2026.

# 

# \---

# 

# \## ✨ Funcionalidades

# 

# | Modulo | Descricao | Status |

# |--------|-----------|--------|

# | 🚗 \*\*Cadastro de Veiculos\*\* | CRUD completo com placa, modelo, marca, ano, categoria e status | ✅ |

# | 📝 \*\*Registro de Atividades\*\* | Vinculacao rapida de atividades a veiculos com data e quantidade | ✅ |

# | 📊 \*\*Dashboard\*\* | KPIs em tempo real, graficos de barras (top veiculos) e linha (atividades por dia) | ✅ |

# | 📜 \*\*Historico\*\* | Tabela paginada com filtros por veiculo, periodo, categoria e ordenacao | ✅ |

# | 📄 \*\*Relatorios PDF\*\* | Geracao de PDFs profissionais com identidade visual MADEMAXI | ✅ |

# | 📧 \*\*E-mail SMTP\*\* | Envio manual ou automatico de relatorios com corpo HTML responsivo | ✅ |

# | ⏰ \*\*Agendamento\*\* | Envio semanal automatico as segundas-feiras as 08:00 com catch-up | ✅ |

# | 🎨 \*\*Temas\*\* | Suporte a tema Dark (padrao) e Light com paleta global | ✅ |

# 

# \---

# 

# \## 🛠 Stack Tecnica

# 

# \- \*\*Python\*\* 3.14.6 — Linguagem principal

# \- \*\*PySide6\*\* \&gt;= 6.10.1 — Framework GUI (Qt6)

# \- \*\*SQLite + SQLAlchemy\*\* \&gt;= 2.0.40 — Banco de dados local

# \- \*\*PyQtGraph\*\* \&gt;= 0.14.0 — Graficos interativos

# \- \*\*ReportLab\*\* \&gt;= 4.3.1 — Geracao de PDFs

# \- \*\*APScheduler\*\* \&gt;= 3.11.0 — Agendamento de tarefas

# \- \*\*PyInstaller\*\* — Compilacao para executavel standalone

# \- \*\*Inno Setup\*\* — Gerador de instalador Windows

# 

# \---

# 

# \## 🚀 Instalacao para Desenvolvimento

# 

# ```bash

# \# Clone o repositorio

# git clone https://github.com/MaiconDAS/Dashboard\_Frotas.git

# cd Dashboard\_Frotas

# 

# \# Crie e ative o ambiente virtual

# python -m venv .venv

# .venv\\Scripts\\Activate.ps1

# 

# \# Instale as dependencias

# pip install -r requirements.txt

# 

# \# Execute o aplicativo

# python run.py

