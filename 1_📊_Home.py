#importações necessarias  
import streamlit as st 

#configurações da pagina 
st.set_page_config(
    layout="wide",
    page_title="Projeto Gas Lift",
    initial_sidebar_state="expanded",
    page_icon="📊",
)

st.markdown("# Projeto Gas Lift! ⚙🛢") 
st.sidebar.image('logo_nuno.jpg',)
st.sidebar.markdown(" *Desenvolvido pelo estudante de engenharia de petróleo Nuno Henrique Albuquerque Pires,[Universidade Federal de Alagoas].* ")

with st.expander("Informações Adicionais"):
    st.markdown('- Esse web app foi feito para projetar o uso do gás lift .')
    st.markdown('- Esse web app foi desenvolvido com base nas equações do livro Petroleum Production Engineering Second Edition .')
    st.markdown('- Referência : Guo, Boyun, Xinghui Liu, e Xuehao Tan. Petroleum Production Engineering. 2ª ed., Gulf Professional Publishing, 2017.')


st.markdown(
    """
    O trabalho a ser realizado envolve o desenvolvimento de um projeto de gas lift utilizando Python, 
    com o objetivo de modelar e automatizar todo o processo, 
    desde a determinação da pressão de injeção até a seleção de válvulas e a parte de compressão. 
    O uso de Python permitirá criar um fluxo de trabalho eficiente e customizável, 
    integrando cálculos complexos e permitindo análises detalhadas e precisas. 
    Este projeto visa não apenas otimizar o processo de gas lift, 
    mas também fornecer uma ferramenta poderosa para tomada de decisões em operações de produção de petróleo.
"""
)




