import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# criando o banco de dados
connection = sqlite3.connect("Biblioteca.db")
tabela = connection.cursor()

# criando a tabela de livros
tabela.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    ano INTEGER,
    UNIQUE(titulo, autor)
)
""")           


# criando a tabela de clientes
tabela.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefone TEXT
)
""")


# criando a tabela de empréstimos
tabela.execute("""
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    livro_id INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL,
    data_devolucao TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
)
""")

# adição inicial de livros disponiveis
livros = [
    ("1984", "George Orwell", 1949),
    ("O Senhor dos Anéis", "J.R.R. Tolkien", 1954),
    ("Dom Casmurro", "Machado de Assis", 1899),
    ("Harry Potter e a Pedra Filosofal", "J.K. Rowling", 1997),
    ("Capitães da Areia", "Jorge Amado", 1937),
    ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", 1943),
    ("A Revolução dos Bichos", "George Orwell", 1945),
    ("A Metamorfose", "Franz Kafka", 1915),
    ("Cem Anos de Solidão", "Gabriel García Márquez", 1967),
    ("O Código Da Vinci", "Dan Brown", 2003),
    ("O Alquimista", "Paulo Coelho", 1988),
    ("O Hobbit", "J.R.R. Tolkien", 1937),
    ("O Nome do Vento", "Patrick Rothfuss", 2007),
    ("Jogos Vorazes", "Suzanne Collins", 2008),
    ("Ensaio sobre a Cegueira", "José Saramago", 1995),
    ("O Apanhador no Campo de Centeio", "J.D. Salinger", 1951),
    ("Orgulho e Preconceito", "Jane Austen", 1813),
    ("Drácula", "Bram Stoker", 1897),
    ("Frankenstein", "Mary Shelley", 1818),
    ("As Crônicas de Nárnia", "C.S. Lewis", 1956),
    ("O Morro dos Ventos Uivantes", "Emily Brontë", 1847),
    ("A Menina que Roubava Livros", "Markus Zusak", 2005),
    ("O Caçador de Pipas", "Khaled Hosseini", 2003),
    ("A Cabana", "William P. Young", 2007),
    ("O Silmarillion", "J.R.R. Tolkien", 1977),
    ("A Bússola de Ouro", "Philip Pullman", 1995),
    ("Eragon", "Christopher Paolini", 2002),
    ("O Senhor das Moscas", "William Golding", 1954),
    ("A Guerra dos Tronos", "George R.R. Martin", 1996),
    ("It: A Coisa", "Stephen King", 1986)
]


# adiçao inicial de clientes 
clientes = [
    ("João Silva", "joao.silva@email.com", "21 98765-4321"),
    ("Maria Oliveira", "maria.oliveira@email.com", "21 99876-5432"),
    ("Carlos Souza", "carlos.souza@email.com", "21 97654-3210"),
    ("Ana Paula", "ana.paula@email.com", "21 96543-2109"),
    ("Lucas Ferreira", "lucas.ferreira@email.com", "21 95432-1098"),
    ("Juliana Rocha", "juliana.rocha@email.com", "21 94321-0987"),
    ("Fernando Lima", "fernando.lima@email.com", "21 93210-9876"),
    ("Patrícia Gomes", "patricia.gomes@email.com", "21 92109-8765"),
    ("André Costa", "andre.costa@email.com", "21 91098-7654"),
    ("Beatriz Martins", "beatriz.martins@email.com", "21 90987-6543"),
    ("Rafael Almeida", "rafael.almeida@email.com", "21 89876-5432"),
    ("Camila Mendes", "camila.mendes@email.com", "21 88765-4321"),
    ("Eduardo Pinto", "eduardo.pinto@email.com", "21 87654-3210"),
    ("Larissa Barbosa", "larissa.barbosa@email.com", "21 86543-2109"),
    ("Tiago Moreira", "tiago.moreira@email.com", "21 85432-1098")
]


# Verifica e insere livros apenas se necessario, fazendo assim a ordem exata dos id livros 
tabela.execute("SELECT COUNT(*) FROM livros")
if tabela.fetchone()[0] == 0:
    tabela.executemany("""INSERT INTO livros (titulo, autor, ano)
        VALUES (?, ?, ?)
    """, livros)


# Verifica e insere clientes apenas se necessario, fazendo assim a ordem do id clientes
tabela.execute("SELECT COUNT(*) FROM clientes")
if tabela.fetchone()[0] == 0:
    tabela.executemany("""INSERT INTO clientes (nome, email, telefone)
        VALUES (?, ?, ?)
    """, clientes)

connection.commit()
    
class BibliotecaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DataLiB")
        self.root.geometry("1000x700")
        
        # conexao com banco de dados
        self.connection = sqlite3.connect("Biblioteca.db")  
        self.tabela = self.connection.cursor()
        
        self.criar_interface()
        
    def criar_interface(self):
        # criaçao do titulo 
       
        titulo = tk.Label(self.root, text="📚 DataLiB 📚", 
                         font=('Arial', 18, 'bold'))
        titulo.pack(pady=10)
        
        # criaçao de frame de botões principais
       
        frame_botoes = tk.Frame(self.root)  
        frame_botoes.pack(pady=10)
        
        # criaçao dos botoes principais 
       
        tk.Button(frame_botoes, text="Adicionar Livro", 
                 command=self.abrir_adicionar_livro, width=20, height=2).grid(row=0, column=0, padx=5)
        tk.Button(frame_botoes, text="Adicionar Cliente", 
                 command=self.abrir_adicionar_cliente, width=20, height=2).grid(row=0, column=1, padx=5)
        tk.Button(frame_botoes, text="Fazer Empréstimo", 
                 command=self.abrir_fazer_emprestimo, width=20, height=2).grid(row=0, column=2, padx=5)
        
        tk.Button(frame_botoes, text="Ver Livros", 
                 command=self.ver_livros, width=20, height=2).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_botoes, text="Ver Clientes", 
                 command=self.ver_clientes, width=20, height=2).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame_botoes, text="Ver Empréstimos", 
                 command=self.ver_emprestimos, width=20, height=2).grid(row=1, column=2, padx=5, pady=5)
        
        tk.Button(frame_botoes, text="Devolver Livro", 
                 command=self.abrir_devolver_livro, width=20, height=2, bg='#90EE90').grid(row=2, column=1, padx=5, pady=5)
        
        # criaçao de area de exibiçao
        
        frame_exibicao = tk.Frame(self.root)  
        frame_exibicao.pack(pady=10, padx=10, fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(frame_exibicao)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.texto_exibicao = tk.Text(frame_exibicao, height=15, width=90, 
                                       yscrollcommand=scrollbar.set, font=('Courier', 10))
        self.texto_exibicao.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=self.texto_exibicao.yview)
        
        self.mostrar_mensagem("Bem-vindo ao DataLib!\nClique nos botões acima para começar.")
    
    # area onde se exibe o texto, acionada pelas funçoes de ver_livros, ver_clientes e ver_emprestimos

    def mostrar_mensagem(self, mensagem):
        self.texto_exibicao.delete(1.0, tk.END)
        self.texto_exibicao.insert(1.0, mensagem)
       
    # criaçao da janela adicionar livro
    
    def abrir_adicionar_livro(self):
        janela = tk.Toplevel(self.root)
        janela.title("Adicionar Livro")
        janela.geometry("400x200")
        
        
        tk.Label(janela, text="Título:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        entry_titulo = tk.Entry(janela, width=30)
        entry_titulo.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(janela, text="Autor:", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        entry_autor = tk.Entry(janela, width=30)
        entry_autor.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(janela, text="Ano:", font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        entry_ano = tk.Entry(janela, width=30)
        entry_ano.grid(row=2, column=1, padx=10, pady=10)
        
        def salvar():
            titulo = entry_titulo.get().strip()
            autor = entry_autor.get().strip()
            ano = entry_ano.get().strip()
            
            if not titulo or not autor or not ano:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            try:
                ano = int(ano)
                self.tabela.execute("INSERT INTO livros (titulo, autor, ano) VALUES (?, ?, ?)", 
                                  (titulo, autor, ano))
                self.connection.commit()
                messagebox.showinfo("Sucesso", f"Livro '{titulo}' adicionado!")
                janela.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Ano deve ser um número!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Livro já cadastrado!")
        
        tk.Button(janela, text="Salvar", command=salvar, bg='#4CAF50', 
                 fg='white', width=15).grid(row=3, column=1, pady=20)
        
    # criaçao da janela adicionar clientes 
    
    def abrir_adicionar_cliente(self):
        janela = tk.Toplevel(self.root)
        janela.title("Adicionar Cliente")
        janela.geometry("400x200")
        
        tk.Label(janela, text="Nome:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        entry_nome = tk.Entry(janela, width=30)
        entry_nome.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(janela, text="Email:", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        entry_email = tk.Entry(janela, width=30)
        entry_email.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(janela, text="Telefone:", font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        entry_telefone = tk.Entry(janela, width=30)
        entry_telefone.grid(row=2, column=1, padx=10, pady=10)
        
        
        def salvar():
            nome = entry_nome.get().strip()
            email = entry_email.get().strip()
            telefone = entry_telefone.get().strip()
            
            if not nome or not email:
                messagebox.showwarning("Aviso", "Preencha nome e email!")
                return
            
            try:
                self.tabela.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", 
                                  (nome, email, telefone))
                self.connection.commit()
                messagebox.showinfo("Sucesso", f"Cliente '{nome}' adicionado!")
                janela.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Email já cadastrado!")
        
        tk.Button(janela, text="Salvar", command=salvar, bg='#4CAF50', 
                 fg='white', width=15).grid(row=3, column=1, pady=20)
    
    # criaçao da janela fazer emprestimo
    
    def abrir_fazer_emprestimo(self):
        janela = tk.Toplevel(self.root)
        janela.title("Fazer Empréstimo")
        janela.geometry("400x150")
        
        tk.Label(janela, text="ID do Cliente:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        entry_cliente = tk.Entry(janela, width=30)
        entry_cliente.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(janela, text="ID do Livro:", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        entry_livro = tk.Entry(janela, width=30)
        entry_livro.grid(row=1, column=1, padx=10, pady=10)
        
        def salvar():
            cliente_id = entry_cliente.get().strip()
            livro_id = entry_livro.get().strip()
            
            if not cliente_id or not livro_id:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            try:
                cliente_id = int(cliente_id)
                livro_id = int(livro_id)
                
                self.tabela.execute("SELECT * FROM emprestimos WHERE livro_id = ? AND data_devolucao IS NULL", (livro_id,))
                if self.tabela.fetchone():
                    messagebox.showerror("Erro", "Este livro já está emprestado!")
                    return
                
                data_emprestimo = datetime.now().strftime("%Y-%m-%d")
                self.tabela.execute("INSERT INTO emprestimos (cliente_id, livro_id, data_emprestimo) VALUES (?, ?, ?)",
                                  (cliente_id, livro_id, data_emprestimo))
                self.connection.commit()
                messagebox.showinfo("Sucesso", "Empréstimo registrado!")
                janela.destroy()
            except ValueError:
                messagebox.showerror("Erro", "IDs devem ser números!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Cliente ou livro não encontrado!")
        
        tk.Button(janela, text="Registrar", command=salvar, bg='#4CAF50', 
                 fg='white', width=15).grid(row=2, column=1, pady=20)
    
    # criaçao da janela devolver livro 
    
    def abrir_devolver_livro(self):
        janela = tk.Toplevel(self.root)
        janela.title("Devolver Livro")
        janela.geometry("400x100")
        
        tk.Label(janela, text="ID do Livro:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        entry_livro = tk.Entry(janela, width=30)
        entry_livro.grid(row=0, column=1, padx=10, pady=10)
        
        def salvar():
            livro_id = entry_livro.get().strip()
            
            if not livro_id:
                messagebox.showwarning("Aviso", "Digite o ID do livro!")
                return
            
            try:
                livro_id = int(livro_id)
                data_devolucao = datetime.now().strftime("%Y-%m-%d")
                
                self.tabela.execute("""
                    UPDATE emprestimos 
                    SET data_devolucao = ? 
                    WHERE livro_id = ? AND data_devolucao IS NULL
                """, (data_devolucao, livro_id))
                
                if self.tabela.rowcount == 0:
                    messagebox.showerror("Erro", "Nenhum empréstimo ativo para este livro!")
                else:
                    self.connection.commit()
                    messagebox.showinfo("Sucesso", "Livro devolvido!")
                    janela.destroy()
            except ValueError:
                messagebox.showerror("Erro", "ID deve ser um número!")
        
        tk.Button(janela, text="Devolver", command=salvar, bg='#4CAF50', 
                 fg='white', width=15).grid(row=1, column=1, pady=20)
    
    # funçoes dos botoes onde a sua exibiçao e na janela principal
    
    def ver_livros(self):
        self.tabela.execute("SELECT * FROM livros")
        livros = self.tabela.fetchall()
        
        texto = "LIVROS CADASTRADOS\n" + "="*80 + "\n\n"
        if not livros:
            texto += "Nenhum livro encontrado.\n"
        else:
            for livro in livros:
                texto += f"ID: {livro[0]} | {livro[1]} - {livro[2]} ({livro[3]})\n"
        
        self.mostrar_mensagem(texto)
    
    def ver_clientes(self):
        self.tabela.execute("SELECT * FROM clientes")
        clientes = self.tabela.fetchall()
        
        texto = "CLIENTES CADASTRADOS\n" + "="*80 + "\n\n"
        if not clientes:
            texto += "Nenhum cliente encontrado.\n"
        else:
            for cliente in clientes:
                telefone = cliente[3] if cliente[3] else "Não informado"
                texto += f"ID: {cliente[0]} | {cliente[1]}\n"
                texto += f"Email: {cliente[2]} | Telefone: {telefone}\n"
                texto += "-" * 80 + "\n"
        
        self.mostrar_mensagem(texto)
    
    def ver_emprestimos(self):
        self.tabela.execute("""
            SELECT e.id, c.nome, l.titulo, e.data_emprestimo, e.data_devolucao
            FROM emprestimos e
            JOIN clientes c ON e.cliente_id = c.id
            JOIN livros l ON e.livro_id = l.id
        """)
        emprestimos = self.tabela.fetchall()
        
        texto = "EMPRÉSTIMOS REGISTRADOS\n" + "="*80 + "\n\n"
        if not emprestimos:
            texto += "Nenhum empréstimo encontrado.\n"
        else:
            for emp in emprestimos:
                status = emp[4] if emp[4] else "Em aberto"
                texto += f"ID: {emp[0]} | Cliente: {emp[1]}\n"
                texto += f"Livro: {emp[2]}\n"
                texto += f"Empréstimo: {emp[3]} | Devolução: {status}\n"
                texto += "-" * 80 + "\n"
        
        self.mostrar_mensagem(texto)
    
    # funçoes de encerramento 
    def fechar(self):
        self.tabela.close()
        self.connection.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.fechar)
    root.mainloop()

if __name__ == "__main__":
    main()