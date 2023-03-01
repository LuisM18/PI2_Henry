import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import plotly.express as px
import openpyxl

acciones = ['AZO', 'TSCO', 'NEE', 'AES', 'CTVA', 'LIN', 'EXR', 'MAA', 'HES', 'COP']

################################## SIDEBAR ##################################
st.set_page_config(
    page_title="Simulador de portafolio de inversión",
    layout="wide",
    initial_sidebar_state='expanded'
)

st.sidebar.markdown('''
# **Proyecto Individual Henry Bootcamp**
---
''')           

st.sidebar.header('Parametros de portafolio')

st.sidebar.subheader('Acciones')
acciones_select = st.sidebar.multiselect('Seleccione las acciones del portafolio',options=acciones,default=acciones,key='select')

st.sidebar.subheader('Método de ponderación')
ponderacion = st.sidebar.radio('Seleccione método de ponderación',options= ['Capitalización', 'Equiponderado','Riesgo'])

st.sidebar.subheader('Inversión inicial(USD)')
capital_inicial = st.sidebar.number_input('Inversión inicial',value=100000,step=1000,label_visibility='collapsed')

st.sidebar.subheader('Fecha de inicio de inversión')
start_date = st.sidebar.date_input('Fecha',dt.date(2023,1,1),label_visibility='collapsed')

#Opcion para agregar boton accion a la lista
st.sidebar.subheader('Agregar accion al portafolio')
text,boton = st.sidebar.columns(2)
agregar = text.text_input('Ticket',max_chars=7,placeholder='ej. AAPL',label_visibility='collapsed')

if boton.button('Agregar'):    
    st.write('Fue agregado al universo de inversión')

st.sidebar.markdown('''
---
Creado por [Luis Miguel Vargas](https://github.com/LuisM18).
''')


################################## DATA ################################## 
@st.experimental_memo(persist='disk',experimental_allow_widgets=True)
def get_data(acciones,start):
    
    end = dt.date.today()
    if (end-start).days < 360:
        start = end - dt.timedelta(days=1460)
    
    data = yf.download(acciones,start,end)['Adj Close']
    st.success('La data fue cargada correctamente')

    return data

@st.experimental_memo(persist='disk',experimental_allow_widgets=True)
def get_marketcap(acciones):

    mkt_cap = []
    for i in acciones:
        x = pdr.get_quote_yahoo(i)['marketCap']
        mkt_cap.append(x)

    market_cap  = pd.concat(mkt_cap, axis=0).values

    return market_cap

def get_kpis(acciones):

    kpis = {}
    for i in acciones:
        m = pd.read_excel('https://stockrow.com/api/companies/{}/financials.xlsx?dimension=Q&section=Metrics&sort=desc'.format(i))
        m['kpis'] = m.iloc[:,0]
        m.set_index('kpis',inplace=True)
        m = m.loc[['Debt/Equity','Current Ratio','Net Profit Margin']]
        m = m.T
        m = m.iloc[1:,:]
        m = m.apply(pd.to_numeric)
        kpis['{}_kpis'.format(i)] = m


    return kpis

def get_pesos(data,acciones,ponderacion):

    if ponderacion == 'Capitalización':

        market_cap = get_marketcap(acciones)
        pesos = market_cap/market_cap.sum()        

    elif ponderacion == 'Riesgo':

        rent = np.log1p(data.pct_change())
        vol_inv = 1/(rent.std()*np.sqrt(252))
        
        pesos = vol_inv/vol_inv.sum()
        pesos = pesos.values        

    else:

        pesos = np.full(shape=len(acciones),
                fill_value=1/len(acciones),
                dtype=float)
        
    return pesos


def get_portafolio(data,pesos):

    portafolio = []
    for i,row in data.iterrows(): 
        portafolio.append(np.dot(row,pesos))   

    data['Portafolio'] = portafolio

    return data['Portafolio']

data = get_data(acciones_select,start_date)
pesos = get_pesos(data,acciones_select,ponderacion)
portafolio = get_portafolio(data,pesos)
kpis = get_kpis(acciones)


################################## Graficos portafolio ##################################

st.markdown('''
# Simulador de portafolio de inversón
---
''')
            
st.header('Grafico de desempeño del portafolio')

rent_port = np.log1p(portafolio.pct_change())
cum_port = ((1+rent_port[start_date:]).cumprod()-1)

c1,c2 = st.columns([4,1])

with c1:

    tab1, tab2 = st.tabs(["Rendimiento acumulado", "Rendimiento diario"])

    with tab1:

        fig = px.line(cum_port)
        fig.update_yaxes(tickformat=".2%")
        fig.update_layout(showlegend=False)

        st.plotly_chart(fig,theme='streamlit',use_container_width=True)

    with tab2:

        fig2 = px.bar(rent_port[start_date:])
        fig2.update_yaxes(tickformat=".2%")
        fig2.update_layout(showlegend=False)

        st.plotly_chart(fig2,theme='streamlit',use_container_width=True)

