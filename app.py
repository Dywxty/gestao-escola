from flask import Flask, request

from database import criar_tabelas, conectar_banco

app = Flask(__name__)

criar_tabelas()

@app.route("/")
def inicio():
    return "Sistema de Gerenciamento Escolar"

#___________________________________________________________________________________________
@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    dados = request.get_json()

    nome = dados["nome"]
    email = dados["email"]
    idade = dados["idade"]

    conexao = conectar_banco()

    conexao.execute("""
        INSERT INTO alunos (nome, email, idade)
        VALUES (?, ?, ?)
    """, (nome, email, idade))

    conexao.commit()
    conexao.close()

    return "Aluno cadastrado com sucesso", 200


@app.route("/alunos", methods=["GET"])
def buscar_alunos():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM alunos
    """)

    alunos = cursor.fetchall()

    conexao.close()

    return [dict(aluno) for aluno in alunos], 200
#___________________________________________________________________________________________

@app.route("/disciplinas", methods=["POST"])
def cadastrar_disciplina():
    dados = request.get_json()

    nome = dados["nome"]
    codigo = dados["codigo"]
    carga_horaria = dados["carga_horaria"]

    conexao = conectar_banco()

    conexao.execute("""
        INSERT INTO disciplinas (nome, codigo, carga_horaria)
        VALUES (?, ?, ?)
    """, (nome, codigo, carga_horaria))

    conexao.commit()
    conexao.close()

    return "Disciplina cadastrada com sucesso", 200


@app.route("/disciplinas", methods=["GET"])
def buscar_disciplinas():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM disciplinas
    """)

    disciplinas = cursor.fetchall()

    conexao.close()

    return [dict(disciplina) for disciplina in disciplinas], 200

#___________________________________________________________________________________________

@app.route("/turmas", methods=["POST"])
def cadastrar_turma():
    dados = request.get_json()

    nome = dados["nome"]
    ano_letivo = dados["ano_letivo"]
    periodo = dados["periodo"]

    conexao = conectar_banco()

    conexao.execute("""
        INSERT INTO turmas (nome, ano_letivo, periodo)
        VALUES (?, ?, ?)
    """, (nome, ano_letivo, periodo))

    conexao.commit()
    conexao.close()

    return "Turma cadastrada com sucesso", 200


@app.route("/turmas", methods=["GET"])
def buscar_turmas():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM turmas
    """)

    turmas = cursor.fetchall()

    conexao.close()

    return [dict(turma) for turma in turmas], 200

#___________________________________________________________________________________________

@app.route("/aluno-turma", methods=["POST"])
def matricular_aluno():
    dados = request.get_json()

    aluno_id = dados["aluno_id"]
    turma_id = dados["turma_id"]

    conexao = conectar_banco()

    conexao.execute("""
        INSERT INTO aluno_turma (aluno_id, turma_id)
        VALUES (?, ?)
    """, (aluno_id, turma_id))

    conexao.commit()
    conexao.close()

    return "Aluno matriculado na turma com sucesso", 200

#___________________________________________________________________________________________

@app.route("/alunos/<int:aluno_id>/turmas", methods=["GET"])
def buscar_turmas_aluno(aluno_id):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            turmas.id,
            turmas.nome,
            turmas.ano_letivo,
            turmas.periodo,
            aluno_turma.data_matricula
        FROM aluno_turma
        INNER JOIN turmas
            ON turmas.id = aluno_turma.turma_id
        WHERE aluno_turma.aluno_id = ?
    """, (aluno_id,))

    turmas = cursor.fetchall()

    conexao.close()

    return [dict(turma) for turma in turmas], 200

#___________________________________________________________________________________________

@app.route("/turmas/<int:turma_id>/alunos", methods=["GET"])
def buscar_alunos_turma(turma_id):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            alunos.id,
            alunos.nome,
            alunos.email,
            alunos.idade,
            aluno_turma.data_matricula
        FROM aluno_turma
        INNER JOIN alunos
            ON alunos.id = aluno_turma.aluno_id
        WHERE aluno_turma.turma_id = ?
    """, (turma_id,))

    alunos = cursor.fetchall()

    conexao.close()

    return [dict(aluno) for aluno in alunos], 200

#___________________________________________________________________________________________

@app.route("/notas", methods=["POST"])
def cadastrar_nota():
    dados = request.get_json()

    aluno_id = dados["aluno_id"]
    turma_id = dados["turma_id"]
    disciplina_id = dados["disciplina_id"]
    nota = dados["nota"]
    etapa = dados["etapa"]

    conexao = conectar_banco()

    conexao.execute("""
        INSERT INTO notas (
            aluno_id,
            turma_id,
            disciplina_id,
            nota,
            etapa
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        aluno_id,
        turma_id,
        disciplina_id,
        nota,
        etapa
    ))

    conexao.commit()
    conexao.close()

    return "Nota cadastrada com sucesso", 200

#___________________________________________________________________________________________

@app.route("/alunos/<int:aluno_id>/notas", methods=["GET"])
def buscar_notas_aluno(aluno_id):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            notas.id,
            alunos.nome AS aluno,
            turmas.nome AS turma,
            disciplinas.nome AS disciplina,
            notas.nota,
            notas.etapa,
            notas.data_lancamento
        FROM notas

        INNER JOIN alunos
            ON alunos.id = notas.aluno_id

        INNER JOIN turmas
            ON turmas.id = notas.turma_id

        INNER JOIN disciplinas
            ON disciplinas.id = notas.disciplina_id

        WHERE notas.aluno_id = ?

        ORDER BY disciplinas.nome, notas.etapa
    """, (aluno_id,))

    notas = cursor.fetchall()

    conexao.close()

    return [dict(nota) for nota in notas], 200

#___________________________________________________________________________________________

@app.route("/frequencias", methods=["POST"])
def cadastrar_frequencia():
    dados = request.get_json()

    aluno_id = dados["aluno_id"]
    turma_id = dados["turma_id"]
    disciplina_id = dados["disciplina_id"]
    data_aula = dados["data_aula"]
    presente = dados["presente"]

    conexao = conectar_banco()

    conexao.execute("""
        INSERT INTO frequencias (
            aluno_id,
            turma_id,
            disciplina_id,
            data_aula,
            presente
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        aluno_id,
        turma_id,
        disciplina_id,
        data_aula,
        presente
    ))

    conexao.commit()
    conexao.close()

    return "Frequência cadastrada com sucesso", 200

#___________________________________________________________________________________________

@app.route("/alunos/<int:aluno_id>/frequencias", methods=["GET"])
def buscar_frequencias_aluno(aluno_id):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            frequencias.id,
            alunos.nome AS aluno,
            turmas.nome AS turma,
            disciplinas.nome AS disciplina,
            frequencias.data_aula,
            frequencias.presente
        FROM frequencias

        INNER JOIN alunos
            ON alunos.id = frequencias.aluno_id

        INNER JOIN turmas
            ON turmas.id = frequencias.turma_id

        INNER JOIN disciplinas
            ON disciplinas.id = frequencias.disciplina_id

        WHERE frequencias.aluno_id = ?

        ORDER BY frequencias.data_aula DESC
    """, (aluno_id,))

    frequencias = cursor.fetchall()

    conexao.close()

    return [dict(frequencia) for frequencia in frequencias], 200

#___________________________________________________________________________________________



if __name__ == "__main__":
    app.run(debug=True)

