#!/usr/bin/env python
# coding: utf-8

# # Estratégia para seleção de ações do setor de energia elétrica a partir do método multicritério AHP - Gaussiano

# ## Importando as bibliotecas necessárias

# In[354]:


import pandas as pd
import dataframe_image as dfi


# ## Carregando a base de dados

# In[355]:


dados = pd.read_csv('dados/statusinvest-busca-avancada.csv', sep = ';')


# In[356]:


dados


# ## Realizando o tratamento da Base de dados

# In[357]:


dados.info()


# ### Verificando o tipo dos dados

# ### Removendo variáveis não necessárias para a análise e missing values

# In[358]:


dados.drop(columns = ['P/ATIVOS',
                      'PSR',
                      'P/CAP. GIRO',
                      'P. AT CIR. LIQ.',
                      'LIQ. CORRENTE',
                      'PATRIMONIO / ATIVOS',
                      'PASSIVOS / ATIVOS',
                      'GIRO ATIVOS',
                      ' VPA',
                      ' PEG Ratio'], inplace = True)


# In[359]:


dados = dados.dropna()


# In[360]:


dados.head()


# ### Renomeando as variáveis da base de dados

# In[361]:


dados.rename(columns= {'TICKER': 'ticker',
                       'PRECO': 'preco',
                       'DY': 'dy',
                       'P/L': 'preco_por_lucro',
                       'P/VP': 'preco_por_vp',
                       'MARGEM BRUTA': 'margem_bruta',
                       'MARGEM EBIT': 'margem_ebit',
                       'MARG. LIQUIDA': 'margem_liquida',
                       'P/EBIT': 'preco_por_ebit',
                       'EV/EBIT': 'ev_por_ebit',
                       'DIVIDA LIQUIDA / EBIT': 'div_liq_por_ebit',
                       'DIV. LIQ. / PATRI.': 'div_liq_por_patri',
                       'ROE': 'roe',
                       'ROA': 'roa',
                       'ROIC': 'roic',
                       'CAGR RECEITAS 5 ANOS': 'cagr_receita_5anos',
                       'CAGR LUCROS 5 ANOS': 'cagr_lucros_5anos',
                       ' LIQUIDEZ MEDIA DIARIA': 'liq_media_diaria',
                       ' LPA': 'lpa',
                       ' VALOR DE MERCADO': 'valor_de_mercado'}, inplace=True)


# In[362]:


dados


# ### Convertando dados do tipo object em valores numéricos

# In[363]:


nome_colunas = list(dados.columns)[1:]
nome_colunas


# In[364]:


for coluna in nome_colunas:
    dados[coluna] = dados[coluna].astype('str')
    dados[coluna] = dados[coluna].str.replace(',', '').str.replace('.', '')
    dados[coluna] = pd.to_numeric(dados[coluna], errors = 'coerce')/ 100


# In[365]:


dados
dados_sem_margens_efic = dados #variável foi criada posteriormente para testar condições ao final do projeto


# In[366]:


dados.info()


# ### Configurando número de casas decimais do dataframe

# In[367]:


pd.options.display.float_format = '{:.4f}'.format


# ### Verificando a média e mediana das variáveis do dataframe

# In[368]:


media_dados = dados.mean()
media_dados


# In[369]:


mediana_dados = dados.median()
mediana_dados


# ## Aplicando o método AHP - Gaussiano 

# ### Etapa 01: Determinando a matriz de decisão

# #### Definindo os critérios e alternativas
# * P/L - deve ser positivo e menor ou igual a 20<br>
# * DY - maior ou  igual a 4%
# * ROE - maior ou igual a 10%
# * Margem Bruta - maior ou igual a 15%
# * CAGR receita 5 anos - deve ser positivo
# * Liquidez média diária - maior ou igual a mediana do setor

# #### Filtrando a Base de dados com base nos critérios mínimos estabelecidos

# In[370]:


max_preco_por_lucro = 20
min_dy = 4
min_roe = 10
min_margem_bruta = 15
min_cagr_receita5anos = 0
min_liq_media_diaria = mediana_dados['liq_media_diaria']