with c2:

    st.metric('Balance',"${:,.0f}".format(round(capital_inicial*(1+cum_port[-1]),0)))

################################## KPIs ##############################
    st.markdown('''
    ---
    ### KPIs 📈
    ''')

    st.metric('ROI',"{0:.2%}".format(round(cum_port[-1],2)))   

    var = rent_port.quantile(0.05)*20
    st.metric('VAR Mensual(95%)',"{0:.2%}".format(round(var,2)),
              help='El VAR(Value at Risk) es la medida de la maáxima pérdida esperada en un mes, con un 95% de confianza')
    
    vol = rent_port[-20:].std()*np.sqrt(20)
    r_mes = ((1+rent_port[-20:].mean())**20)-1
    sharpe = r_mes/vol
    st.metric('Sharpe (Mensual)',round(sharpe,2),
              help='El ratio de Sharpe es una medida de la rentabilidad ajustada al riesgo, es mejor si es un valor\n superior a 1, ya que indica que por cada unidad de rentabilidad se asume menor riesgo')



################################## Composicion ##############################
st.markdown('''
---
# Composición del portafolio
''')

tabc1, tabc2 = st.tabs(['Gráfico','Tabla'])

with tabc1:
    pie = pd.DataFrame({'Ticket':acciones_select,
                        'Ponderacion':pesos})
    fig3 = px.pie(pie,values='Ponderacion',names='Ticket')
    st.plotly_chart(fig3, use_container_width=True)

with tabc2:
    st.markdown('''
    
    ''')
    info = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0][['Symbol','Security']]       
    info.set_index('Symbol',inplace=True)
    info.rename(columns={'Symbol':'Ticket','Security':'Empresa'},inplace=True)
    info = info[info.index.isin(acciones_select)]
    info['Ponderación'] = pesos
    info['Inversión inicial'] = info['Ponderación']*capital_inicial

    rent = np.log1p(data.pct_change())
    cum_rent = ((1+rent[start_date:]).cumprod()-1).iloc[-1:]

    info['ROI'] = cum_rent.T.iloc[:-1,0].values
    info['Beneficio'] = info['Inversión inicial']*info['ROI']        
    info['Balance'] = info['Inversión inicial'] + info['Beneficio']

    format_map = {'Ponderación':'{:,.2%}',
                    'Inversión inicial':'${:,.2f}',
                    'ROI':'{:,.2%}',
                    'Beneficio':'${:,.2f}',
                    'Balance':'${:,.2f}'}        


    info.sort_values(['Ponderación'],ascending=False,inplace=True)
    st.dataframe(info.style.format(format_map),use_container_width=True)

################################## Graficos acciones ##############################
st.markdown('''
---
# Gráfico de desempeño de cada accion
''')

acciones_grafico = st.multiselect('Seleccione las acciones del portafolio',options=acciones_select,default=acciones_select)

rent_cum_acciones = ((1+rent[start_date:]).cumprod()-1)

fig4 = px.line(rent_cum_acciones[acciones_grafico])
fig4.update_yaxes(tickformat=".2%")
st.plotly_chart(fig4,theme='streamlit',use_container_width=True)


################################## KPIs Empresas #################################
st.markdown('''
---
# KPIs por empresa
''')

accion = st.selectbox('Seleccione la accion a analizar',tuple(acciones_select))

de , margen, current = st.tabs(['Debt/Equity','Margen Neto','Current ratio'])

with de:

    fig5 = px.bar(kpis['{}_kpis'.format(accion)]['Debt/Equity'][:10],text_auto=True)
    fig5.update_layout(showlegend=False)
    fig5.update_traces(textposition='outside')
    fig5.update_xaxes(dtick='M1', tickformat='%b\n%Y')

    st.plotly_chart(fig5,theme='streamlit',use_container_width=True)

with margen:

    fig6 = px.bar(kpis['{}_kpis'.format(accion)]['Net Profit Margin'][:10],text_auto=True)
    fig6.update_layout(showlegend=False)
    fig6.update_yaxes(tickformat=".2%")
    fig6.update_xaxes(dtick='M1', tickformat='%b\n%Y')

    st.plotly_chart(fig6,theme='streamlit',use_container_width=True)

with current:

    fig7 = px.bar(kpis['{}_kpis'.format(accion)]['Current Ratio'][:10],text_auto=True)
    fig7.update_layout(showlegend=False)
    fig7.update_xaxes(dtick='M1', tickformat='%b\n%Y')

    st.plotly_chart(fig7,theme='streamlit',use_container_width=True)    


################################## Noticias #################################










