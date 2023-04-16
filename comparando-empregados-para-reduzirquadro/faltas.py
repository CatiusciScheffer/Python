import pandas as pd;
import numpy as np;
import seaborn as sns; sns.set();
import matplotlib.pyplot as plt;
import plotly.express as px;
import ssl

df_lev = pd.read_excel("Movimentos.xlsx")

df_mot_falta_dsr = df_lev.groupby('NOME')[['MOTIVO', 'VALOR_CALCULADO']].sum().reset_index()
df_mot_falta_dsr = df_mot_falta_dsr.groupby('NOME').agg({
            'VALOR_CALCULADO': sum
        })
df_mot_falta_dsr= df_mot_falta_dsr.sort_values(by=['VALOR_CALCULADO'], ascending=False)
print(df_mot_falta_dsr.head(10))

df_selecao_motivo = df_lev.groupby(['MOTIVO', 'NOME', 'VALOR_CALCULADO']).sum().reset_index()
df_motivo1 = df_selecao_motivo[df_selecao_motivo['MOTIVO'] == 'ATESTADO/JUST']
df_motivo1= df_motivo1[['MOTIVO', 'NOME', 'VALOR_CALCULADO']]
df_motivo1 = df_motivo1.groupby('NOME').agg({
            'VALOR_CALCULADO': sum
        })
df_motivo1= df_motivo1.sort_values(by=['VALOR_CALCULADO'], ascending=False)
print(df_motivo1.head(10))


df_motivo2 = df_selecao_motivo[df_selecao_motivo['MOTIVO'] == 'FALTA']
df_motivo2= df_motivo2[['MOTIVO', 'NOME', 'VALOR_CALCULADO']]
df_motivo2 = df_motivo2.groupby('NOME').agg({
            'VALOR_CALCULADO': sum
        })
df_motivo2= df_motivo2.sort_values(by=['VALOR_CALCULADO'], ascending=False)
print(df_motivo2.head(10))


df_motivo3 = df_selecao_motivo[df_selecao_motivo['MOTIVO'] == 'DSR']
df_motivo3= df_motivo3[['MOTIVO', 'NOME', 'VALOR_CALCULADO']]
df_motivo3 = df_motivo3.groupby('NOME').agg({
            'VALOR_CALCULADO': sum
        })
df_motivo3= df_motivo3.sort_values(by=['VALOR_CALCULADO'], ascending=False)
print(df_motivo3.head(10))


df_motivo = df_lev.groupby(['MOTIVO']).sum().reset_index()
df_motivo = df_motivo[['MOTIVO', 'VALOR_CALCULADO']]
df_motivo= df_motivo.sort_values(by=['VALOR_CALCULADO'], ascending=False)
plt.figure(figsize=(6,3))
plt.xticks(rotation = 45)
plt.title('Custo por motivo de ausência')
print(df_motivo)
sns.barplot(data=df_motivo, x='MOTIVO', y='VALOR_CALCULADO')


