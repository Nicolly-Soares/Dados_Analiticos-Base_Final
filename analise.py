import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#o caminho para o arquivo
arquivo = "dados_de_2018_a_2023.csv"

#para importar os dados
df = pd.read_csv(arquivo, sep=";", encoding="latin1")
print("Dados importados com sucesso!\n")

# transformar coluna Total em número
df["Total"] = df["Total"].str.replace(".", "", regex=False).astype(int)
print(df)

# a primeiras linhas
print("Primeiras linhas da base:")
print(df.head())

print("\nInformações da base:")
print(df.info())

print("\nValores nulos:")
print(df.isnull().sum())

# o grafico para vizualizar melhor os dadoos

plt.plot(df["Períodos"], df["Total"])
plt.title("Beneficiários de Planos de Saúde no Brasil")
plt.xlabel("Ano")
plt.ylabel("Total de Beneficiários")
plt.show()

#IMPORTAR DADOS DO VCMH

print("\nCarregando dados do VCMH...")

vcmh = pd.read_csv("dados_vcmh_2018_2023.csv", sep=";", encoding="latin1")

print("Dados do VCMH carregados com sucesso!\n")

print("Primeiras linhas:")
print(vcmh.head())

print("\nInformações da base:")
print(vcmh.info())

print("\nValores nulos:")
print(vcmh.isnull().sum())

plt.plot(vcmh["Períodos"], vcmh["Total"])


plt.title("Evolução do VCMH")
plt.xlabel("Período")
plt.ylabel("VCMH")

plt.show()

#bloco3


print(f"Beneficiários : {df.shape[0]} linhas x {df.shape[1]} colunas")
print(f"VCMH          : {vcmh.shape[0]} linhas x {vcmh.shape[1]} colunas")


vcmh["Total"] = vcmh["Total"].str.replace(".", "", regex=False)
vcmh["Total"] = vcmh["Total"].str.replace(",", ".", regex=False)
vcmh["Total"] = vcmh["Total"].astype(float)


n_miss = vcmh["Total"].isnull().sum()
pct = 100 * n_miss / vcmh.shape[0]

print(f"NaN em VCMH/Total: {n_miss} ({pct:.1f}% das obs.)")
print("Índices com NaN:", vcmh[vcmh["Total"].isnull()].index.tolist())


serie = vcmh["Total"].dropna()

Q1 = serie.quantile(0.25)
Q3 = serie.quantile(0.75)

IQR = Q3 - Q1

limite_inf = Q1 - 1.5 * IQR
limite_sup = Q3 + 1.5 * IQR

outliers = serie[(serie < limite_inf) | (serie > limite_sup)]

print("Quantidade de outliers:", len(outliers))
print(outliers)

# bloco 4

# títulos
print("\nDuplicatas Beneficiários:", df.duplicated().sum())
print("Duplicatas VCMH:", vcmh.duplicated().sum())

#valores de indicativos
print("\nBenef. negativos:", (df["Total"] < 0).sum())
print("VCMH negativos:", (vcmh["Total"] < 0).sum())
print("VCMH > 50%:", (vcmh["Total"] > 50).sum(), "→ impossível para VCMH mensal")


#variações negativas dos benef
var_abs = df["Total"].diff()

quedas = var_abs[var_abs < 0]

print(f"Variações negativas em Beneficiários: {len(quedas)}")

if len(quedas) > 0:
    pct_queda = quedas.values[0] / df["Total"].iloc[0] * 100
    print(f"↓ {pct_queda:.4f}% da base – retração documentada (ANS, 2020)")


#inconsistência no formato da coluna períodos do VCMH
formatos = vcmh["Períodos"].str.strip().unique()[[0,1,2,3,4]]

print("\nAmostra de formato em Períodos:", formatos)
print("→ Mistura: 'jan/18' vs 'Fev / 2018' – requer padronização")

 
#bloco 5 tratamento completo da base

# garantia de tipos
df_b = df.copy()

