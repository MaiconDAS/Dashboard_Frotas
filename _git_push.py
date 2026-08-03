import os
import subprocess
import sys
from pathlib import Path

BASE = Path(r"C:\Dashboard_Frota_Dev")
os.chdir(BASE)

def run(cmd, check=True):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False, text=True)
    if check and result.returncode != 0:
        print(f"[AVISO] Comando retornou codigo {result.returncode}")
    return result

print("=" * 60)
print("  PUSH PARA GITHUB - Dashboard Frotas MADEMAXI")
print("=" * 60)

# ============================================================
# 1. CONFIGURAR GIT (se necessario)
# ============================================================
print("\n=== 1/6: CONFIGURANDO GIT ===")
run(["git", "config", "--global", "user.email", "maicon@example.com"], check=False)
run(["git", "config", "--global", "user.name", "Maicon do Amarilho Silveira"], check=False)

# ============================================================
# 2. INICIALIZAR REPOSITORIO (se nao existir)
# ============================================================
print("\n=== 2/6: INICIALIZANDO REPOSITORIO ===")
git_dir = BASE / ".git"
if not git_dir.exists():
    run(["git", "init"])
    print("  [OK] Repositorio Git inicializado")
else:
    print("  [OK] Repositorio ja existe")

# ============================================================
# 3. CRIAR .GITIGNORE
# ============================================================
print("\n=== 3/6: CRIANDO .GITIGNORE ===")

gitignore = """# Dados sensiveis e temporarios
data/app.db
data/config.json
data/logs/
*.db
*.log

# Ambiente virtual
.venv/
venv/
env/
ENV/

# Builds e distribuicao
dist/
build/
dist_installer/
*.spec
*.exe
*.msi

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
.eggs/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Sistema operacional
Thumbs.db
.DS_Store
desktop.ini

# Outros
*.tmp
*.bak
"""

gitignore_path = BASE / ".gitignore"
gitignore_path.write_text(gitignore, encoding="utf-8")
print("  [OK] .gitignore criado")

# ============================================================
# 4. ADICIONAR ARQUIVOS
# ============================================================
print("\n=== 4/6: ADICIONANDO ARQUIVOS ===")
run(["git", "add", "."])
print("  [OK] Arquivos adicionados")

# ============================================================
# 5. COMMIT
# ============================================================
print("\n=== 5/6: FAZENDO COMMIT ===")
run(["git", "commit", "-m", "feat: Dashboard Frotas MADEMAXI v1.0.0\n\n- Sincronizacao automatica Historico/Dashboard\n- Registro direto sem confirmacao\n- Dashboard reformulado com dropdown somente leitura\n- PDF profissional com identidade MADEMAXI\n- E-mail HTML profissional compativel Gmail/Outlook\n- Logo MADEMAXI no software e relatorios\n- Build automatizado PyInstaller + Inno Setup\n- Tema dark/light com stylesheet global\n- Agendamento semanal automatico com catch-up"], check=False)

# ============================================================
# 6. CONFIGURAR REMOTE E PUSH
# ============================================================
print("\n=== 6/6: PUSH PARA GITHUB ===")

# Verifica se remote ja existe
result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
if "origin" not in result.stdout:
    run(["git", "remote", "add", "origin", "https://github.com/MaiconDAS/Dashboard_Frotas.git"])

# Renomeia branch para main (se estiver como master)
subprocess.run(["git", "branch", "-M", "main"], capture_output=True)

# Push
result = run(["git", "push", "-u", "origin", "main"], check=False)
if result.returncode != 0:
    print("\n" + "=" * 60)
    print("  PUSH FALHOU - POSSIVEIS CAUSAS:")
    print("=" * 60)
    print("  1. Nao esta logado no GitHub no Git")
    print("  2. O repositorio remoto ja tem commits (conflito)")
    print("  3. Sem permissao no repositorio")
    print("\n  SOLUCOES:")
    print("  - Para login: git config --global credential.helper manager")
    print("  - Para forcar push: git push -u origin main --force")
    print("  - Para puxar primeiro: git pull origin main --rebase")
    print("=" * 60)
    sys.exit(1)

print("\n" + "=" * 60)
print("  PUSH CONCLUIDO COM SUCESSO!")
print("=" * 60)
print("  Repositorio: https://github.com/MaiconDAS/Dashboard_Frotas")
print("=" * 60)
