def mediaPonderada():
    valores = {
        "nota1": {
            "valor": 5,
            "peso": 2
        },
        "nota2": {
            "valor": 10,
            "peso": 3
        },
        "nota3": {
            "valor": 15,
            "peso": 5
        }
    } # objeto com os valores, para adicionar mais basta aumentar o json

    total = 0

    for key in valores: # loop dentro dos objetos
        valor = valores[key] # pega o índice atual
        tempTotal = total # salva um valor de forma temporária
        total = valor['valor'] * valor['peso'] # multiplica os valores atuais
        total = total + tempTotal # soma ao total o valor multiplicado
    
    return total / 10 # na hora de retornar, divide por 10

print(mediaPonderada()) # calcula a média ponderada