# In[371]:


mediana_dados['liq_media_diaria']


# In[372]:


dados = dados[(dados.preco_por_lucro <= max_preco_por_lucro) &
              (dados.dy >= min_dy) &
              (dados.roe >= min_roe) &
              (dados.margem_bruta >= min_margem_bruta) & 
              (dados.cagr_receita_5anos >= min_cagr_receita5anos) &
              (dados.liq_media_diaria >= min_liq_media_diaria)]


# In[373]:


dados


# #### Exportando dados como imagem

# In[374]:


dfi.export(dados, 'dados.png')


# ##### Analisando os critérios
# 1. preco - quanto MENOR melhor<br>
# 2. dy - quanto MAIOR melhor<br>
# 3. preco_por_lucro - quanto MENOR melhor<br>
# 4. preco_por_vp - quanto MENOR melhor<br>
# 5. margem_bruta - quanto MAIOR melhor<br>
# 6. margem_ebit - quanto MAIOR melhor<br>
# 7. margem_liquida - quanto MAIOR melhor<br>
# 8. preco_por_ebit - quanto MENOR melhor<br>
# 9. ev_por_ebit - quanto MENOR melhor<br>
# 10. div_liq_por_ebit - quanto MENOR melhor<br>
# 11. div_liq_por_patri - quanto MENOR melhor<br>
# 12. roe - quanto MAIOR melhor<br>
# 13. roa - quanto MAIOR melhor<br>
# 14. roic - quanto MAIOR melhor<br>
# 15. cagr_receita_5anos - quanto MAIOR melhor<br>
# 16. cagr_lucros_5anos - quanto MAIOR melhor<br>
# 17. liq_media_diaria - quanto MAIOR melhor<br>
# 18. lpa - quanto MAIOR melhor<br> 
# 19. valor_de_mercado - quanto MAIOR melhor

# In[375]:


menor_melhor = ['preco',
 'preco_por_lucro',
 'preco_por_vp',
 'preco_por_ebit',
 'ev_por_ebit',
 'div_liq_por_ebit',
 'div_liq_por_patri']


# #### Aplicando a função normalizar

# In[376]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
dados_normalizados = normalizar_dados(dados)
dados_normalizados


# ### Etapa 02: Calculando o fator gaussiano para cada critério

# #### Aplicando a função Fator Gaussiano

# In[377]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
res_fator_gaussiano = fator_gaussiano(dados)
res_fator_gaussiano


# In[378]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
fator_gaussiano_normalizado = normalizar_fator_gaussiano(res_fator_gaussiano)
fator_gaussiano_normalizado


# ### Etapa 03: Ponderando a Matriz de Decisão

# In[379]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
dados_ponderados = ponderar_dados(dados_normalizados)
dados_ponderados


# ### Etapa 04: Obtendo o Ranking das alternativas

# #### Aplicando a Função Obter Ranking

# In[380]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
dados_ranqueados = obter_ranking(dados_ponderados)
dados_ranqueados


# #### Organizando o index do DataFrame

# In[381]:


dados_ranqueados.index = range(len(dados_ranqueados))


# In[382]:


dados_ranqueados


# #### Exportando DataFrame ordenado como imagem

# In[383]:


dados_ranqueados.columns


# In[384]:


dados_ranqueados_ordem = dados_ranqueados[['ticker','soma_das_ponderacoes', 'preco', 'dy', 'preco_por_lucro', 'preco_por_vp',
       'margem_bruta', 'margem_ebit', 'margem_liquida', 'preco_por_ebit',
       'ev_por_ebit', 'div_liq_por_ebit', 'div_liq_por_patri', 'roe', 'roa',
       'roic', 'cagr_receita_5anos', 'cagr_lucros_5anos', 'liq_media_diaria',
       'lpa', 'valor_de_mercado']]
dfi.export(dados_ranqueados_ordem, 'dados_ranqueados_ordem.png')


# In[385]:


