import pandas as pd

try:
    with open('dummy.csv', 'w') as f:
        f.write('col1,col2\n1,2\n')
    
    df = pd.read_csv('dummy.csv', dtype={'col1': 'int', 'route_changed': 'int'})
    print("Sucesso: CSV lido com dtype extra")
except Exception as e:
    print(f"Erro: {e}")
