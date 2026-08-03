# \# ðŸš› Dashboard Frotas â€” MADEMAXI

# 

# \<p align="center"\>

# &#x20; \<img src="app/assets/logo\_mademaxi.png" alt="MADEMAXI Logo" width="180"\>

# \</p\>

# 

# \<p align="center"\>

# &#x20; \<b\>Sistema de Gestao de Atividades de Veiculos\</b\>\<br\>

# &#x20; \<i\>MADEMAXI â€” Materiais de Construcao e Ferragem\</i\>

# \</p\>

# 

# \<p align="center"\>

# &#x20; \<img src="https://img.shields.io/badge/Python-3.14-blue?logo=python\&logoColor=white"\>

# &#x20; \<img src="https://img.shields.io/badge/PySide6-6.10+-green?logo=qt\&logoColor=white"\>

# &#x20; \<img src="https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite\&logoColor=white"\>

# &#x20; \<img src="https://img.shields.io/badge/License-Proprietary-red"\>

# \</p\>

# 

# \---

# 

# \## ðŸ“‹ Sobre

# 

# O \*\*Dashboard Frotas\*\* e um aplicativo desktop desenvolvido para a \*\*MADEMAXI\*\* com o objetivo de centralizar o controle de atividades realizadas pela frota de veiculos da empresa.

# 

# O sistema permite o cadastro completo de veiculos, registro agil de atividades (quantidade de servicos realizados), acompanhamento em tempo real via dashboard com KPIs e graficos, geracao de relatorios PDF profissionais e envio automatizado por e-mail com agendamento semanal.

# 

# \> âš ï¸ Este software e propriedade exclusiva da \*\*MADEMAXI\*\*. Todos os direitos reservados (C) 2026.

# 

# \---

# 

# \## âœ¨ Funcionalidades

# 

# | Modulo | Descricao | Status |

# |--------|-----------|--------|

# | ðŸš— \*\*Cadastro de Veiculos\*\* | CRUD completo com placa, modelo, marca, ano, categoria e status | âœ… |

# | ðŸ“ \*\*Registro de Atividades\*\* | Vinculacao rapida de atividades a veiculos com data e quantidade | âœ… |

# | ðŸ“Š \*\*Dashboard\*\* | KPIs em tempo real, graficos de barras (top veiculos) e linha (atividades por dia) | âœ… |

# | ðŸ“œ \*\*Historico\*\* | Tabela paginada com filtros por veiculo, periodo, categoria e ordenacao | âœ… |

# | ðŸ“„ \*\*Relatorios PDF\*\* | Geracao de PDFs profissionais com identidade visual MADEMAXI | âœ… |

# | ðŸ“§ \*\*E-mail SMTP\*\* | Envio manual ou automatico de relatorios com corpo HTML responsivo | âœ… |

# | â° \*\*Agendamento\*\* | Envio semanal automatico as segundas-feiras as 08:00 com catch-up | âœ… |

# | ðŸŽ¨ \*\*Temas\*\* | Suporte a tema Dark (padrao) e Light com paleta global | âœ… |

# 

# \---

# 

# \## ðŸ›  Stack Tecnica

# 

# \- \*\*Python\*\* 3.14.6 â€” Linguagem principal

# \- \*\*PySide6\*\* \>= 6.10.1 â€” Framework GUI (Qt6)

# \- \*\*SQLite + SQLAlchemy\*\* \>= 2.0.40 â€” Banco de dados local

# \- \*\*PyQtGraph\*\* \>= 0.14.0 â€” Graficos interativos

# \- \*\*ReportLab\*\* \>= 4.3.1 â€” Geracao de PDFs

# \- \*\*APScheduler\*\* \>= 3.11.0 â€” Agendamento de tarefas

# \- \*\*PyInstaller\*\* â€” Compilacao para executavel standalone

# \- \*\*Inno Setup\*\* â€” Gerador de instalador Windows

# 

# \---

# 

# \## ðŸš€ Instalacao para Desenvolvimento

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


