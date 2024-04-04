from django.shortcuts import render
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages

def initial_population():
    print("vou pular")
    
    cursor = connection.cursor()
    
    senha = "123456"
    senha_armazenar = sha256(senha.encode()).hexdigest()
    
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email,senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "' ),"
    

def abre_index(request):
    return render(request, 'login.html')



# Create your views here.
