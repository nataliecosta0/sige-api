import pandas as pd

def loadfile(path):
    import ipdb; ipdb.sset_trace()

    data = pd.read_excel(path) 
    df = pd.DataFrame(data, columns= ['Usuario', 'curso'])
    print (df.to_dict())