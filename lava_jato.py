from datetime import timedelta, datetime

tipo_carro = 'P' # P, M, G
tempo_pqueno = 30
tempo_medio = 45
tempo_grande = 60
data_atual = datetime.now()

if tipo_carro == 'P':
    data_estimada = data_atual + timedelta(minutes=tempo_pqueno)
    print('O carro chegou ás: {}, e ficará pronto ás {}'.format(data_atual, data_estimada))
elif tipo_carro == 'M':
    data_estimada = data_atual + timedelta(minutes=tempo_medio)
    print('O carro chegou ás: {}, e ficará pronto ás {}'.format(data_atual, data_estimada))
else:
    data_estimada = data_atual + timedelta(minutes=tempo_grande)
    print('O carro chegou ás: {}, e ficará pronto ás {}'.format(data_atual, data_estimada))    