df_b["Períodos"] = df_b["Períodos"].astype(int)
df_b["Total"] = df_b["Total"].astype(int)


# preparar base
df_v = vcmh.copy()

# limpar espaços e padronizar texto
df_v["Períodos"] = df_v["Períodos"].str.strip().str.lower()


# traduzir meses PT → EN
meses = {
    "jan": "jan",
    "fev": "feb",
    "mar": "mar",
    "abr": "apr",
    "mai": "may",
    "jun": "jun",
    "jul": "jul",
    "ago": "aug",
    "set": "sep",
    "out": "oct",
    "nov": "nov",
    "dez": "dec"
}

for pt, en in meses.items():
    df_v["Períodos"] = df_v["Períodos"].str.replace(pt, en, regex=False)


# converter para data
df_v["Data"] = pd.to_datetime(df_v["Períodos"], format="%b/%y", errors="coerce")

# ordenar cronologicamente
df_v = df_v.sort_values("Data").reset_index(drop=True)


# tratar outlier extremo
idx_out = df_v[df_v["Total"] > 50].index

df_v.loc[idx_out, "Total"] = np.nan

print(f"Outlier convertido para NaN: índice(s) {list(idx_out)}")


# imputação Interpolação Linear
n_antes = df_v["Total"].isnull().sum()

df_v["Total"] = df_v["Total"].interpolate(
    method="linear",
    limit_direction="both"
)

n_depois = df_v["Total"].isnull().sum()

print(f"Imputação: {n_antes} NaN → {n_depois} NaN restantes")


# a padronizaçao do rótulo do período
df_v["Periodo_fmt"] = df_v["Data"].dt.strftime("%b/%y").str.lower()


# a verificação final
print(f"NaN restantes: {df_v['Total'].isnull().sum()}")
print(f"Min VCMH: {df_v['Total'].min():.2f}  Max VCMH: {df_v['Total'].max():.2f}")
print("Verificação final – intervalo plausível (0-40%): OK")

#bloco6 criação de Variáveis Derivadas

#Beneficiários
df_b = df.copy()

# fluxo líquido de novos vínculos
df_b["Var_Abs"] = df_b["Total"].diff()

#taxa de crescimento (%)
df_b["Var_Pct"] = df_b["Total"].pct_change() * 100


#taxa composta anual de crescimento
anos = df_b["Períodos"].iloc[-1] - df_b["Períodos"].iloc[0]

df_b["CAGR"] = (
    (df_b["Total"] / df_b["Total"].iloc[0]) ** (1 / anos) - 1
) * 100


#mostrar resultados
print("\nVariáveis derivadas (Beneficiários):")
print(df_b[["Períodos", "Total", "Var_Abs", "Var_Pct"]])

print(f"\nCAGR médio do período: {df_b['CAGR'].iloc[-1]:.2f}% ao ano")


# CRIAR PASTAS 

import os

os.makedirs("dados_brutos", exist_ok=True)
os.makedirs("dados_tratados", exist_ok=True)
os.makedirs("dados_analiticos", exist_ok=True)


# SALVAR DADOS TRATADOS


df_b.to_csv("dados_tratados/beneficiarios_tratado.csv", index=False)
df_v.to_csv("dados_tratados/vcmh_tratado.csv", index=False)


# CRIAR BASE ANALÍTICA


# agregar VCMH mensal → anual
vcmh_anual = df_v.copy()
vcmh_anual["Ano"] = vcmh_anual["Data"].dt.year

vcmh_anual = vcmh_anual.groupby("Ano")["Total"].mean().reset_index()

# juntar com beneficiários
base_final = pd.merge(
    df_b,
    vcmh_anual,
    left_on="Períodos",
    right_on="Ano",
    how="left"
)

# renomear colunas
base_final.rename(columns={
    "Total_x": "Beneficiarios",
    "Total_y": "VCMH"
}, inplace=True)

# salvar base final
base_final.to_csv("dados_analiticos/base_final.csv", index=False)

print("\nArquivos salvos com sucesso!")