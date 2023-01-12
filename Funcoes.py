#!/usr/bin/env python
# coding: utf-8

# # FUNÇÕES

# ## Função Normalizar Dados:

# In[54]:


def normalizar_dados(dados):
    dados = dados.copy()
    for classific in menor_melhor:
        dados[classific] = 1 /(dados[classific])
  
    for normalizar in nome_colunas:
        dados[normalizar] = (dados[normalizar]) / (dados[normalizar].sum())

    return dados


# In[4]:


def normalizar_dados_2(dados):
    dados = dados.copy()
    for classific in menor_melhor:
        dados[classific] = 1 /(dados[classific])
  
    for normalizar in nome_colunas_2:
        dados[normalizar] = (dados[normalizar]) / (dados[normalizar].sum())

    return dados


# ## Função Fator Gaussiano:

# In[2]:


def fator_gaussiano(dados):
    res_fator_gaussiano = dados.std()/dados.mean()
    return res_fator_gaussiano


# ## Função Normalizar Fator Gaussiano:

# In[56]:


def normalizar_fator_gaussiano(fator_gaussiano):
    fator_gaussiano = fator_gaussiano/ fator_gaussiano.sum()
    return fator_gaussiano


# ## Função Ponderar Dados:

# In[57]:


def ponderar_dados(dados):
    dados_ponderados = dados.copy()
    for coluna in nome_colunas:
        dados_ponderados[coluna] = dados_ponderados[coluna] * fator_gaussiano_normalizado[coluna]
    return dados_ponderados


# ## Função Soma das Ponderações:

# In[58]:


def obter_ranking(dados):
    dados_soma_criterios = dados.copy()
    dados_soma_criterios['soma_das_ponderacoes'] = dados_soma_criterios.sum(axis = 1)
    dados_soma_criterios.sort_values(by = 'soma_das_ponderacoes', ascending = False, inplace = True)
    
    return dados_soma_criterios

