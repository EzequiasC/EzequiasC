texto = input("Informe um texto: ")
VOGAIS = "AEIOU"

for letra in texto:
    if letra.upper() in VOGAIS:
        print(letra, end=" ")
else:
     print()
     print("Fim do programa")


     
#### 
for numero in range(0, 11):
    print(numero, end=" ")


#### while

opcao = -1

while opcao != 0:
    opcao = int(input("[1] sacar \n[2] depositar \n[3] saldo \n[0] sair \nEscolha uma opção: "))
    if opcao == 1:
        print("Saque")
    elif opcao == 2:
        print("Depositar")
    elif opcao == 3:
        print("Saldo")
    