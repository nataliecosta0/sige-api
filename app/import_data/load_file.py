import pandas as pd

def loadfile(path):
    import ipdb; ipdb.sset_trace()

    data = pd.read_excel(path) 
    df = pd.DataFrame(data, 
                    columns= ['Código da Unidade', 'Nome da Unidade', 
                    'Código do Curso', 'Nome do Curso', 'Turno (por extenso)',
                    'RA', 'Nome', 'Data de Nascimento', 'Data de Ingresso' , 
                    'Ano de Ingresso', 'Turma de Ingresso', 'Semestre de Ingresso',
                    'Data de Conclusão', 'Sexo', 'Cor', 'Nacionalidade', 
                    'Situação no Curso', 'RG', 'Email', 'Telefone', 'Nome do Pai', 
                    'Nome da Mãe', 'Nome do Cônjuge', 'Endereço Familiar', 
                    'Endereço Residencial', 'Bairro Comercial', 'CEP Comercial', 
                    'Bairro Familiar', 'CEP Familiar', 'Bairro Residencial',
                    'CEP Residencial', 'Telefone Residencial', 'Telefone Comercial', 
                    'Fax', 'Telefone Recado', 'Cidade Comercial', 'Cidade Familiar', 
                    'Cidade Residencial', 'CPF', 'Estabelecimento de Ensino', 
                    'Semestre Atual', 'Semestres Cursados', 'PP', 'PR', 'Turno (numérico)', 
                    'Naturalidade', 'Estado Naturalidade']
                    )
    print (df.to_dict())