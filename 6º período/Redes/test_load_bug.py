import pandas as pd
try:
    # Create dummy csv without route_changed
    with open('dummy.csv', 'w') as f:
        f.write('col1,col2\n1,2\n')
    
    # Try reading with extra dtype
    df = pd.read_csv('dummy.csv', dtype={'col1': 'int', 'route_changed': 'int'})
    print("Success: Read CSV with extra dtype")
except Exception as e:
    print(f"Error: {e}")
