<h1 align='center'>
 <b>PROYECTO INDIVIDUAL Nº2 DE HENRY BOOTCAMP </b>
</h1>
 
# <h1 align="center">**`Mercado bursátil`**</h1>

## **Descripción del proyecto**

El objetivo de este proyecto es obtener recomendaciones de inversión en las bolsas de Estados Unidos en las empresas
que estan incluidas en el indice bursatil Standard & Poors 500(SP500) y simular el comportamiento de un portafolio de inversión.

Para desarrollar el proyecto se realizó un analisis de datos a la información historica de los últimos 23 años SP500,los precios historicos de los últimos 5 años de ETFs que siguen el movimiento de los sectores del indice y de las empresas que lo conforman. Para finalmente seleccionar las acciones recomendadas, utilizando el ratio de Sharpe como criterio de selección.

Por último, estas acciones se utilizan en un dashboard,desarrollado con Streamlit,para hacer simular de 3 tipos de portafolios y observar algunas metricas de su performance, riesgo e información de cada componente.

## **Archivos del repositorio**

### **Librerias necesarias**
En el archivo `requirements.txt` se encuentran las librerias necesarias para la ejecucion del proyecto.

Se intala desde la consola de forma recursiva con:
'''bash
    pip install -r requirements.txt
'''

### **Análisis Exploratorio de los datos**(_Exploratory Data Analysis = EDA_)
En el notebook de jupyter `EDA.ipynb ` se necuentra el analisis de los rendimientos del indice S&P500, asi como el analisis por sector y la selección de acciones para invertir.
  
### **Dashboard en streamlit**
En `main.py` corre el dashboard de simulación de portafolios, que se encuentra publicado en el siguiente [link]().

1. Una vez instaladas las librerias necesarias ejecuta el comando:
'''bash
    streamlit run main.py
''' 
2. El dashboard se desplegara localmente en la direccion http://localhost:8501 

NOTA: Se recomienda el uso de un entorno virtual en python para ejecutar el proyecto. Mas información en la documentación de python, en el siguiente [link](https://docs.python.org/es/3/library/venv.html) 

---  
## Fuentes de datos:

- Libreria [yfinance](https://pypi.org/project/yfinance/) 

- [Listade acciones del índice SP500](https://www.google.com/url?q=https://en.wikipedia.org/wiki/List_of_S%2526P_500_companies&sa=D&source=docs&ust=1676566032938438&usg=AOvVaw3J6gZYtEH8xJABTCf0pYqO)

- [ETFs de cada sector del S&P500](https://www.etf.com/sections/etf-strategist-corner/sector-sector-sp-500)

- [Stockrow](https://stockrow.com/) para datos fundamentales de las empresas

---
## Descargo de responsabilidad
La información de este proyecto no constituye una recomendación de inversión. El proyecto se realizó solo con fines académicos
  
---
## Propuestas futuras para el proyecto

- Mejorar la funcionalidad del boton de agregar nuevas acciones al portafolio
- Crear un indicador de sentimeinto de mercado con NPL, extrayendo información de noticias y redes sociales, para mejorar la toma de decisiones
- Agregar una nueva pagina al dashboard para visualizar mas a fondo la información cualitativa y cuantitativa de cada empresa