dados_ranqueados_ordem


# ### Análises Gráficas

# In[386]:


import seaborn as sns
import matplotlib.pyplot as plt


# ### Analisando a correlação entre as variáveis

# In[387]:


plt.figure(figsize=(14,10))
corr_var = sns.heatmap(dados_ranqueados_ordem.corr().round(2),
                      vmin = -1,
                      vmax = 1,
                      annot = True,
                      cmap='coolwarm')
corr_var.set_title('Correlação entre as variáveis', fontsize=16, y= 1.01)


# ### Analisando a correlação entre os critérios e a soma das ponderações

# In[388]:


plt.figure(figsize=(10,8))
corr_var_soma_pond = sns.heatmap(dados_ranqueados_ordem.corr()[['soma_das_ponderacoes']].sort_values(by='soma_das_ponderacoes',
                                                                                                     ascending=False).round(2),
                      vmin = -1,
                      vmax = 1,
                      annot = True,
                      cmap='coolwarm')
corr_var_soma_pond.set_title('Critérios correlacionados com a Soma das ponderações', fontsize=16, y= 1.01)


# In[389]:


dados_ranqueados_ordem[['soma_das_ponderacoes','margem_bruta', 'margem_ebit', 'margem_liquida']].describe()


# In[390]:


dados[['margem_bruta', 'margem_ebit', 'margem_liquida']].describe()


# =========================================================================================================================

# ##  Aplicando novamente o modelo removendo os indicadores de eficiência
# 
# Objetivo: Verificar se haverá alteração no ranking com a remoção das variáveis que apresentaram fortes correlações positivas com a variável responsável pelo ranqueamento do modelo (soma_das_ponderações)

# ### Visualizando a base de dados

# In[391]:


dados_sem_margens_efic
dados_sem_margens_efic.head()


# ### Removendo os indicadores de eficiência (margem_bruta, margem_ebit, margem_liquida)

# In[392]:


dados_sem_margens_efic.drop(columns = ['margem_bruta', 'margem_ebit', 'margem_liquida'], inplace = True)
dados_sem_margens_efic.head()


# ### Aplicando o método AHP - Gaussiano

# #### Etapa 01: Determinando a matriz de decisão

# #### Definindo os critérios e alternativas (Mesmos critérios utilizados anteriormente)
# * P/L - deve ser positivo e menor ou igual a 20<br>
# * DY - maior ou  igual a 4%
# * ROE - maior ou igual a 10%
# * Margem Bruta - maior ou igual a 15% (REMOVIDA)
# * CAGR receita 5 anos - deve ser positivo
# * Liquidez média diária - maior ou igual a mediana do setor

# #### Filtrando a Base de dados com base nos critérios mínimos estabelecidos

# In[393]:


max_preco_por_lucro = 20
min_dy = 4
min_roe = 10
#min_margem_bruta = 15
min_cagr_receita5anos = 0
min_liq_media_diaria = mediana_dados['liq_media_diaria']


# In[394]:


dados_sem_margens_efic = dados_sem_margens_efic[(dados_sem_margens_efic.preco_por_lucro <= max_preco_por_lucro) &
              (dados_sem_margens_efic.dy >= min_dy) &
              (dados_sem_margens_efic.roe >= min_roe) &
              (dados_sem_margens_efic.cagr_receita_5anos >= min_cagr_receita5anos) &
              (dados_sem_margens_efic.liq_media_diaria >= min_liq_media_diaria)]


# In[395]:


dados_sem_margens_efic


