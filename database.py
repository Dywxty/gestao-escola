import sqlite3

DATABASE = "escola.db"
def conectar_banco():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row

    # Ativa as chaves estrangeiras do SQLite
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def criar_tabelas():
    conexao = conectar_banco()

    # ALUNOS
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            idade INTEGER NOT NULL
        )
    """)

    # DISCIPLINAS
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo TEXT NOT NULL UNIQUE,
            carga_horaria INTEGER NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # TURMAS
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ano_letivo INTEGER NOT NULL,
            periodo TEXT NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ALUNO e TURMA - relação
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS aluno_turma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            turma_id INTEGER NOT NULL,
            data_matricula DATE NOT NULL DEFAULT CURRENT_DATE,

            FOREIGN KEY (aluno_id)
                REFERENCES alunos(id)
                ON DELETE CASCADE,

            FOREIGN KEY (turma_id)
                REFERENCES turmas(id)
                ON DELETE CASCADE,

            UNIQUE(aluno_id, turma_id)
        )
    """)

    # NOTAS
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            turma_id INTEGER NOT NULL,
            disciplina_id INTEGER NOT NULL,
            nota REAL NOT NULL,
            etapa INTEGER NOT NULL,
            data_lancamento DATE NOT NULL DEFAULT CURRENT_DATE,

            FOREIGN KEY (aluno_id)
                REFERENCES alunos(id)
                ON DELETE CASCADE,

            FOREIGN KEY (turma_id)
                REFERENCES turmas(id)
                ON DELETE CASCADE,

            FOREIGN KEY (disciplina_id)
                REFERENCES disciplinas(id)
                ON DELETE CASCADE
        )
    """)

    # FREQUÊNCIAS
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS frequencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            turma_id INTEGER NOT NULL,
            disciplina_id INTEGER NOT NULL,
            data_aula DATE NOT NULL,
            presente INTEGER NOT NULL,

            FOREIGN KEY (aluno_id)
                REFERENCES alunos(id)
                ON DELETE CASCADE,

            FOREIGN KEY (turma_id)
                REFERENCES turmas(id)
                ON DELETE CASCADE,

            FOREIGN KEY (disciplina_id)
                REFERENCES disciplinas(id)
                ON DELETE CASCADE
        )
    """)

    conexao.commit()
    conexao.close()