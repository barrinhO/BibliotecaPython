import os
import time
import hashlib
import json

FILE_NAME = "users.json"

print("Use 'y' para aceitar e 'n' para negar")

def clear_console():
    os.system("cls" if os.name in ("nt", "dos") else "clear")

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def carregar_usuarios():
    return json.load(open(FILE_NAME)) if os.path.exists(FILE_NAME) else {}

def salvar_usuarios(usuarios):
    json.dump(usuarios, open(FILE_NAME, "w"), indent=4)

lista_de_livros = [
    "Técnicas de Comunicação Escrita",
    "Programador Autodidata",
    "Técnicas de Invasão",
    "Estruturas de Dados e Algoritmos em Python",
    "Clean Code: Código Limpo",
    "Engenharia de Software Moderna",
    "Machine Learning Prático",
    "Desenvolvimento Web com JavaScript e Node.js",
    "Banco de Dados SQL para Desenvolvedores",
    "Computação em Nuvem: Conceitos e Práticas",
]


usuario_logado = None

def tem_cadastro():
    cadastro_sn = input("Você possui cadastro? ").strip().lower()
    clear_console()
    
    if cadastro_sn == "n":
        nao_possui_cadastro()
    elif cadastro_sn == "y":
        possui_cadastro()
    else:
        print("Entrada inválida! Digite 'y' para sim ou 'n' para não.")
        time.sleep(2)
        clear_console()
        tem_cadastro()

def possui_cadastro():
    global usuario_logado
    usuarios = carregar_usuarios()
    user_login = input("Digite seu nome de usuário: ").strip().lower()
    user_senha = input("Digite sua senha de 4 dígitos: ").strip()
    
    if user_login in usuarios and usuarios[user_login]["senha"] == hash_senha(user_senha):
        usuario_logado = user_login
        print("Login bem-sucedido! Bem-vindo,", user_login)
        time.sleep(2)
        clear_console()
        pagina_inicial()
    else:
        print("Usuário ou senha incorretos!")
        time.sleep(2)
        clear_console()
    
    escolha = input("Se deseja tentar novamente, aperte 'y'. Se quer fazer um novo cadastro, aperte 'n': ")
    
    if(escolha == "y"):
        clear_console()
        possui_cadastro()
    elif escolha == "n":
        clear_console()
        nao_possui_cadastro()
    else:
        return escolha
    

def nao_possui_cadastro():
    usuarios = carregar_usuarios()
    create_user = input("Crie seu nome de usuário: ").strip().lower()
    create_password = input("Crie uma senha com 4 dígitos: ").strip()
    
    if create_user in usuarios:
        print("Erro: Usuário já existe!")
        time.sleep(2)
        clear_console()
        return nao_possui_cadastro()
    
    usuarios[create_user] = {
        "senha": hash_senha(create_password),
        "livros_emprestados": []
    }
    clear_console()
    salvar_usuarios(usuarios)
    print("Conta criada com sucesso!")
    possui_cadastro()

def livros_disponiveis():
    usuarios = carregar_usuarios()
    livros_emprestados = {livro for user in usuarios.values() for livro in user["livros_emprestados"]}
    return [livro for livro in lista_de_livros if livro not in livros_emprestados]

def selecionar_livro():
    global usuario_logado
    usuarios = carregar_usuarios()
    livros_disp = livros_disponiveis()
    
    if not livros_disp:
        print("Nenhum livro disponível.")
        time.sleep(2)
        clear_console()
        return pagina_inicial()
    
    print("\n".join(f"{i + 1}. {livro}" for i, livro in enumerate(livros_disp)))
    escolha = input("Digite o número do livro para obtê-lo ou qualquer outra tecla para voltar: ").strip()
    clear_console()

    if escolha.lower() == "b":
        return pagina_inicial()
    
    if escolha.isdigit() and 1 <= int(escolha) <= len(livros_disp):
        livro_escolhido = livros_disp[int(escolha) - 1]
        usuarios[usuario_logado]["livros_emprestados"].append(livro_escolhido)
        salvar_usuarios(usuarios)

        print(f"Livro '{livro_escolhido}' emprestado com sucesso!")
        time.sleep(2)
        clear_console()

    pagina_inicial()

def devolver_livros():
    global usuario_logado
    usuarios = carregar_usuarios()
    livros_emprestados = usuarios[usuario_logado]["livros_emprestados"]

    if not livros_emprestados:
        print("Nenhum livro para devolver.")
        time.sleep(2)
        clear_console()
        return pagina_inicial()

    print("\n".join(f"{i + 1}. {livro}" for i, livro in enumerate(livros_emprestados)))
    escolha = input("Digite o número do livro para devolver ou 'b' para voltar: ").strip()
    clear_console()

    if escolha.lower() == "b":
        return pagina_inicial()

    if escolha.isdigit() and 1 <= int(escolha) <= len(livros_emprestados):
        livro_escolhido = livros_emprestados.pop(int(escolha) - 1)
        usuarios[usuario_logado]["livros_emprestados"] = livros_emprestados
        salvar_usuarios(usuarios)

        print(f"Livro '{livro_escolhido}' devolvido com sucesso!")
        time.sleep(2)
        clear_console()

    pagina_inicial()

def pagina_inicial():
    global usuario_logado
    usuarios = carregar_usuarios()
    livros_usuario = usuarios[usuario_logado]["livros_emprestados"]

    print("Bem-vindo à Biblioteca Virtual Poggers!")
    print("1. Escolher Livro")
    print("2. Meus Livros")
    print("3. Devolver Livro")
    print("4. Sair")

    escolha = input("Escolha uma opção: ").strip()
    clear_console()

    if escolha == "1":
        selecionar_livro()
    elif escolha == "2":
        print("\n".join(f"- {livro}" for livro in livros_usuario) if livros_usuario else "Não há livros.")
        input("Pressione qualquer tecla para voltar: ")
        clear_console()
    elif escolha == "3":
        devolver_livros()
    elif escolha == "4":
        print("Saindo...")
        time.sleep(2)
        print("Até logo!")
        exit()
    else:
        print("Opção inválida!")

    pagina_inicial()

tem_cadastro()