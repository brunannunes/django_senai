from django.shortcuts import render
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages
from django.http import HttpResponse

def initial_population():
    print("vou pular")
    
    cursor = connection.cursor()
    
    senha = "123456"
    senha_armazenar = sha256(senha.encode()).hexdigest()
    
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome,email,senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "' ),"
    insert_sql_professor = insert_sql_professor + "('Profa. Angela Merkel', 'angela.merkel@gmail.com', '" + senha_armazenar + "' ),"
    insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar + "' )"
    
    cursor.execute(insert_sql_professor)
    transaction.atomic() #seria como um commit para o insert e update
    
    #tabela Turma
    insert_sql_turma = "INSERT INTO App_Escola_turma(nome_turma,id_professor_id) VALUES"
    insert_sql_turma = insert_sql_turma + "('1o semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2o semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3o semestre - Desenvolvimento de Sistemas', 3)"
    
    cursor.execute(insert_sql_turma)
    transaction.atomic()
    
    #tabela de atividade
    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade,id_turma_id) VALUES"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos de programação', 1),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar FrameWork Django', 2),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar conceito de Gerenciamento de Projetos', 3)"
    
    cursor.execute(insert_sql_atividade)
    transaction.atomic()
    
    print("funfa")
    

def abre_index(request):
    # return render(request, 'index.html')
    dado_pesquisa = 'Obama'
    
    verifica_populado = Professor.objects.filter(nome__icontains = dado_pesquisa)
    
    if len(verifica_populado) == 0:
        print("não esta populado")
        initial_population()
    else:
        print("Achei o Obama", verifica_populado)
    
    return render(request, 'login.html')
        

def enviar_login(request):
    
    if (request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email=email).values("nome", "senha", "id")
        print("dados do professor", dados_professor)
        
        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']
            if (senha == senha_criptografada):
                #se logou corretamente, traz as turmas do professor
                #para isso estanciamos o model turmas do professor
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
                print("Turma do professor", turmas_do_professor)
                return render(request, 'Cons_Turma_Lista.html', {'usuario_logado':usuario_logado,
                                                                 'turmas_do_professor': turmas_do_professor,
                                                                 "id_logado": id_logado})
            else:
                messages.info(request, 'Usuario ou senha incorretos, Tente noamente')
                return render(request, 'login.html')
            
    messages.info(request, "Ola" + email + ",seja be, vindo! Percebmos que voce é novo aqui.Complete o seu cadastro")
    return render(request, 'cadastro.html',{'login':email})

def confirmar_cadastro(request):
    if(request.method == 'POST'):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        
        grava_professor = Professor(
            nome=nome,
            email=email,
            senha=senha_criptografada
        )
        grava_professor.save()
        
        mensagem = "Olá Professor" + nome + "seja bem vindo"
        return HttpResponse(mensagem)



# Create your views here.