# ##### Analisando os critérios
# 1. preco - quanto MENOR melhor<br>
# 2. dy - quanto MAIOR melhor<br>
# 3. preco_por_lucro - quanto MENOR melhor<br>
# 4. preco_por_vp - quanto MENOR melhor<br>
# 5. margem_bruta - quanto MAIOR melhor (REMOVIDA)<br>
# 6. margem_ebit - quanto MAIOR melhor (REMOVIDA)<br>
# 7. margem_liquida - quanto MAIOR melhor (REMOVIDA)<br>
# 8. preco_por_ebit - quanto MENOR melhor<br>
# 9. ev_por_ebit - quanto MENOR melhor<br>
# 10. div_liq_por_ebit - quanto MENOR melhor<br>
# 11. div_liq_por_patri - quanto MENOR melhor<br>
# 12. roe - quanto MAIOR melhor<br>
# 13. roa - quanto MAIOR melhor<br>
# 14. roic - quanto MAIOR melhor<br>
# 15. cagr_receita_5anos - quanto MAIOR melhor<br>
# 16. cagr_lucros_5anos - quanto MAIOR melhor<br>
# 17. liq_media_diaria - quanto MAIOR melhor<br>
# 18. lpa - quanto MAIOR melhor<br> 
# 19. valor_de_mercado - quanto MAIOR melhor

# In[396]:


menor_melhor = ['preco',
 'preco_por_lucro',
 'preco_por_vp',
 'preco_por_ebit',
 'ev_por_ebit',
 'div_liq_por_ebit',
 'div_liq_por_patri']


# In[397]:


nome_colunas_2 = nome_colunas
nome_colunas_2.remove('margem_bruta')
nome_colunas_2.remove('margem_ebit')
nome_colunas_2.remove('margem_liquida')
nome_colunas_2


# #### Aplicando a função normalizar

# In[398]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
dados_normalizados_sem_margens_efic = normalizar_dados_2(dados_sem_margens_efic)
dados_normalizados_sem_margens_efic


# #### Etapa 02: Calculando o fator gaussiano para cada critério

# In[399]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
res_fator_gaussiano_sem_margens = fator_gaussiano(dados_normalizados_sem_margens_efic)
res_fator_gaussiano_sem_margens


# In[400]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
fator_gaussiano_normalizado_sem_margens = normalizar_fator_gaussiano(res_fator_gaussiano_sem_margens)
fator_gaussiano_normalizado_sem_margens


# #### Etapa 03: Ponderando a Matriz de Decisão

# In[401]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
dados_ponderados_sem_margens = ponderar_dados(dados_normalizados_sem_margens_efic)
dados_ponderados_sem_margens


# #### Etapa 04: Obtendo o Ranking das alternativas

# In[402]:


get_ipython().run_line_magic('run', '"Funcoes.ipynb"')
dados_ranqueados_sem_margens = obter_ranking(dados_ponderados_sem_margens)
dados_ranqueados_sem_margens


# #### Organizando o index do DataFrame  e ordenando os dados

# In[404]:


dados_ranqueados_sem_margens.index = range(len(dados_ranqueados_sem_margens))
dados_ranqueados_sem_margens


# In[406]:


dados_ranqueados_ordem_sem_margens = dados_ranqueados_sem_margens[['ticker','soma_das_ponderacoes', 'preco', 'dy', 'preco_por_lucro', 'preco_por_vp', 'preco_por_ebit',
       'ev_por_ebit', 'div_liq_por_ebit', 'div_liq_por_patri', 'roe', 'roa',
       'roic', 'cagr_receita_5anos', 'cagr_lucros_5anos', 'liq_media_diaria',
       'lpa', 'valor_de_mercado']]
dados_ranqueados_ordem_sem_margens


# In[407]:


dfi.export(dados_ranqueados_ordem_sem_margens, 'dados_ranqueados_ordem_sem_margens.png')


# #### Analisando a correlação entre os critérios e a soma das ponderações¶

# In[408]:


plt.figure(figsize=(10,8))
corr_var_soma_pond_sem_margens = sns.heatmap(dados_ranqueados_ordem_sem_margens.corr()[['soma_das_ponderacoes']].sort_values(by='soma_das_ponderacoes',
                                                                                                     ascending=False).round(2),
                      vmin = -1,
                      vmax = 1,
                      annot = True,
                      cmap='coolwarm')
corr_var_soma_pond_sem_margens.set_title('Critérios correlacionados com a Soma das ponderações', fontsize=16, y= 1.01)


# In[ ]:




