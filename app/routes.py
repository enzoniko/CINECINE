from datetime import datetime
from random import randint
from typing import Dict, List
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.Backend.sessao import Sessao
from app.forms import AdminLoginForm, CompraForm, EditarSessaoForm
from app.Backend.helpers import lugares_disponiveis, load_objects, most_empty, store_objects, lista_strings_para_string
from app.Backend.sala import Sala, letras
from app.Backend.pagamento import Pagamento
from app.Backend.filme import Filme
import qrcode

# Se os arquivos estiverem vazios guarda novos objetos (pra iniciar com algo), se tiver objetos para serem lidos, carrega
filmes: List[Filme] = list(load_objects('app/storage/filmes.pkl')) or store_objects([Filme("O Senhor dos Aneis"), Filme("Homens de Preto")], "app/storage/filmes.pkl")

sessoes: List[Sessao] = list(load_objects('app/storage/sessoes.pkl')) or store_objects([Sessao(nome = 'O Senhor dos Aneis', legenda = False, DDD = False, horarios = ['15:00', '20:00']), Sessao(nome = 'O Senhor dos Aneis', legenda = False, DDD = False, horarios = ['15:00', '23:00']), Sessao(nome = 'Homens de Preto', legenda = True, DDD = False, horarios = ['22:00', '23:00'])], "app/storage/sessoes.pkl")

if not list(load_objects('app/storage/salas.pkl')):
    salas: List[Sala] = [Sala(), Sala()]
    salas[0].adicionar_sessao(sessoes[0])
    salas[1].adicionar_sessao(sessoes[1])
    salas[1].adicionar_sessao(sessoes[2])
    salas: List[Sala] = store_objects(salas, "app/storage/salas.pkl")
else:
    salas: List[Sala] = list(load_objects('app/storage/salas.pkl'))

pagamentos: List[Pagamento] = list(load_objects('app/storage/pagamentos.pkl')) or store_objects([], "app/storage/pagamentos.pkl")

payments: Dict[str, Pagamento] = {}

def create_new_session(form: EditarSessaoForm, id: int) -> Sessao:
    """Cria uma nova sessão a partir do formulário"""
    return Sessao(
                    nome = form.titulo.data, 
                    classificacao=form.classificacao.data, 
                    legenda=form.legenda.data, 
                    DDD=form.DDD.data, 
                    horarios=[str(horario.data)[:5] for horario in form.horarios], 
                    id = id
                )

def get_session_from_sessions(id: int) -> Sessao:
    """Retorna uma sessão a partir do id"""
    return [sessao for sessao in sessoes if sessao.id == id][0]

def remove_empty_sessions() -> None:
    """Remove as sessões cujo nome for '-'"""
    sessoes[:] = [sessao for sessao in sessoes if sessao.nome != '-']

def create_sessions_dict() -> Dict[str, list]:
    """Cria um dicionário com as sessões, para ser usado no template"""
    sessions: Dict[str, list] = {}
    for sessao in sessoes:
        if sessao.nome not in sessions:
            sessions[sessao.nome]: list = []
            for each in [s for s in sessoes if s.nome == sessao.nome]:
                new: list = [each.generos, each.DDD, each.legenda, each.horarios, each.id, each.classificacao, each.description, each.imagem]
                sessions[sessao.nome].append(new)
    return sessions

# Rota para a página inicial
@app.route('/', methods=['GET', 'POST'])
def escolha_do_filme():
    return render_template(
        'escolha_do_filme.html', 
        title = 'Filmes', 
        filmes = [(filmes.index(filme) + 1, filme) for filme in filmes], 
        sessions = create_sessions_dict(), 
        sessoes = sessoes
    )

# Rota para a página de compra
@app.route('/poltronas/<id_sessao>/<horario>', methods=['GET', 'POST'])
def poltronas(id_sessao, horario):
    session: Sessao = get_session_from_sessions(int(id_sessao))
    ingressos: List[str] = request.form.getlist('poltronas')
    quantidade_lugares_disponiveis_sala_mais_vazia: int = most_empty([[sala.cronograma[f"{id_sessao} {horario}"] for sessao in sala.sessoes if sessao.id == int(id_sessao)] for sala in salas])
    
    sala: Sala = None
    for s in salas:
        for horario in session.horarios:
            if session in s.sessoes and lugares_disponiveis(s.cronograma[f"{session.id} {horario}"]) == quantidade_lugares_disponiveis_sala_mais_vazia:
                sala: Sala = s
                break

    poltronas: List[List[int]] = [sala.cronograma[f"{id_sessao} {horario}"][i-1][::-1] for i in range(len(sala.cronograma[f"{id_sessao} {horario}"]), 0, -1)]
    
    form: CompraForm = CompraForm()
    if form.validate_on_submit():
        if form.meias.data > len(ingressos):
            flash('Você não pode comprar mais meias do que ingressos')
        elif len(ingressos) > quantidade_lugares_disponiveis_sala_mais_vazia:
            flash('Não há lugares suficientes disponíveis')
        else:
            poltronas_a_preencher: List[str] = [letras[::-1][:len(poltronas)][int(ingressos[i].split()[0])]+[str(x+1) for x in range(len(poltronas[0]))][::-1][int(ingressos[i].split()[1])] for i in range(len(ingressos))]
            sala.preencher_poltronas(poltronas_a_preencher, id_sessao, horario)
            #flash(f'Você comprou {len(ingressos)} ingressos e {form.meias.data} meias-entradas.')
            pagamento: Pagamento = Pagamento(len(ingressos), form.meias.data, forma = form.maneira.data)
            payments[f"{pagamento.id}"]: Pagamento = pagamento
            pagamentos.append(pagamento)
            store_objects(pagamentos, 'app/storage/pagamentos.pkl')
            store_objects(salas, 'app/storage/salas.pkl')
    
            return redirect(url_for(
                'pagamento', 
                pagamento_id = pagamento.id, 
                id_sessao = id_sessao, 
                horario = horario, 
                poltronas = lista_strings_para_string([poltrona.upper() for poltrona in poltronas_a_preencher])
            ))

    return render_template(
        'poltronas.html', 
        title = 'Poltronas', 
        letras = letras[::-1][:len(poltronas)], 
        horario = horario, 
        sessao = session, 
        form = form, 
        poltronas = poltronas
    )

