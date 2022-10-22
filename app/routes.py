from typing import Dict, List
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.Backend.sessao import Sessao
from app.forms import AdminLoginForm, CompraForm
from app.Backend.main import sessoes, printar_filmes, sala_mais_vazia, salas, pagamentos
from app.Backend.helpers import most_empty, store_objects
from app.Backend.sala import letras
from app.Backend.pagamento import Pagamento

payments: Dict[str, Pagamento] = {}
@app.route('/', methods=['GET', 'POST'])
def escolha_do_filme():
    sessions: Dict[str, list] = {}
    for sessao in sessoes:
        # print('nome:', sessao.nome)
        if sessao.nome not in sessions:
           
            sessions[sessao.nome]: list = []
            for each in [s for s in sessoes if s.nome == sessao.nome]:
                new: list = [each.generos, each.legenda, each.DDD, each.horarios, each.id, each.classificacao, each.description, each.imagem]
                sessions[sessao.nome].append(new)

    return render_template('escolha_do_filme.html', title='Filmes', filmes=printar_filmes, sessions=sessions, sessoes=sessoes)

@app.route('/poltronas/<id_sessao>/<horario>', methods=['GET', 'POST'])
def poltronas(id_sessao, horario):
    session: List[Sessao] = [sessao for sessao in sessoes if sessao.id == int(id_sessao)][0]
    ingressos: List[str] = request.form.getlist('poltronas')
    quantidade_lugares_disponiveis_sala_mais_vazia: int = most_empty(
        [
            [
                sala.cronograma[
                    f"{id_sessao} {horario}"
                ]
                for sessao in sala.sessoes
                if sessao.id == int(id_sessao)
            ]
            for sala in salas
        ]
    )

    sala: Sessao = sala_mais_vazia(quantidade_lugares_disponiveis_sala_mais_vazia, session)
    poltronas: List[List[int]] = sala.cronograma[f"{id_sessao} {horario}"]
    poltronas: List[List[int]] = [poltronas[i-1][::-1] for i in range(len(poltronas), 0, -1)]
    form: CompraForm = CompraForm()
    if form.validate_on_submit():
        if form.meias.data > len(ingressos):
            flash('Você não pode comprar mais meias do que ingressos')
        elif len(ingressos) >  quantidade_lugares_disponiveis_sala_mais_vazia:
            flash('Não há lugares suficientes disponíveis')
        else:
            poltronas_a_preencher: List[str] = [letras[::-1][:len(poltronas)][int(ingressos[i].split()[0])]+[str(x+1) for x in range(len(poltronas[0]))][::-1][int(ingressos[i].split()[1])] for i in range(len(ingressos))]
            sala.preencher_poltronas(poltronas_a_preencher, id_sessao, horario)
            flash(f'Você comprou {len(ingressos)} ingressos e {form.meias.data} meias-entradas.')
            pagamento: Pagamento = Pagamento(len(ingressos), form.meias.data)
            payments[f"{pagamento.id}"]: Pagamento = pagamento
            pagamentos.append(pagamento)
            store_objects(pagamentos, 'app/storage/pagamentos.pkl')
            store_objects(salas, 'app/storage/salas.pkl')
            
    
            return redirect(url_for('pagamento', pagamento_id=pagamento.id))

    sala.printar_poltronas(id_sessao, horario)

    return render_template('poltronas.html', title='Sessoes', horario = horario, sessao = session, form=form, poltronas=poltronas)

@app.route('/pagamentos/<pagamento_id>', methods=['GET', 'POST'])
def pagamento(pagamento_id):
    print(payments)
    valor_total: float = payments[pagamento_id].valor
    return render_template('pagamentos.html', title='Pagamentos', valor_total=valor_total)


@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    form: AdminLoginForm = AdminLoginForm()
    if form.validate_on_submit():
        if form.password.data == "adminadmin":
            # flash(" ", "class")
            flash("Admin logged in successfully!")
            return redirect(url_for('escolha_do_filme'))
        else:
            flash("Login unsuccessful. Please check username and password")
    return render_template('adminLogin.html', title="Admin Login", form=form)

