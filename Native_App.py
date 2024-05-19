import sqlite3
import tkinter as tk
import customtkinter as ctk

from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showinfo
from datetime import datetime, timedelta
from tkinter.simpledialog import askstring


class InterfaceGrafica:
    def __init__(self, janela, db_file='frota.db'):
        self.janela = janela
        self.janela.title("Gestão de Frota")
        self.janela.resizable(1, 1)

        self.db_file = db_file

        self.tabela = self.configura_tabela()

        self.mensagem = tk.Label(text='', fg='red')
        self.mensagem.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)

        # Botoões da parte de cima, "Disponível" e "Indisponivel"
        btn_listar_veiculos_disponiveis = ctk.CTkButton(
            self.janela, text="Disponíveis", command=lambda: self.get_veiculos_disp(1))
        btn_listar_veiculos_disponiveis.grid(row=1, column=0, columnspan=3)

        btn_listar_veiculos_indisponiveis = ctk.CTkButton(self.janela, text="Indisponíveis",command=lambda: self.get_veiculos_disp(0))
        btn_listar_veiculos_indisponiveis.grid(row=2, column=0, columnspan=3)

        btn_editar_vhc = ctk.CTkButton(self.janela, text='Editar VHC', command=self.modif_vhc)
        btn_editar_vhc.grid(row=3, column=0, columnspan=3)


        # Botões do Rodapé
        frame_rodape = ctk.CTkFrame(self.janela)
        frame_rodape.grid(row=10, column=0, columnspan=2, pady=10, sticky=tk.W)

        # Botões do Rodapé
        btn_revisao = ctk.CTkButton(
            frame_rodape, text='Manutenção'.upper(), command=self.revisao)
        btn_revisao.grid(row=0, column=0, padx=5, pady=5)

        btn_legalizar = ctk.CTkButton(
            frame_rodape, text='ESTADO LEGAL', command=self.estado_legal)
        btn_legalizar.grid(row=0, column=1, padx=5, pady=5)

        btn_auxiliar = ctk.CTkButton(
            frame_rodape, text='TIRAR DA MANUTENÇÃO', command=self.func_btn_auxiliar)
        btn_auxiliar.grid(row=0, column=2, padx=5, pady=5)

        btn_teste_compra_veiculos = ctk.CTkButton(frame_rodape, text='COMPRAR VHC', command=self.adicionar_veiculo)
        btn_teste_compra_veiculos.grid(row=0, column=3, padx=5, pady=5)



    def configura_tabela(self):
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        tabela = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        tabela.grid(row=5, column=0, columnspan=2)
        tabela.heading('#0', text='Modelo', anchor=tk.CENTER)
        tabela.heading('#1', text='Categoria', anchor=tk.CENTER)

        return tabela

    def _connect(self):
        return sqlite3.connect(self.db_file)

    def db_consulta(self, consulta, parametros=()):
        with self._connect() as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_veiculos(self, disponivel):
        query = f'SELECT MODELO, UPPER(Categoria) FROM Veiculos WHERE Disponivel = {disponivel}'
        registros = self.db_consulta(query)
        return registros


    def modif_vhc_nome(self):
        janela_adicionar = tk.Toplevel(self.janela)
        janela_adicionar.title("NOVO NOME/MODELO")

        largura = 330
        altura = 85

        largura_tela = janela_adicionar.winfo_screenwidth()
        altura_tela = janela_adicionar.winfo_screenheight()

        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        janela_adicionar.geometry(f"{largura}x{altura}+{x}+{y}")

        lbl_novo_nome = ctk.CTkLabel(janela_adicionar, text="Insira o novo\nnome/modelo do veículo", font=('Arial', 15))
        lbl_novo_nome.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        entry_novo_nome = ctk.CTkEntry(janela_adicionar)
        entry_novo_nome.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        btn_salvar = ctk.CTkButton(janela_adicionar, text="Alterar")
        btn_salvar.grid(row=1, column=0, columnspan=2, pady=10)

    def modif_vhc(self):
        try:
            selecionado = self.tabela.selection()
            if not selecionado:
                messagebox.showinfo("Aviso", "Selecione um veículo na tabela")
                return

            nome_veiculo = self.tabela.item(selecionado, 'text')

            query = "SELECT * FROM Veiculos WHERE Modelo = ?"
            cursor = self.db_consulta(query, (nome_veiculo,))
            detalhes_veiculo = cursor.fetchone()

            if not detalhes_veiculo:
                messagebox.showinfo("Aviso", f"Não foi possível encontrar detalhes para o veículo {nome_veiculo}.")
                return

            janela_modificacao = tk.Toplevel(self.janela)
            janela_modificacao.title(f"{nome_veiculo}")
            largura= 200
            altura=200

            largura_tela = janela_modificacao.winfo_screenwidth()
            altura_tela = janela_modificacao.winfo_screenheight()

            x = (largura_tela - largura) // 2
            y = (altura_tela - altura) // 2

            janela_modificacao.geometry(f"{largura}x{altura}+{x}+{y}")

            lbl_popup = ctk.CTkLabel(janela_modificacao,text=f"O QUE QUER MODIFICAR\n EM {nome_veiculo}?",  font=('Arial', 13.5))
            lbl_popup.grid(row=0, column=0)

            btn_nome = ctk.CTkButton(janela_modificacao, text='Nome'.upper(), command=self.modif_vhc_nome)
            btn_nome.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

            btn_revisao = ctk.CTkButton(janela_modificacao, text='Manutenção'.upper())
            btn_revisao.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

            btn_legalizacao = ctk.CTkButton(janela_modificacao, text='Legalização'.upper())
            btn_legalizacao.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

            btn_categoria = ctk.CTkButton(janela_modificacao, text='Categoria'.upper())
            btn_categoria.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)


        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir a janela de modificação: {str(e)}")



    def adicionar_veiculo(self):
        # Criar uma nova janela sobreposta
        janela_adicionar = tk.Toplevel(self.janela)
        janela_adicionar.title("Adicionar Veículo")

        largura = 330
        altura = 250

        largura_tela = janela_adicionar.winfo_screenwidth()
        altura_tela = janela_adicionar.winfo_screenheight()

        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        janela_adicionar.geometry(f"{largura}x{altura}+{x}+{y}")



        # Campo Modelo
        lbl_modelo = ctk.CTkLabel(janela_adicionar, text="Modelo:", font=('Arial', 15))
        lbl_modelo.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        entry_modelo = ctk.CTkEntry(janela_adicionar)
        entry_modelo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        # Campo Tipo
        lbl_tipo = ctk.CTkLabel(janela_adicionar, text="Tipo: ", font=('Arial', 15))
        lbl_tipo.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        opcoes_tipo = ["CARRO", "MOTO"]
        tipo_selecionado = tk.StringVar(janela_adicionar)
        tipo_selecionado.set(opcoes_tipo[1])

        option_menu_tipo = ttk.OptionMenu(janela_adicionar, tipo_selecionado, *opcoes_tipo)
        option_menu_tipo.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)


        # Adicionar campo para a data de revisão
        lbl_data_revisao = ctk.CTkLabel(janela_adicionar, text="Data de Revisão\n(Dia/Mes/Ano):", font=('Arial', 15))
        lbl_data_revisao.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        entry_data_revisao = ctk.CTkEntry(janela_adicionar)
        entry_data_revisao.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        # Adicionar campo para a categoria
        lbl_categoria = ctk.CTkLabel(janela_adicionar, text="Categoria:", font=('Arial', 15))
        lbl_categoria.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        # Opções para o OptionMenu
        opcoes_categoria = ["GOLD", "PRATA", "ECONOMIC"]
        categoria_selecionada = tk.StringVar(janela_adicionar)
        categoria_selecionada.set(opcoes_categoria[1])  # Definir a opção padrão

        # Criar o OptionMenu
        option_menu_categoria = ttk.OptionMenu(janela_adicionar, categoria_selecionada, *opcoes_categoria)
        option_menu_categoria.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        # Criar data Legalização
        lbl_data_legalizacao = ctk.CTkLabel(janela_adicionar, text="Data da Legalização\n(Dia/Mes/Ano):",
                                         font=('Arial', 15))
        lbl_data_legalizacao.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        entry_data_legalizacao = ctk.CTkEntry(janela_adicionar)
        entry_data_legalizacao.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        # Criando o botão
        btn_salvar = ctk.CTkButton(janela_adicionar, text="Salvar", command=lambda: self.salvar_veiculo(
            entry_modelo.get(), entry_data_revisao.get(), tipo_selecionado.get(),
            categoria_selecionada.get(), entry_data_legalizacao.get(), janela_adicionar
        ))
        btn_salvar.grid(row=5, column=0, columnspan=2, pady=10)

    def salvar_veiculo(self, modelo, data_revisao, tipo, categoria, data_legalizacao, janela_adicionar):
        try:
            # Validar os campos antes de salvar no banco de dados
            if not modelo or not data_revisao or not tipo or not categoria or not data_legalizacao:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            # Converter a data de revisão para o formato desejado (por exemplo, "%Y/%m/%d") nessa parte tive um erro pois estava causando conufsoa por ser datetime...
            data_revisao_formatada = datetime.strptime(data_revisao, "%d/%m/%Y").date()
            data_legalizacao_formatada = datetime.strptime(data_legalizacao, "%d/%m/%Y").date()

            # Adicionar o veículo ao banco de dados
            query = "INSERT INTO Veiculos (Modelo, Tipo, Categoria, Disponivel, DataUltimaRevisao, DataProximaRevisao, DataUltimaLegalizacao, DataProximaLegalizacao) VALUES (?,?, ?, ?, ?, ?, ?, ?)"
            self.db_consulta(query, (
                modelo, tipo, categoria, 1, data_revisao_formatada,
                data_revisao_formatada + timedelta(days=30), data_legalizacao_formatada,
                data_legalizacao_formatada + timedelta(days=275)
            ))

            # Fechar a janela de adicionar veículo
            janela_adicionar.destroy()

            # Mostrar a tabela
            messagebox.showinfo("Sucesso", "Veículo adicionado com sucesso.")
            self.get_veiculos_disp(1)



        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar veículo:\n{str(e)}")


    def aviso_estoque_baixo(self):
        try:
            registros_tabela = self.tabela.get_children()
            quantidade_item = len(registros_tabela)

            if quantidade_item <= 1 or quantidade_item == 0:
                messagebox.showerror("Estoque Baixíssimo",
                                     f"Nosso estoque tinha apenas {quantidade_item} veículos disponíveis;\nnos restam 0")
                resposta = messagebox.askquestion(title="Estoque Baixíssimo", message='Deseja comprar mais veículos?')
                if resposta == 'yes':
                    self.adicionar_veiculo()
                    return  # Adicionando return para encerrar a função após comprar mais veículos
                else:
                    resposta_transferir = messagebox.askquestion(title="Transferir para Tabela",
                                                                 message="Para qual tabela quer transferir: \n\nDisponível(Yes) ou Indisponível(No)?")
                    if resposta_transferir == 'yes':
                        disponibilidade = 1
                    elif resposta_transferir == 'no':
                        disponibilidade = 0
                    else:
                        messagebox.showinfo("Aviso", "Escolha inválida.")
                        return
                    self.get_veiculos_disp(disponibilidade)
                    messagebox.showinfo(f"Veículos {'Disponíveis' if disponibilidade else 'Indisponíveis'}",
                                        f"Estes são os veículos {'disponíveis' if disponibilidade else 'indisponíveis'}")

            elif quantidade_item <= 3:
                    messagebox.showerror("Estoque Em Nível Crítico",
                                         f"Nosso estoque tem apenas {quantidade_item} veículos disponíveis")

            elif quantidade_item == 5:
                    messagebox.showwarning(title=f"Estoque Baixo",
                                           message=f'O estoque está baixando, restam apenas {quantidade_item} veículos')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar aviso de estoque baixo: {str(e)}")

    def aviso_estoque_baixo_em_revisao(self):
        registros_tabela = self.tabela.get_children()
        quantidade_item = len(registros_tabela)

        try:
            if quantidade_item <= 5:
                messagebox.showwarning(title="Estoque Baixo",
                                       message=f'Estamos trabalhando à todo vapor, só temos {quantidade_item} veiculos na revisão')

        except sqlite3.Error as e:
            print(f'Erro no banco de dados: {e}')

    def get_veiculos_disp(self, disponivel):
        registros_tabela = self.tabela.get_children()
        for linha in registros_tabela:
            self.tabela.delete(linha)

        registros = self.get_veiculos(disponivel)

        for linha in registros:
            self.tabela.insert('', 0, text=linha[0], values=linha[1])

        self.aviso_estoque_baixo()
        # self.verificar_manutencao(registros_tabela)

    # Função destinada ao Botão Manutenção, no Rodapé
    def revisao(self):
        self.mensagem['text'] = ''

        try:
            nome = self.tabela.item(self.tabela.selection())['text']
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um veículo'
            return

        self.mensagem['text'] = ''
        data_ultima_revisao = datetime.now().date()
        data_proxima_revisao = (datetime.now() + timedelta(days=30)).date()

        # Atualiza o veículo para a manutenção e define as datas de revisão
        query = "UPDATE Veiculos SET Disponivel = 0, DataUltimaRevisao = ?, DataProximaRevisao = ? WHERE Modelo = ?"
        self.db_consulta(query, (data_ultima_revisao, data_proxima_revisao, nome))

        # # Chamando a função para realizar a manutenção
        # self.realizar_manutencao(nome)

        showinfo("Operação realizada com sucesso", f"O veículo {nome} foi marcado para revisão com êxito")

        self.aviso_estoque_baixo()
        # Atualizar a tabela com os veiculos disponiveis
        self.get_veiculos_disp(1)

    def verificar_manutencao(self, id_veiculo):
        con = self._connect()
        cursor = con.cursor()
        data_atual = datetime.now().date()
        cursor.execute('''
        SELECT DataProximaRevisao
        FROM Veiculos
        WHERE ID = ?
        ''', (id_veiculo,))
        data_proxima_revisao = cursor.fetchone()[0]

        if data_proxima_revisao and data_atual > data_proxima_revisao:
            return True
        else:
            return False

    def realizar_manutencao(self, id_veiculo):
        con = self._connect()
        cursor = con.cursor()
        cursor.execute('''
            UPDATE Veiculos
            SET DataUltimaRevisao = ?,
                DataProximaRevisao = ?
            WHERE ID = ?
        ''', (datetime.now().date(), datetime.now().date() + timedelta(days=30), id_veiculo))
        con.commit()
        con.close()

    def manutencao_veiculo(self):
        self.mensagem['text'] = ''

        try:
            id_veiculo = int(self.tabela.item(self.tabela.selection())['text'])
            print(id_veiculo)
        except (IndexError, ValueError) as e:
            self.mensagem['text'] = 'Por favor, selecione um veículo válido'
            print(f'O erro é: {e}')
            return

        self.mensagem['text'] = ''

        if self.verificar_manutencao(id_veiculo):
            self.mensagem['text'] = 'Este veículo já está em manutenção'
        else:
            self.realizar_manutencao(id_veiculo)
            self.mensagem['text'] = f'Manutenção realizada com sucesso para o veículo {id_veiculo}'

    def legalizar_veiculo_db(self, nome_veiculo):
        try:
            data_ultima_legalizacao = datetime.now().date()
            data_proxima_legalizacao = (datetime.now() + timedelta(days=365)).date()

            query = "UPDATE Veiculos SET Disponivel = 0, DataUltimaLegalizacao = ?, DataProximaLegalizacao = ? WHERE Modelo = ?"
            self.db_consulta(query, (data_ultima_legalizacao, data_proxima_legalizacao, nome_veiculo))

            messagebox.showinfo("Sucesso", f"O veículo {nome_veiculo} foi legalizado com sucesso!")

            self.get_veiculos_disp(1)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao legalizar veículo: {str(e)}")


    def converter_para_datetime(self, data_str):
        formatos_data = ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]

        for formato in formatos_data:
            try:
                # Tente converter a string para um objeto datetime
                return datetime.strptime(data_str, formato)
            except ValueError:
                pass

        return None

    def verificar_proxima_legalizacao(self, nome_veiculo):
        try:
            query = "SELECT DataUltimaLegalizacao, DataProximaLegalizacao FROM Veiculos WHERE Modelo = ?"
            cursor = self.db_consulta(query, (nome_veiculo,))
            result = cursor.fetchone()

            cursor.close()

            if not result:
                messagebox.showinfo("Aviso",
                                    f"Não foi possível encontrar informações de legalização para o veículo {nome_veiculo}")
                return

            # Converter as strings de data para objetos datetime
            data_ultima_legalizacao = self.converter_para_datetime(result[0])
            data_proxima_legalizacao = self.converter_para_datetime(result[1])

            if data_ultima_legalizacao is None or data_proxima_legalizacao is None:
                messagebox.showerror("Erro", f"Erro ao converter datas: {result[0]}, {result[1]}")
                return

            diferenca = data_proxima_legalizacao - data_ultima_legalizacao
            days_legal = diferenca.days

            limite_alerta_1 = timedelta(days=30)
            limite_alerta_2 = timedelta(days=15)
            limite_alerta_3 = timedelta(days=5)

            if diferenca <= limite_alerta_3:
                while True:
                    messagebox.showerror("Data Limite", f"Data Limite para legalizar o veiculo {nome_veiculo}, apenas {days_legal} para o mesmo")
                    self.resposta = messagebox.askyesno(title="Legalizacao", message=f'O veículo {nome_veiculo} está muito perto da data de legalização, restam {days_legal} dias\n\nDeseja colocar o veículo para legalizar?')

                    if self.resposta:
                        self.legalizar_veiculo_db(nome_veiculo)
                        break
                    else:
                        messagebox.showwarning('Aviso', f'Conduzir com um veículo não legalizado é passível de apreensão, favor legalizar, restam {days_legal} dias')
                        self.resposta = messagebox.askyesno(title="Legalizacao", message=f'Veículo {nome_veiculo} perto da data de legalização\n\nDeseja colocar o veículo para legalizar?')

                        if self.resposta:
                            self.legalizar_veiculo_db(nome_veiculo)
                            break

            elif diferenca <= limite_alerta_2:
                messagebox.showwarning("Alerta", f"O veículo {nome_veiculo} está à '{days_legal}' dias próximo da data de legalização!, ter atenção às datas")
                self.resposta = messagebox.askyesno(title="Legalizacao", message=f'Veículo {nome_veiculo} perto da data de legalização, restam {days_legal} dias;\nDeseja colocar o veículo para legalizar?')
                if self.resposta:
                    self.legalizar_veiculo_db(nome_veiculo)
                else:
                    showinfo('Aviso', f'Conduzir com um veículo não legalizado é passivel de apreensão, favor legalizar\nTer atenção às datas, restam apenas {days_legal} dias para legalizar o veículo')
                    self.get_veiculos_disp(0)

            # else:
            #     messagebox.showinfo("Informação", f"O veículo {nome_veiculo} está regular")

            elif diferenca <= limite_alerta_1:
                messagebox.showwarning("Alerta", f"O veículo {nome_veiculo} está próximo da data de legalização!")
                self.resposta = messagebox.askyesno(title="Legalizacao", message=f'Veículo {nome_veiculo} à {days_legal} dias perto da data de legalização\nDeseja colocar o veículo para manutenção?')
                if self.resposta:
                    self.legalizar_veiculo_db(nome_veiculo)
                else:
                    showinfo('Aviso', f'Conduzir com um veículo não legalizado é passivel de apreensão, faltam {days_legal} dias para legalização, favor legalizar')
                    self.get_veiculos_disp(0)

            else:
                messagebox.showinfo("Informação", f"O veículo {nome_veiculo} está regular")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar próxima legalização: {str(e)}")

    def estado_legal(self):
        try:
            selecionado = self.tabela.selection()
            if not selecionado:
                messagebox.showinfo("Aviso", "Selecione um veículo na tabela.")

            nome_veiculo = self.tabela.item(selecionado, 'text')

            self.verificar_proxima_legalizacao(nome_veiculo)

        except Exception as e:
            messagebox.showerror("Erro", "Ocorreu um erro ao validar o estado legal")

    def func_btn_auxiliar(self):
        self.mensagem['text'] = ''

        try:
            nome = self.tabela.item(self.tabela.selection())['text']
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um veículo'
            return

        query = "UPDATE Veiculos SET Disponivel = 1 WHERE Modelo = ?"
        self.db_consulta(query, (nome,))
        showinfo('Operação Concluída', f'Veículo {nome} devolvido à lista dos disponíveis com sucesso')

        self.aviso_estoque_baixo_em_revisao()
        self.get_veiculos_disp(0)


# Criação da janela
janela = tk.Tk()

largura_janela = 620  # substitua pelo tamanho desejado
altura_janela = 570  # substitua pelo tamanho desejado

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

x = (largura_tela - largura_janela) // 2
y = (altura_tela - altura_janela) // 2

janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")


# Inicialização da classe
app = InterfaceGrafica(janela)

# Inicia a interface gráfica
janela.mainloop()

