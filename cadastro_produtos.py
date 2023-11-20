# Authored by: Arthur (Tuts) Rodrigues
# GitHub: Tuts9

import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from fpdf import FPDF
import pandas as pd
import unicodedata

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class Produtos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title('Produtos do mercadinho')
        self.janela.geometry('1200x900')
        self.janela.resizable(False, True)
        self.criar_tabela()

        self.labelMain = ctk.CTkLabel(self.janela, text='Cadastro de produtos', font=('Arial', 25, 'bold'))
        self.labelMain.grid(row=0, column=1, pady=10, padx=10, columnspan=8)

        # 1 FRAME
        self.frame_cadastro = ctk.CTkFrame(self.janela, fg_color='transparent')
        self.frame_cadastro.grid(row=1, column=1, pady=10, columnspan=8)

        self.nomeProdutoEntry = ctk.CTkEntry(self.frame_cadastro, placeholder_text='Nome do produto', width=250)
        self.nomeProdutoEntry.pack(pady=(10, 0))

        self.quantProdutoEntry = ctk.CTkEntry(self.frame_cadastro, placeholder_text='Quantidade', width=250)
        self.quantProdutoEntry.pack(pady=(10,0))

        self.valorProdutoEntry = ctk.CTkEntry(self.frame_cadastro, placeholder_text='Valor do produto', width=250)
        self.valorProdutoEntry.pack(pady=(10,0))

        self.descricaoProdutoEntry = ctk.CTkEntry(self.frame_cadastro, placeholder_text='Descrição do produto', width=250)
        self.descricaoProdutoEntry.pack(pady=(10,0))

        self.bt_cadastrar = ctk.CTkButton(self.frame_cadastro, text='Cadastrar produto', command=self.cadastrar_produto)
        self.bt_cadastrar.pack(pady=(10, 0))

        self.janela.bind('<Return>', self.cadastrar_produto)

        self.bt_editar = ctk.CTkButton(self.frame_cadastro, text='Editar Produto', command=self.editar_produtos)
        self.bt_editar.pack(pady=10)

        self.bt_pesquisar = ctk.CTkButton(self.frame_cadastro, text='Pesquisar produtos', command=self.pesquisar_produto1)
        self.bt_pesquisar.pack()

        # 2 FRAME
        self.frame_main = ctk.CTkFrame(self.janela, fg_color='transparent', width=500)
        self.frame_main.grid(row=2, column=1, pady=10, padx=10)

        self.tree = ttk.Treeview(self.frame_main, columns=('ID', 'Nome', 'Quantidade', 'Valor', 'Descrição'), show='headings')

        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Quantidade', text='Quantidade')
        self.tree.heading('Valor', text='Valor')
        self.tree.heading('Descrição', text='Descrição')

        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nome', width=170, anchor='center')
        self.tree.column('Quantidade', width=90, anchor='center')
        self.tree.column('Valor', width=90, anchor='center')
        self.tree.column('Descrição', width=190, anchor='center')

        self.tree.pack(side='left', fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame_main, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.bind('<ButtonRelease-1>', self.preecher_campos)

        # FRAME 3
        self.frame_bt = ctk.CTkFrame(self.janela, fg_color='transparent')
        self.frame_bt.grid(row=3, column=1, pady=10, columnspan=8)

        self.bt_listar = ctk.CTkButton(self.frame_bt, text='Listar Produtos', command=self.listar_produtos)
        self.bt_listar.pack(side='left')

        self.bt_excluir = ctk.CTkButton(self.frame_bt, text='Excluir Produto', command=self.excluir_produto)
        self.bt_excluir.pack(side='left', padx=5)

        self.bt_salvar_pdf = ctk.CTkButton(self.frame_bt, text='Salvar PDF', command=self.criar_pdf)
        self.bt_salvar_pdf.pack(side='right')

        self.bt_excel = ctk.CTkButton(self.frame_bt, text='Exportar excel')
        self.bt_excel.pack(side='right', padx=5)

        # FRAME (GAMBIARRA; PARA CRIAR UM ESPAÇO INVISIVEL NA ESQUERDA PRA CENTRALIZAR OS OUTROS ELEMENTOS)
        self.frame_space = ctk.CTkFrame(self.janela, width=300, fg_color='transparent')
        self.frame_space.grid(row=4, column=0)

    def remover_acentos(self, texto):
        return''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

    def criar_tabela(self):
        conexao = sqlite3.connect('produtosOFC.db')
        c = conexao.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS tb_items (
                N_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                T_NOME TEXT NOT NULL,
                N_QUANTIDADE INTEGER NOT NULL,
                R_VALOR REAL NOT NULL,
                T_DESCRICAO TEXT
            )""")
        conexao.commit()
        conexao.close()

    def cadastrar_produto(self, event=None):
        nome = self.nomeProdutoEntry.get()
        quantidade = self.quantProdutoEntry.get()
        valor = self.valorProdutoEntry.get()
        descricao = self.descricaoProdutoEntry.get()

        if ',' in valor:
            messagebox.showerror('Aviso', 'Não é permitido vírgula no campo de valor!')
            self.valorProdutoEntry.delete(0, 'end')
            self.valorProdutoEntry.focus()
            return
        
        else:
            if nome and quantidade and valor:
                conexao = sqlite3.connect('produtosOFC.db')
                c = conexao.cursor()
                c.execute("SELECT T_NOME FROM tb_items")

                nomes = c.fetchall()
                nomes_sem_acento = self.remover_acentos(nome.upper())

                for nome_db in nomes:
                    nome_db_sem_acento = self.remover_acentos(nome_db[0].upper())

                    if nomes_sem_acento == nome_db_sem_acento:
                        conexao.close()
                        messagebox.showwarning('Aviso', 'Produto já cadastrado.')
                        return
                    
                c.execute("INSERT INTO tb_items (T_NOME, N_QUANTIDADE, R_VALOR, T_DESCRICAO) VALUES (?, ?, ?, ?)", 
                        (nomes_sem_acento, quantidade, valor, descricao))
                conexao.commit()
                conexao.close()

                self.listar_produtos()
                self.limpar_campos()
                
                self.nomeProdutoEntry.focus()

            else:
                messagebox.showwarning('Aviso', 'Preencha nome, quantidade e valor completamente.')

    def listar_produtos(self):
        conexao = sqlite3.connect('produtosOFC.db')
        c = conexao.cursor()
        c.execute("SELECT * FROM tb_items")
        self.rows = c.fetchall()
        conexao.close()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in self.rows:
            self.tree.insert('', 'end', values=row)

    def excluir_produto(self):
        selected_item = self.tree.selection()

        if selected_item:

            if messagebox.askyesno('Aviso', 'Deseja realmente excluir o produto selecionado?'):
                conexao = sqlite3.connect('produtosOFC.db')
                c = conexao.cursor()

                for item in selected_item:
                    c.execute("DELETE FROM tb_items WHERE N_ID=?", (self.tree.item(item, 'values')[0],))

                conexao.commit()
                conexao.close()

                self.listar_produtos()
                self.nomeProdutoEntry.focus()

        else:
            messagebox.showwarning('Aviso', 'Selecione um produto para excluir.')
    
    def editar_produtos(self):
        selected_item = self.tree.selection()

        if selected_item:

            if messagebox.askyesno('Aviso', 'Deseja realmente alterar o produto selecionado?'):
                produto_id = self.tree.item(selected_item, 'values')[0]

                nome = self.remover_acentos(self.nomeProdutoEntry.get())
                quantidade = self.quantProdutoEntry.get()
                valor = self.valorProdutoEntry.get()
                descricao = self.descricaoProdutoEntry.get()

                if ',' in valor:
                    messagebox.showerror('Erro', 'Não é permitido vírgula no campo de valor')
                    self.valorProdutoEntry.delete(0, 'end')
                    self.valorProdutoEntry.focus()
                    return
                
                elif nome and quantidade and valor:
                    conexao = sqlite3.connect('produtosOFC.db')
                    c = conexao.cursor()
                    c.execute("UPDATE tb_items SET T_NOME=?, N_QUANTIDADE=?, R_VALOR=?, T_DESCRICAO=? WHERE N_ID=?", (nome, quantidade, valor, descricao, produto_id))

                    conexao.commit()
                    conexao.close()

                    self.limpar_campos()
                    self.listar_produtos()

                else:
                    messagebox.showwarning('Aviso', 'Preencha todos os campos completamente.')
        
        else:
            messagebox.showinfo('Aviso', 'Selecione um produto para editar.')

    def preecher_campos(self, event):
        selected_item = self.tree.selection()

        if selected_item:
            values = self.tree.item(selected_item, 'values')

            self.nomeProdutoEntry.delete(0, 'end')
            self.quantProdutoEntry.delete(0, 'end')
            self.valorProdutoEntry.delete(0, 'end')
            self.descricaoProdutoEntry.delete(0, 'end')

            self.nomeProdutoEntry.insert(0, values[1])
            self.quantProdutoEntry.insert(0, values[2])
            self.valorProdutoEntry.insert(0, values[3])
            self.descricaoProdutoEntry.insert(0, values[4])

    def pesquisar_produto1(self):
        
        self.nomeProdutoEntry.forget()
        self.quantProdutoEntry.forget()
        self.valorProdutoEntry.forget()
        self.descricaoProdutoEntry.forget()
        self.bt_cadastrar.forget()
        self.bt_editar.forget()
        self.bt_pesquisar.forget()

        self.pesquisa_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text='Pesquisar...')
        self.pesquisa_entry.pack(pady=(0,10))

        self.bt_pesquisar = ctk.CTkButton(self.frame_cadastro, text='Pesquisar', command=self.pesquisar_produto2)
        self.bt_pesquisar.pack()

    def pesquisar_produto2(self):

        termo_pesquisa = self.remover_acentos(self.pesquisa_entry.get().upper())

        if termo_pesquisa:

            conexao = sqlite3.connect('produtosOFC.db')
            c = conexao.cursor()
            c.execute("SELECT * FROM tb_items")
            rows = c.fetchall()
            conexao.close()

            resultados = []

            for row in rows:
                nome_produto = row[1].upper()

                if termo_pesquisa in nome_produto:
                    resultados.append(row)

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in resultados:
                self.tree.insert('', 'end', values=row)

            self.pesquisa_entry.forget()
            self.bt_pesquisar.forget()

            self.nomeProdutoEntry.pack()
            self.quantProdutoEntry.pack(pady=10)
            self.valorProdutoEntry.pack(pady=(0,10))
            self.descricaoProdutoEntry.pack()
            self.bt_cadastrar.pack(pady=(10,0))
            self.bt_editar.pack(pady=10)

            self.bt_pesquisar = ctk.CTkButton(self.frame_cadastro, text='Pesquisar produtos', command=self.pesquisar_produto1)
            self.bt_pesquisar.pack()

            if not resultados:
                messagebox.showinfo('Aviso', 'Este produto não está na lista.')

        else:
            messagebox.showerror('Aviso', 'Digite algum nome para ser pesquisado.')

    def criar_pdf(self):
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(190, 10, 'Lista de Produtos', align='C', ln=True)
                self.set_fill_color(255,0,255)
                self.cell(20, 10, 'ID', border=1, align='C', fill=True)
                self.cell(50, 10, 'Nome', border=1, align='C', fill=True)
                self.cell(30, 10, 'Quantidade', border=1, align='C', fill=True)
                self.cell(30, 10, 'Valor', border=1, align='C', fill=True)
                self.cell(40, 10, 'Descrição', border=1, align='C', fill=True)
                self.ln(10.0)

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

        pdf = PDF()
        pdf.add_page()

        conexao = sqlite3.connect('produtosOFC.db')
        c = conexao.cursor()
        c.execute("SELECT * FROM tb_items")
        rows = c.fetchall()
        conexao.close()

        pdf.set_fill_color(255, 255, 255)

        for row in rows:
            pdf.cell(20, 10, str(row[0]), border=1)
            pdf.cell(50, 10, row[1], border=1)
            pdf.cell(30, 10, str(row[2]), border=1)
            pdf.cell(30, 10, 'R$ %.2f' % row[3], border=1)
            pdf.multi_cell(40, 10, str(row[0]), border=1)
            pdf.ln(0)

        pdf_file = 'lista_produtosOFC.pdf'
        pdf.output(pdf_file)

        messagebox.showinfo('Aviso', f'Lista de produtos salva em {pdf_file}')

    def criar_excel(self):
        conexao = sqlite3.connect('produtosOFC.db')
        c = conexao.cursor()
        c.execute("SELECT * FROM tb_produtos")
        produtos_cadastrados = c.fetchall()
        produtos_cadastrados = pd.DataFrame(produtos_cadastrados, columns=['ID', 'Nome', 'Quantidade', 'Valor', 'Descrição'])
        produtos_cadastrados.to_excel('base_produtos.xlsx')
        conexao.commit()
        conexao.close()

    def limpar_campos(self):
        self.nomeProdutoEntry.delete(0, 'end')
        self.quantProdutoEntry.delete(0, 'end')
        self.valorProdutoEntry.delete(0, 'end')
        self.descricaoProdutoEntry.delete(0, 'end')

    def iniciarInterface(self):
        self.janela.mainloop()

if __name__ == '__main__':
    janela = ctk.CTk()
    merc = Produtos(janela)
    merc.iniciarInterface()
