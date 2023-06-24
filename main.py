from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "cadastro_podutos"
)

def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    numero_id = valor_id

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_5.setText(str(produto[0][3]))
    tela_editar.lineEdit_4.setText(str(produto[0][4]))


def salvar_dados_editados():
    # pegar o numero do id
    global numero_id
    #valor digitado no lineEdit
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_5.text()
    categoria = tela_editar.lineEdit_4.text()
    # Atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute(f"UPDATE produtos SET codigo = '{codigo}', descricao = '{descricao}', preco = '{preco}', categoria = '{categoria}' WHERE id = {numero_id}")
    # atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    lista2()






def limpar_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))
    



def gera_pdf():
    cursor = banco.cursor()
    comandoSQL = "SELECT * FROM produtos"
    cursor.execute(comandoSQL)
    dados_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos Cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CODIGO")
    pdf.drawString(210, 750, "PRODUTOS")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("PFD FOI GERADO COM SUCESSO!!")



def funcao_principal():
    l1 = untitled.lineEdit.text()
    l2 = untitled.lineEdit_2.text()
    l3 = untitled.lineEdit_3.text()
    
    categoria = ""

    if untitled.radioButton.isChecked():
        print("Categoria: Eletronicos.")
        categoria = "Eletronico"

    elif untitled.radioButton_2.isChecked():
        print("Categoria: Roupas.")
        categoria = "Roupas"

    else:
        print("Categoria: Alimentos.")
        categoria = "Alimento"

    print("Codigo: ", l1)
    print("Descrição: ", l2)
    print("Preço: ", l3)
    cursor = banco.cursor()
    comandoSQL = "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (%s, %s, %s, %s)"
    dados = (str(l1), str(l2), str(l3), categoria)
    cursor.execute(comandoSQL, dados)
    banco.commit()
    untitled.lineEdit.setText("")
    untitled.lineEdit_2.setText("")
    untitled.lineEdit_3.setText("")




def lista2():
    segunda_tela.show()

    cursor = banco.cursor()
    comandoSQL = "SELECT * FROM produtos"
    cursor.execute(comandoSQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))




app = QtWidgets.QApplication([])
untitled = uic.loadUi("untitled.ui")
segunda_tela = uic.loadUi("untitled1.ui")
tela_editar = uic.loadUi("untitled3.ui")
untitled.pushButton_3.clicked.connect(funcao_principal)
untitled.pushButton_2.clicked.connect(lista2)
segunda_tela.pushButton_2.clicked.connect(gera_pdf)
segunda_tela.pushButton_3.clicked.connect(limpar_dados)

segunda_tela.pushButton_4.clicked.connect(editar_dados)
tela_editar.pushButton_3.clicked.connect(salvar_dados_editados)

untitled.show()
app.exec()
