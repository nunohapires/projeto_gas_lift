# importações necessarias 
import streamlit as st
import numpy as np
from fpdf import FPDF

st.set_page_config(
    page_title="Pojeto",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.sidebar.image('logo_nuno.jpg',)
st.sidebar.markdown(" *Desenvolvido pelo estudante de engenharia de petróleo Nuno Henrique Albuquerque Pires,[Universidade Federal de Alagoas].* ")

st.title('Projeto de Gas Lift ⚙')
st.subheader('Vamos calcular todos os passos do projeto')

st.divider()#################################################################################################################################

#calculando a pressão de injeção :
st.markdown('### Pressão de injeção ')
st.markdown('#### Temos duas equações que podem ser usadas ')
eq_press_inj = st.selectbox('Escolha a equação a ser usada :',['Completa','Reduzida'])

if eq_press_inj == 'Completa':
    #criando as colunas para melhrar o layout 
    col1 , col2 = st.columns(2)
    with col1:
        g = 9.81
        psup = st.number_input('Pressão de superficie [PSI]',value=800)
        vis_g = st.number_input('Viscosidade ',value=0.75)
    with col2:
        z = st.number_input('Qual é o fator de compressibilidade ?',value=0.9)
        h = st.number_input('Qual é a altura superficie em relação poço ?[ft]',value=7000)
    t = st.number_input('Temperatura de injeção  [F]',value=150)
    t = t + 460
    p_inj = psup*np.e**(0.018875* ((vis_g * h) / (z * t)))  
if eq_press_inj == 'Reduzida':
    psup = st.number_input('Pressão de superficie [PSI]',value=800)
    h = st.number_input('Altura superficie em relação poço [ft]',value=7000)
    p_inj = psup*(1+(h/40_000))
st.session_state['p_inj'] = p_inj
st.latex(f"P_{{\\text{{inj}}}} = {p_inj:.2f} \\text{{ PSI}}")

st.divider()#################################################################################################################################

st.markdown('### Vazão de injeção ')

with st.popover("Curva de Gilbert"):
    st.markdown("Espero ter ajudado 👋")
    st.image('curva_gilbert.png')
rgl_trb = st.number_input('Indique a RGL_trabalho [scf/stb]',value=500)
rgl_form = st.number_input('Indique a RGL_formação [scf/stb]',value=450)
qo = st.number_input('Indique a vazão de injeção [scf/day]',value=250)
q_inj = (rgl_trb - rgl_form)*qo

st.session_state['q_inj'] = q_inj
st.latex(f"Q_{{\\text{{inj}}}} = {q_inj:.1f} \\text{{ stb/day}}")

st.divider()#################################################################################################################################

st.markdown('### Dimensionamento e escolha da válvula ')
st.markdown('#### *Temos quatro opções de válvulas que podem ser usadas* ')
valvula = st.selectbox('Escolha a válvula a ser usada :', ['Orifício convencional', 'Venturi', 'Válvula de pressão'])
if valvula == 'Orifício convencional':
    st.markdown('- Método Thornhill-Craver para dimensionamento (equação aproximada)')
    c1 = 1248 # Coeficiente relativo ao sistema de unidades e condições utilizadas 4232
    cd = 0.6 # Coeficiente de descarga 0,865
    P_mont = p_inj/0.55 #𝑃𝑟𝑒𝑠𝑠ã𝑜 𝑎 𝑚𝑜𝑛𝑡𝑎𝑛𝑡𝑒 𝑑𝑎 𝑣á𝑙𝑣𝑢𝑙𝑎
    gc = 32.17 #Fator de correção devido à falta de consistência de unidades
    k = 1.256 #razão entre os calores específicos do gás (1,256)
    r = 0.55 # Razão entre as pressões absolutas a jusante e a montante da válvula. Para o GN é igual a 0,55
    dg = 0.5 #densidade do gas 
    if eq_press_inj == 'Reduzida':
        t = st.number_input('Temperatura de injeção  [F]',value=150)
    taqui = t + 460
    rais1 = np.sqrt(2*gc*(k/(k - 1)*(r**(2 / k) - r**((k+1)/k))))
    rais2 = np.sqrt(dg*taqui)
    As = q_inj/(c1*cd*P_mont*(rais1/rais2))
    Dv = 1.1284*np.sqrt(As)

    st.markdown('Utilize-o como suporte para dimensionar sua válvula.')
    with st.popover("Comparativo"):
        st.markdown("Espero ter ajudado 👋")
        st.image('val_convencional.png')

    st.session_state['A_s'] = As
    st.session_state['D_v'] = Dv
    st.latex(f"A_{{\\text{{S}}}} = {As:.3f}\\,\\text{{in}}^2")
    st.latex(f"D_{{\\text{{v}}}} = {Dv:.3f}\\,\\text{{in}}")

if valvula == 'Venturi':
    c1 = 1248 # Coeficiente relativo ao sistema de unidades e condições utilizadas 4232
    cd = 0.6 # Coeficiente de descarga 0,865
    P_mont = p_inj/0.55 #𝑃𝑟𝑒𝑠𝑠ã𝑜 𝑎 𝑚𝑜𝑛𝑡𝑎𝑛𝑡𝑒 𝑑𝑎 𝑣á𝑙𝑣𝑢𝑙𝑎
    gc = 32.17 #Fator de correção devido à falta de consistência de unidades
    k = 1.256 #razão entre os calores específicos do gás (1,256)
    r = 0.95 # Razão entre as pressões absolutas a jusante e a montante da válvula. Para o GN é igual a 0,55
    dg = 0.5 #densidade do gas 
    if eq_press_inj == 'Reduzida':
        t = st.number_input('Temperatura de injeção  [F]',value=150)
        ti = t
    ti = t
    rais1 = np.sqrt(2*gc*(k/(k - 1)*(r**(2 / k) - r**((k+1)/k))))
    rais2 = np.sqrt(dg*ti)
    As = q_inj/(c1*cd*P_mont*(rais1/rais2))
    Dv = 1.1284*np.sqrt(As)

    st.markdown('Utilize-o como suporte para dimensionar sua válvula.')
    with st.popover("Comparativo"):
        st.markdown("Espero ter ajudado 👋")
        st.image('d1_val_venturi.png')
        st.image('2d_val_venturi.png')
    st.session_state['A_s'] = As
    st.session_state['D_v'] = Dv
    st.latex(f"A_{{\\text{{S}}}} = {As:.3f}\\,\\text{{in}}^2")
    st.latex(f"D_{{\\text{{v}}}} = {Dv:.3f}\\,\\text{{in}}")

if valvula == 'Válvula de pressão':
    tipo = st.radio(
    "Qual válvula de pressão você gostaria de  usar :",
    ["IPO", "PPO"], 
    captions=["📌","📌"])
    if tipo == 'IPO':
        Ap = st.number_input('Qual é a Área da porta [IN²]',value=2)
        Ab = st.number_input('Qual é a Área do fole [IN²]',value= 1 + Ap)
        As = st.number_input('Qual é a Área da haste ou mola [IN²]',value= Ap)
        pf =st.number_input('Qual é a pressão dos fluidos produzidos [PSI]', value=600)
        pd = st.number_input('Qual é a pressão calibrada no equipamento ? [PSI] :', value=900)

        
        
        Fb = Ab/(Ab - Ap)
        Fp = Ap/(Ab - Ap)
        Fs = As/(Ab - Ap)
        s = Ab - Ap
        p_abrir_ipo = pd*Fb - pf*Fp+s

        st.latex(f"P_{{\\text{{open}}}} = {p_abrir_ipo:.2f}\\,\\text{{PSI}}")
        p_fechar_ipo = pd + s*(1 - (Ap/Ab))
        st.latex(f"P_{{\\text{{close}}}} = {p_fechar_ipo:.2f}\\,\\text{{PSI}}")

        st.session_state['P_open_ipo'] = p_abrir_ipo
        st.session_state['P_close-ipo'] = p_fechar_ipo
    if tipo == 'PPO':
        Ap = st.number_input('Qual é a Área da porta :',value=2)
        Ab = st.number_input('Qual é a Área do fole :',value= 1 + Ap)
        As = st.number_input('Qual é a Área da haste ou mola :',value= Ap)
        pf =st.number_input('Qual é a pressão dos fluidos produzidos :', value=500)
        pd = st.number_input('Qual é a pressão calibrada no equipamento ? :', value=900)

        # calculando a pressão para abrir
        
        Fb = Ab/(Ab - Ap)
        Fp = Ap/(Ab - Ap)
        Fs = As/(Ab - Ap)
        s = Ab - Ap
        p_abrir_ppo = pd*Fb-p_inj*Fp+s
        st.latex(f"P_{{\\text{{open}}}} = {p_abrir_ppo:.2f}\\,\\text{{PSI}}")
        p_fechar_ppo = pd + s*(1 - (Ap/Ab))
        st.latex(f"P_{{\\text{{close}}}} = {p_fechar_ppo:.2f}\\,\\text{{PSI}}")

        st.session_state['P_open_ppo'] = p_abrir_ppo
        st.session_state['P_close_ppo'] = p_fechar_ppo

st.divider()
##################################################################################

st.markdown('### Cálculo da pressão de saída do compressor')
col3 , col4 = st.columns(2)
with col3:
    p_inj = st.number_input('Pressão de injeção [padrão calculada anteriormente][psi]',value=2000)
    q_inj = st.number_input('Vazão de injeção [padrão calculada anteriormente] [MMsfc/d]',value= 8.6)
    p_base = st.number_input('Pressão de base - psi',value=14.7)
    n_mani = st.number_input('Numero de manifolds',value=2)
    n_poco = st.number_input('Numero de poços operando com gas lift ',value=17)
    t_valvula = st.number_input('Temperatura valvula  [F]',value=150) 

with col4 : 
    if eq_press_inj == 'Reduzida':
        z = st.number_input('Qual é o fator de compressibilidade ?',value=0.95)
        vis_g = st.number_input('Viscosidade ',value=0.75)
        t = st.number_input('Temperatura de injeção  [F]',value=90) 
        
    sf = st.number_input('Fator de segurança',value=1.1)
    Lg = st.number_input('Comprimento da linha de gás [mi]',value=4) 
    Dlg = st.number_input('Diâmetro da linha de gás [in])',value=1.75)

tm = ((t + t_valvula)/2 ) + 460
qoMM = (((q_inj) * n_poco)/n_mani)* 1000 #ajustar para Milhares
P_mont = p_inj*1.82 #livro

termo_1 = P_mont**2
termo_2 = ((qoMM*p_base)/(0.433*520))**2
termo_3 = (vis_g*tm*z*Lg)/(Dlg**(16/3))
pl = np.sqrt(termo_1 + termo_2 * termo_3)
P_saida = pl*sf

st.session_state['P_saida'] = pl
st.latex(f"P_{{\\text{{saida}}}} = {pl:.2f}\\,\\text{{PSI}}")


st.divider()
##################################################################################

st.markdown('### Cálculo do número de estágios')

psuc = st.number_input('Pressão de sucção [psi]',value=180)
n = 1
r = (P_saida/psuc)
while r > 6 :
    r = (P_saida/psuc)**(1/n)
    n += 1

st.markdown(f"R = {r:.0f}")
st.latex(f"N_{{\\text{{estágios}}}} = {n:.0f}\\,\\text{{}}")
st.session_state['N_estágios'] = n


st.divider()
##################################################################################

st.markdown('### Cálculo da potência requerida')
psup = st.number_input('Pressão de superficie [PSI]',value=180)
k = 1.256 #razão entre os calores específicos do gás (1,256)
Eo = st.number_input('Eficência ',value=0.75)
t1 = t + 460
z1 = 0.95
HPmm = (k/(k - 1))*(3.027*p_base/520)*t1*((P_saida/psup)**(z1*((k-1)/k)) - 1 )
Hpb = ((qoMM/1000)*HPmm)/Eo

st.latex(f"Potencial_{{\\text{{requerido}}}} = {HPmm:.2f}\\,\\text{{HP/MMcfd}}")
st.latex(f"Potencial_{{\\text{{total}}}} = {Hpb:.2f}\\,\\text{{hp}}")

st.session_state['Potencial_requerido'] = HPmm
st.session_state['Potencial_total'] = Hpb

st.divider()
##################################################################################

st.markdown('### Cálculo da temperatura de saída do compressor')

ng = (1_000_000/378.6)*q_inj
ng = st.number_input('número de lb-mols de gás',value=ng)
cp = st.number_input('Capacidade calorífica à pressão constante [btu/lbm-mol°F]',value=9.50 )
r_saida = (P_saida/psup)**(1/n)
t2 = t1*((r_saida)**(z1*((k - 1)/k)))
delta_H = (ng)*cp*(t2 - t1)

st.latex(f"Temperatura_{{\\text{{entrada}}}} = {t1 - 460:.2f}\\,\\text{{°F}}")
st.latex(f"Temperatura_{{\\text{{saida}}}} = {t2 - 460 :.2f}\\,\\text{{°F}}")
st.latex(f"Calor_{{\\text{{removido}}}} = {delta_H:.2f}\\,\\text{{btu/day}}")

st.session_state['Temperatuara_entrada'] = t1
st.session_state['Temperatuara_saida'] = t2
st.session_state['Calor_removido'] = delta_H

######################################################################################################################3

st.divider()

#gerando o dashboard
# Exibindo as métricas no Streamlit
st.title("Relatório de Gas Lift")

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.metric("Pressão de injeção", f"{p_inj} psi")
    st.metric("Vazão de injeção", f"{q_inj} MMsfc/d", f"{qo} sfc/d")

with c2 :
    if  valvula == 'Orifício convencional':
        st.metric("Área", f"{As} in²")
        st.metric("Diametro", f"{Dv} in")

    if  valvula == 'Venturi':
        st.metric("Área", f"{As} in²")
        st.metric("Diametro", f"{Dv} in")

    if  valvula == 'Válvula de pressão':
        if  tipo == 'IPO':
            st.metric("Pressão para Abrir IPO", f"{p_abrir_ipo:.2f} psi")
            st.metric("Pressão para Fechar IPO", f"{p_fechar_ipo:.2f} psi")

        if  tipo == 'PPO':
            st.metric("Pressão para Abrir PPO", f"{p_abrir_ppo:.2f} psi")
            st.metric("Pressão para Fechar PPO", f"{p_fechar_ppo:.2f} psi")

with c3 :
    st.metric("Pressão de saida do compressor", f"{P_saida:.2f} psi", f'{pl:.2f} sem Sfc')
    st.metric("Número de estágios", f"{n:.2f} ",f'{r:.2f} valor de r ')

with c4 :
    st.metric("Potencial_requerido", f"{HPmm:.2f} HP/MMcfd")
    st.metric("Potencial_total", f"{Hpb:.2f} Hp")

with c5 :
    st.metric("Temperatuara_saida", f"{t2:.2f} °F", f"{t1:.2f} entrada °F" )
    st.metric("Calor_removido", f"{delta_H:.2f} btu/day")


# Função para gerar PDF
def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Times", "B", 16)
    pdf.cell(200, 10, txt="Relatório de Gas Lift", ln=True, align='C')

    pdf.ln(10)
    
    # Métricas
    pdf.set_font("Times", size=12)

    # Pressão e Vazão
    pdf.cell(100, 10, txt=f"Pressão de injeção: {p_inj} psi", ln=True)
    pdf.cell(100, 10, txt=f"Vazão de injeção: {q_inj} MMsfc/d", ln=True)
    pdf.cell(100, 10, txt=f"Vazão de óleo: {qo} sfc/d", ln=True)

    pdf.ln(5)
    
    # Detalhes da Válvula
    if valvula in ['Orifício convencional', 'Venturi']:
        pdf.cell(100, 10, txt=f"Área: {As} in²", ln=True)
        pdf.cell(100, 10, txt=f"Diâmetro: {Dv} in", ln=True)
    elif valvula == 'Válvula de pressão':
        if tipo == 'IPO':
            pdf.cell(100, 10, txt=f"Pressão para Abrir IPO: {p_abrir_ipo:.2f} psi", ln=True)
            pdf.cell(100, 10, txt=f"Pressão para Fechar IPO: {p_fechar_ipo:.2f} psi", ln=True)
        elif tipo == 'PPO':
            pdf.cell(100, 10, txt=f"Pressão para Abrir PPO: {p_abrir_ppo:.2f} psi", ln=True)
            pdf.cell(100, 10, txt=f"Pressão para Fechar PPO: {p_fechar_ppo:.2f} psi", ln=True)

    pdf.ln(5)
    
    # Compressor
    pdf.cell(100, 10, txt=f"Pressão de saída do compressor: {P_saida:.2f} psi", ln=True)
    pdf.cell(100, 10, txt=f"Número de estágios: {n:.2f}", ln=True)
    
    pdf.ln(5)
    
    # Potenciais
    pdf.cell(100, 10, txt=f"Potencial requerido: {HPmm:.2f} HP/MMcfd", ln=True)
    pdf.cell(100, 10, txt=f"Potencial total: {Hpb:.2f} Hp", ln=True)

    pdf.ln(5)
    
    # Temperatura e Calor
    pdf.cell(100, 10, txt=f"Temperatura de saída: {t2:.2f} °F", ln=True)
    pdf.cell(100, 10, txt=f"Temperatura de entrada: {t1:.2f} °F", ln=True)
    pdf.cell(100, 10, txt=f"Calor removido: {delta_H:.2f} btu/day", ln=True)

    # Assinatura
    pdf.ln(20)
    pdf.set_font("Times", "I", 12)
    pdf.cell(200, 10, txt="_______________________________", ln=True, align='C')
    pdf.cell(200, 10, txt="Nuno Henrique Albuquerque Pires", ln=True, align='C')

    return pdf.output(dest='S').encode('latin1')  # Retorna o PDF como um byte stream

# Botão para download do PDF
if st.button("Gerar PDF"):
    pdf = gerar_pdf()
    
    st.download_button(label="Baixar PDF", 
                       data=pdf, 
                       file_name="relatorio_gas_lift.pdf", 
                       mime="application/pdf")








