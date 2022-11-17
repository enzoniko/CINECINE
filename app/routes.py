from datetime import datetime
from random import randint
from typing import Dict, List
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.Backend.sessao import Sessao
from app.forms import AdminLoginForm, CompraForm, EditarSessaoForm
from app.Backend.main import sessoes, printar_filmes, sala_mais_vazia, salas, pagamentos, total_faturado, alterar_sessao
from app.Backend.helpers import load_objects, most_empty, store_objects, lista_strings_para_string
from app.Backend.sala import Sala, letras
from app.Backend.pagamento import Pagamento
import qrcode

payments: Dict[str, Pagamento] = {}
@app.route('/', methods=['GET', 'POST'])
def escolha_do_filme():
    sessions: Dict[str, list] = {}
    for sessao in sessoes:
        # print('nome:', sessao.nome)
        if sessao.nome not in sessions:
           
            sessions[sessao.nome]: list = []
            for each in [s for s in sessoes if s.nome == sessao.nome]:
                new: list = [each.generos, each.DDD, each.legenda, each.horarios, each.id, each.classificacao, each.description, each.imagem]
                sessions[sessao.nome].append(new)

    return render_template('escolha_do_filme.html', title='Filmes', filmes=printar_filmes, sessions=sessions, sessoes=sessoes)

@app.route('/poltronas/<id_sessao>/<horario>', methods=['GET', 'POST'])
def poltronas(id_sessao, horario):
    session: Sessao = [sessao for sessao in sessoes if sessao.id == int(id_sessao)][0]
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

    sala: Sala = sala_mais_vazia(quantidade_lugares_disponiveis_sala_mais_vazia, session)
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
            pagamento: Pagamento = Pagamento(len(ingressos), form.meias.data, forma=form.maneira.data)
            payments[f"{pagamento.id}"]: Pagamento = pagamento
            pagamentos.append(pagamento)
            store_objects(pagamentos, 'app/storage/pagamentos.pkl')
            store_objects(salas, 'app/storage/salas.pkl')
    
            return redirect(url_for('pagamento', pagamento_id=pagamento.id, id_sessao=id_sessao, horario=horario, poltronas=lista_strings_para_string([poltrona.upper() for poltrona in poltronas_a_preencher])))

    sala.printar_poltronas(id_sessao, horario)

    return render_template('poltronas.html', title='Poltronas', letras=letras[::-1][:len(poltronas)], horario = horario, sessao = session, form=form, poltronas=poltronas)

@app.route('/pagamentos/<pagamento_id>/<id_sessao>/<horario>/<poltronas>', methods=['GET', 'POST'])
def pagamento(pagamento_id, id_sessao, horario, poltronas):

    qr = qrcode.make(f"Poltronas: {poltronas} Horário: {horario} ID_SESSAO: {id_sessao} ID_PAGAMENTO: {pagamento_id} Sala {[salas.index(sala) for sala in salas if int(id_sessao) in [sessao.id for sessao in sala.sessoes]][0] + 1}")
    qr.save('app/static/qr.png')
     
    return render_template('pagamentos.html', title='Pagamentos', horario = horario, sessao = [sessao for sessao in sessoes if sessao.id == int(id_sessao)][0], valor_total= payments[pagamento_id].valor, maneira=payments[pagamento_id].forma, poltronas=poltronas, sala=[salas.index(sala) for sala in salas if int(id_sessao) in [sessao.id for sessao in sala.sessoes]][0])


@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    form: AdminLoginForm = AdminLoginForm()
    if form.validate_on_submit() and form.password.data == "adminadmin":
        return redirect(url_for('adminMenu'))
    return render_template('adminLogin.html', title="Admin Login", form=form)

@app.route('/adminMenu', methods=['GET', 'POST'])
def adminMenu():
    sessions: Dict[str, list] = {}
    for sessao in sessoes:
        # print('nome:', sessao.nome)
        if sessao.nome not in sessions:
           
            sessions[sessao.nome]: list = []
            for each in [s for s in sessoes if s.nome == sessao.nome]:
                new: list = [each.generos, each.DDD, each.legenda, each.horarios, each.id, each.classificacao, each.description, each.imagem]
                sessions[sessao.nome].append(new)
    return render_template('adminMenu.html', title="Admin Menu", dados_faturamento=total_faturado(), salas=salas,  filmes=printar_filmes, sessions=sessions, sessoes=sessoes)

@app.route('/editar_sessao/<id_sessao>', methods=['GET', 'POST'])
def editar_sessao(id_sessao):
    if id_sessao == '0':
        print('oi')
        print(sessoes)
        print(Sessao().id)
        sessoes.append(Sessao(nome='-'))
        print('.>>>>>>>>>>>>>>')
        print(sessoes[-1])
        id_sessao = sessoes[-1].id
   
    form: EditarSessaoForm = EditarSessaoForm(titulo=[sessao.nome for sessao in sessoes if sessao.id == int(id_sessao)][0], classificacao=[sessao.classificacao for sessao in sessoes if sessao.id == int(id_sessao)][0], horarios={datetime.strptime(horario, '%H:%M'): datetime.strptime(horario, '%H:%M') for horario in [sessao.horarios for sessao in sessoes if sessao.id == int(id_sessao)][0]}, legenda=[sessao.legenda for sessao in sessoes if sessao.id == int(id_sessao)][0], DDD=[sessao.DDD for sessao in sessoes if sessao.id == int(id_sessao)][0])

    


    if form.validate_on_submit():
        print("validou")
        if form.cancelar.data:
            sessoes.remove([sessao for sessao in sessoes if sessao.id == int(id_sessao)][0])
            s = load_objects('app/storage/sessoes.pkl')
            for sessao in s:
                if sessao.id == int(id_sessao):
                    sessoes.append(sessao)
                    
            for sessao in sessoes:
                if sessao.nome == '-':
                    sessoes.remove(sessao)
            store_objects(sessoes, 'app/storage/sessoes.pkl')
            return redirect(url_for('adminMenu'))
        elif form.aplicar.data:
            sessoes.remove([sessao for sessao in sessoes if sessao.id == int(id_sessao)][0])
            sessao = Sessao(nome = form.titulo.data, classificacao=form.classificacao.data, legenda=form.legenda.data, DDD=form.DDD.data, horarios=[str(horario.data)[:5] for horario in form.horarios], id = int(id_sessao))
            sessoes.append(sessao)
            for sessao in sessoes:
                if sessao.nome == '-':
                    sessoes.remove(sessao)
            return redirect(url_for('editar_sessao', id_sessao=id_sessao))
        elif form.confirmar.data:

            sessao_antiga = [sessao for sessao in sessoes if sessao.id == int(id_sessao)][0]

            for sala in salas:
                if sessao_antiga in sala.sessoes:
                    sala.remover_sessao(sessao_antiga)
            sessoes.remove(sessao_antiga)
            sessao = Sessao(nome = form.titulo.data, classificacao=form.classificacao.data, legenda=form.legenda.data, DDD=form.DDD.data, horarios=[str(horario.data)[:5] for horario in form.horarios], id = int(id_sessao))
            sessoes.append(sessao)
            salas[randint(0,1)].adicionar_sessao(sessao)
            for sessao in sessoes:
                if sessao.nome == '-':
                    sessoes.remove(sessao)
            
            store_objects(sessoes, 'app/storage/sessoes.pkl')
            store_objects(salas, 'app/storage/salas.pkl')
            return redirect(url_for('adminMenu'))

    return render_template('editar_sessao.html', title="Editar Sessão", form=form, sessao = [sessao for sessao in sessoes if sessao.id == int(id_sessao)][0])