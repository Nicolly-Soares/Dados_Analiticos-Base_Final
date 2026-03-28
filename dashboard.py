import streamlit as st
import pandas as pd
import altair as alt

#carregamento dos dados 
df = pd.read_csv("dados_analiticos/base_final.csv")

st.set_page_config(layout="wide")

#cores e cards

st.markdown("""
            <style>
            .metric-box{
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.3);
            }
</style>
            """, unsafe_allow_html=True
            )



#título

st.title("📊 Dashboard - Saúde Sumplementar")
st.markdown("Análise de beneficiários e custos médicos-hospitalares (VCMH) entre os anos 2018 a 2023")

#metricas
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <h4>Beneficiários</h4>
        <h2>{df['Beneficiarios'].iloc[-1]:,.0f}.replace(",", ".")</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <h4>VCMH Médio</h4>
        <h2>{df['VCMH'].mean():.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <h4>Crescimento</h4>
        <h2>{df['Beneficiarios'].pct_change().mean()*100:.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("## 🎛️ Filtro")

ano = st.slider(
    "Selecione até qual ano visualizar:",
    int(df["Períodos"].min()),
    int(df["Períodos"].max())
)

df_filtrado = df[df["Períodos"] <= ano]

df_filtrado["Períodos"] = df_filtrado["Períodos"].astype(str)

st.divider()

#graficos

df_filtrado["Períodos"] = df_filtrado["Períodos"].astype(str)

# dos beneficiários
graf1 = alt.Chart(df_filtrado).mark_line(point=True, color="green").encode(
    x=alt.X("Períodos:N", title="Ano", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Beneficiarios:Q",
             title="Total",
             scale=alt.Scale(
                domain=[
                df_filtrado["Beneficiarios"].min()*0.995,
                df_filtrado["Beneficiarios"].max()*1.005
                ])
    ),
    tooltip=["Períodos", "Beneficiarios"]
)
# gráfico VCMH
graf2 = alt.Chart(df_filtrado).mark_line(point=True, color="orange").encode(
    x=alt.X("Períodos:N", title="Ano", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("VCMH:Q", title="VCMH (%)"),
    tooltip=["Períodos", "VCMH"]
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Crescimento Dos Beneficiários")
    st.altair_chart(graf1, use_container_width=True)

with col2:
    st.subheader("📉 Variação Dos Custos Médicos-Hospitalares")
    st.altair_chart(graf2, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("### 📌 Interpretação dos Gráficos")

st.write("""
Observa-se crescimento contínuo no número de beneficiários ao longo do período.
O VCMH apresenta maior volatilidade, indicando variações nos custos de saúde.
""")

st.divider()

st.markdown("## 📌 Insights")

col1, col2, col3 = st.columns(3)

col1.success("Crescimento contínuo de beneficiários")
col2.warning("Oscilação relevante no VCMH")
col3.info("Custos crescem com usuários")

st.divider()

#conclusão
st.markdown("""
<div style="
background-color: #FFFFFF; 
padding:20px;
border-radius:10px;
margin-top:20px;
box-shadow:0px 2px 10px rgba(0,0,0,0.3);
">
<h3>📌 Conclusão</h3>
<p>
Observa-se crescimento no número de beneficiários ao longo do período, 
acompanhado pela elevação dos custos médico-hospitalares (VCMH), 
indicando maior pressão sobre o sistema de saúde suplementar.
</p>
</div>
""", unsafe_allow_html=True)
