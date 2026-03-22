import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# a config da pagina
st.set_page_config(layout="wide")

# carregar dados
df = pd.read_csv("dados_analiticos/base_final.csv")

# css para o estilo do mnosso dashboar
st.markdown("""
<style>
body {
    background-color: #020617;
}

.card {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}

.title {
    font-size: 28px;
    font-weight: bold;
}

.subtitle {
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)


#titulo
st.title("📊 Dashboard - Saúde Suplementar")
st.markdown("Análise de beneficiários e da variação dos custos médicos-hospitalares (VCMH) entre os anos 2018 a 2023")

st.divider()
#filtro

st.sidebar.header("🎛️ Filtro")

ano = st.sidebar.slider(
    "Selecione até qual ano quer visualizar:",
    int(df["Períodos"].min()),
    int(df["Períodos"].max()),
    int(df["Períodos"].max())
)

df_filtrado = df[df["Períodos"] <= ano].copy()
df_filtrado["Períodos"] = df_filtrado["Períodos"].astype(str)

#metricass
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        <h4>👥 Beneficiários</h4>
        <h2>{df_filtrado['Beneficiarios'].iloc[-1]:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h4>💰 VCMH Médio</h4>
        <h2>{df_filtrado['VCMH'].mean():.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    crescimento = df_filtrado["Beneficiarios"].pct_change().mean()*100
    st.markdown(f"""
    <div class="card">
        <h4>📈 Crescimento</h4>
        <h2>{crescimento:.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

st.divider()

#graficos princ.
col1, col2 = st.columns(2)

# gráfico beneficiários
graf1 = alt.Chart(df_filtrado).mark_line(point=True, color="#22c55e").encode(
    x=alt.X("Períodos:N", axis=alt.Axis(labelAngle=0)),
    y="Beneficiarios:Q",
    tooltip=["Períodos", "Beneficiarios"]
)

with col1:
    
    st.subheader("📈 Beneficiários")
    st.altair_chart(graf1, use_container_width=True)
 

# gráfico VCMH
graf2 = alt.Chart(df_filtrado).mark_line(point=True, color="#f59e0b").encode(
    x=alt.X("Períodos:N", axis=alt.Axis(labelAngle=0)),
    y="VCMH:Q",
    tooltip=["Períodos", "VCMH"]
)

with col2:
    
    st.subheader("📉 VCMH")
    st.altair_chart(graf2, use_container_width=True)


st.divider()

#graficos segundos
col1, col2 = st.columns(2)

# barras
graf_bar = alt.Chart(df_filtrado).mark_bar(color="#3b82f6").encode(
    x=alt.X("Períodos:N", axis=alt.Axis(labelAngle=0)),
    y="Beneficiarios:Q"
)

with col1:
    
    st.subheader("📊 Comparação Anual")
    st.altair_chart(graf_bar, use_container_width=True)
    

# pizza
fig = px.pie(
    df_filtrado,
    values="Beneficiarios",
    names="Períodos",
    hole=0.5
)

with col2:

    st.subheader("🥧 Distribuição")
    st.plotly_chart(fig, use_container_width=True)
  

st.divider()

#insigts
st.subheader("📌 Percepção")

col1, col2, col3 = st.columns(3)

col1.success("Crescimento contínuo de beneficiários")
col2.warning("Oscilações relevantes no VCMH")
col3.info("Custos crescem com o aumento da base")

st.divider()

#conclusão
st.markdown("""
<div class="card">
<h3>📌 Conclusão</h3>
<p>
O número de beneficiários apresenta crescimento consistente ao longo do período, 
enquanto o VCMH demonstra variações relevantes, indicando aumento da pressão 
sobre os custos do sistema de saúde suplementar.
</p>
</div>
""", unsafe_allow_html=True)