@app.route('/pagamentos/<pagamento_id>/<id_sessao>/<horario>/<poltronas>', methods=['GET', 'POST'])
def pagamento(pagamento_id, id_sessao, horario, poltronas):
    qrcode.make(f"Poltronas: {poltronas} Horário: {horario} ID_SESSAO: {id_sessao} ID_PAGAMENTO: {pagamento_id} Sala {[salas.index(sala) for sala in salas if int(id_sessao) in [sessao.id for sessao in sala.sessoes]][0] + 1}").save('app/static/qr.png')
    return render_template(
        'pagamentos.html', 
        title = 'Pagamentos', 
        horario = horario, 
        sessao = get_session_from_sessions(int(id_sessao)), 
        valor_total = payments[pagamento_id].valor, 
        maneira = payments[pagamento_id].forma, 
        poltronas = poltronas, 
        sala = [salas.index(sala) for sala in salas if int(id_sessao) in [sessao.id for sessao in sala.sessoes]][0]
    )

@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    form: AdminLoginForm = AdminLoginForm()
    if form.validate_on_submit() and form.password.data == "adminadmin":
        return redirect(url_for('adminMenu'))
    return render_template('adminLogin.html', title = "Admin Login", form = form)

@app.route('/adminMenu', methods=['GET', 'POST'])
def adminMenu():
    return render_template(
        'adminMenu.html', 
        title = "Admin Menu", 
        dados_faturamento = {"Valor faturado": f'R$ {sum(pagamento.valor for pagamento in pagamentos)},00', "Total de Ingressos": sum(pagamento.ingressos for pagamento in pagamentos), "Total de Ingressos Inteiros" :sum(pagamento.ingressos - pagamento.meias for pagamento in pagamentos), "Total de Meias-entradas":sum(pagamento.meias for pagamento in pagamentos)} if pagamentos != [] else None,
        salas = salas,  
        filmes = [(filmes.index(filme) + 1, filme) for filme in filmes], 
        sessions = create_sessions_dict(), 
        sessoes = sessoes
    )

@app.route('/editar_sessao/<id_sessao>', methods=['GET', 'POST'])
def editar_sessao(id_sessao):
    if id_sessao == '0':
        sessoes.append(Sessao(nome='-'))
        id_sessao = sessoes[-1].id

    s = get_session_from_sessions(int(id_sessao))
    form: EditarSessaoForm = EditarSessaoForm(
        titulo = s.nome, 
        classificacao = s.classificacao, 
        horarios = {datetime.strptime(horario, '%H:%M'): datetime.strptime(horario, '%H:%M') for horario in s.horarios}, 
        legenda = s.legenda, 
        DDD = s.DDD
    )
    if form.validate_on_submit():
        if form.cancelar.data:
            sessoes.remove(get_session_from_sessions(int(id_sessao)))
            for sessao in load_objects('app/storage/sessoes.pkl'):
                if sessao.id == int(id_sessao):
                    sessoes.append(sessao)
            remove_empty_sessions()
            store_objects(sessoes, 'app/storage/sessoes.pkl')
            return redirect(url_for('adminMenu'))
        elif form.aplicar.data:
            sessoes.remove(get_session_from_sessions(int(id_sessao)))
            sessoes.append(create_new_session(form, int(id_sessao)))
            remove_empty_sessions()
            return redirect(url_for('editar_sessao', id_sessao = id_sessao))
        elif form.confirmar.data:
            sessao_antiga = get_session_from_sessions(int(id_sessao))
            for sala in salas:
                if sessao_antiga in sala.sessoes:
                    sala.remover_sessao(sessao_antiga)
            sessoes.remove(sessao_antiga)
            sessao = create_new_session(form, int(id_sessao))
            sessoes.append(sessao)
            salas[randint(0,1)].adicionar_sessao(sessao)
            remove_empty_sessions()
            store_objects(sessoes, 'app/storage/sessoes.pkl')
            store_objects(salas, 'app/storage/salas.pkl')
            return redirect(url_for('adminMenu'))

    return render_template('editar_sessao.html', title = "Editar Sessão", form = form, sessao = get_session_from_sessions(int(id_sessao)))