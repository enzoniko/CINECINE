from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import AdminLoginForm, CompraForm

from app.Backend.main import sessoes, printar_filmes, printar_sessoes, sala_mais_vazia
from app.Backend.helpers import most_empty
from app.Backend.sala import salas, letras
from app.Backend.pagamento import Pagamento
payments = {}
@app.route('/', methods=['GET', 'POST'])
def escolha_do_filme():
    sessions = {}
    for sessao in sessoes:
        if sessao.get_nome() not in sessions:
           
            sessions[sessao.get_nome()] = []

            for each in [s for s in sessoes if s.get_nome() == sessao.get_nome()]:
                new = [each.get_generos(), each.get_legenda(), each.get_DDD(), each.get_horarios(), each.get_id()]
                sessions[sessao.get_nome()].append(new)

    return render_template('escolha_do_filme.html', title='Filmes', filmes=printar_filmes(), sessions=sessions, sessoes=sessoes)

@app.route('/poltronas/<id_sessao>/<horario>', methods=['GET', 'POST'])
def poltronas(id_sessao, horario):
    
    session = [sessao for sessao in sessoes if sessao.get_id() == id_sessao][0]
    ingressos = request.form.getlist('poltronas')
    quantidade_lugares_disponiveis_sala_mais_vazia = most_empty(
        [
            [
                sala.get_cronograma()[
                    f"{id_sessao} {horario}"
                ]
                for sessao in sala.get_sessoes()
                if sessao.get_id() == id_sessao
            ]
            for sala in salas
        ]
    )

    sala = sala_mais_vazia(quantidade_lugares_disponiveis_sala_mais_vazia, session)
    poltronas = sala.get_cronograma()[f"{id_sessao} {horario}"]
    poltronas = [poltronas[i-1][::-1] for i in range(len(poltronas), 0, -1)]
    form = CompraForm()
    if form.validate_on_submit():
        if form.meias.data > len(ingressos):
            flash('Você não pode comprar mais meias do que ingressos')
        elif len(ingressos) >  quantidade_lugares_disponiveis_sala_mais_vazia:
            flash('Não há lugares suficientes disponíveis')
        else:
            # Made letras and numeros dynamic, test out later...
            poltronas_a_preencher = [letras[::-1][int(ingressos[i].split()[0])]+[str(x+1) for x in range(len(poltronas[0]))][int(ingressos[i].split()[1])] for i in range(len(ingressos))]
            sala.preencher_poltronas(poltronas_a_preencher, id_sessao, horario)
            flash(f'Você comprou {len(ingressos)} ingressos e {form.meias.data} meias-entradas.')
            pagamento = Pagamento(len(ingressos), form.meias.data)
            payments[f"{pagamento.id}"] = pagamento
            return redirect(url_for('pagamentos', pagamento_id=pagamento.id))

    sala.printar_poltronas(id_sessao, horario)

    return render_template('poltronas.html', title='Sessoes', horario = horario, sessao = session, form=form, poltronas=poltronas)

@app.route('/pagamentos/<pagamento_id>', methods=['GET', 'POST'])
def pagamentos(pagamento_id):
    print(payments)
    valor_total = payments[pagamento_id].get_valor()
    return render_template('pagamentos.html', title='Pagamentos', valor_total=valor_total)


@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.password.data == "adminadmin":
            # flash(" ", "class")
            flash("Admin logged in successfully!")
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check username and password")
    return render_template('adminLogin.html', title="Admin Login", form=form)
