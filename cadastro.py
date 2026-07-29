#import
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# 1. Montamos as credenciais pegando cada pedacinho seguro do st.secrets
credenciais_dict = {
    "type": st.secrets["google_credentials"]["type"],
    "project_id": st.secrets["google_credentials"]["project_id"],
    "private_key_id": st.secrets["google_credentials"]["private_key_id"],
    "private_key": st.secrets["google_credentials"]["private_key"].replace(
        "\\n", "\n"
    ),  # Garante que o Python converta o texto '\n' em quebra de linha real
    "client_email": st.secrets["google_credentials"]["client_email"],
    "client_id": st.secrets["google_credentials"]["client_id"],
    "auth_uri": st.secrets["google_credentials"]["auth_uri"],
    "token_uri": st.secrets["google_credentials"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google_credentials"][
        "auth_provider_x509_cert_url"
    ],
    "client_x509_cert_url": st.secrets["google_credentials"][
        "client_x509_cert_url"
    ],
}

# 2. Definimos o escopo necessário para o Google Sheets e Drive
escopos = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# 3. Geramos o crachá oficial usando o dicionário tratado
creds = Credentials.from_service_account_info(
    credenciais_dict, scopes=escopos
)

# 4. Conectamos com o gspread de forma blindada
conta = gspread.authorize(creds)
planilha = conta.open("PLANILHA DE ASSOCIADOS")
associados = planilha.worksheet("Associados")
mirim = planilha.worksheet("Mirim")

st.markdown(
    '<meta name="google" content="notranslate">', 
    unsafe_allow_html=True
)

if "etapa" not in st.session_state:
    st.session_state.etapa = 1

if st.session_state.etapa == 1:
    #titulo
    st.title("Cadastro Associado Mãe do Infinito Amor")

    #cadastar associado mirim
    if st.button("**Cadastrar um Associado Mirim**", type="primary", use_container_width=True):
        st.session_state.etapa = 4
        st.rerun()

    #Nome
    st.subheader("Nome do Associado")
    nome=st.text_input("Digite o nome completo do associado:")

    if nome:
        st.success(f"Confirmar Nome: {nome.upper()}")

    #cpf
    st.subheader("CPF do Associado")
    cpf_cru=st.text_input("Digite o CPF (Apenas números):", max_chars=11)
    if len(cpf_cru) == 11:
        cpf_formatado = f"{cpf_cru[:3]}.{cpf_cru[3:6]}.{cpf_cru[6:9]}-{cpf_cru[9:]}"
        soma_1 = sum(int(cpf_cru[i]) * (10 - i) for i in range(9))
        digito_1 = 11 - (soma_1 % 11)
        digito_1 = 0 if digito_1 > 9 else digito_1

        soma_2 = sum(int(cpf_cru[i]) * (11 - i) for i in range(10))
        digito_2 = 11 - (soma_2 % 11)
        digito_2 = 0 if digito_2 > 9 else digito_2

        if int(cpf_cru[9]) == digito_1 and int(cpf_cru[10]) == digito_2:
            st.success(f"CPF Válido: {cpf_formatado}")
        else:
            st.error("CPF Inválido. Por favor, verifique os números digitados.")
    elif len(cpf_cru) > 0:
        st.warning("Continue digitando... O CPF precisa ter 11 números.")

    #data de nascimento
    st.subheader("Data de Nascimento do Associado")
    coldata1, coldata2, coldata3 = st.columns([1, 4, 2])
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    with coldata1:
        dia = st.selectbox("Dia", [f"{i:02d}" for i in range(1, 32)], index=None)
    with coldata2:
        mes = st.selectbox("Mês", meses, index=None)
    with coldata3:
        ano = st.text_input("Ano", max_chars=4)

    if dia and mes and ano:
        data_nascimento = f"{dia}/{meses.index(mes)+1:02d}/{ano}"
        st.success(f"Confirme a Data de Nascimento: {data_nascimento}")

    #telefone
    st.subheader("Telefone do Associado")
    coltel1, coltel2, coltel3 = st.columns([2, 1, 6])

    with coltel1:
        ddi = st.selectbox("DDI", ["Alemanha: +49", "Argentina: +54", "Austrália: +61", "Bolívia: +591", "Brasil: +55", "Canadá: +1", "Chile: +56", "China: +86", "Colômbia: +57", "Espanha: +34", "Estados Unidos: +1", "França: +33", "Itália: +39", "Japão: +81", "México: +52", "Paraguai: +595", "Peru: +51", "Portugal: +351", "Reino Unido: +44", "Uruguai: +598"], index=None)
    with coltel2:
        ddd = st.text_input("DDD")
    with coltel3:
        telefone = st.text_input("Telefone (Apenas números):", max_chars=9)

    if ddi and ddd and telefone:
        telefone=str(f"{ddi.split(': ')[1]} ({ddd}) {telefone}")
        st.success(f"Confirme o telefone: {telefone}")

    #email
    st.subheader("Email do Associado")
    email=st.text_input("Digite o email do associado: (não é obrigatório)")

    if email:
        st.success(f"Confirme o email: {email.lower()}")

    #endereço
    st.subheader("Endereço do Associado")
    collogradouro, colnumero,= st.columns([4, 2])
    with collogradouro:
        logradouro=st.text_input("Digite o logradouro (Rua, Avenida, Travessa, etc):")
    with colnumero:
        numero=st.text_input("Digite o número da residência:")
    colcomplemento, colbairro, colcidade = st.columns([3, 4, 4])
    with colcomplemento:
        complemento=st.text_input("Digite o complemento:")
    with colbairro:
        bairro=st.text_input("Digite o bairro:")
    with colcidade:
        cidade=st.text_input("Digite a cidade:")
    colestado, colpais, colcep = st.columns([2, 2, 2])
    with colestado:
        estado=st.text_input("Digite o estado: (Exemplo: RJ):", max_chars=2)
    with colpais:
        pais=st.text_input("Digite o país: (Exemplo: Brasil):")
    with colcep:
        cep=st.text_input("Digite o CEP (Apenas números):", max_chars=8)

    if logradouro and numero and complemento and bairro and cidade and estado and pais and cep:
        endereco = f"{logradouro}, {numero}, {complemento}, {bairro}, {cidade}-{estado}, {pais}, CEP: {cep}"
        st.success(f"Confirme o endereço: {endereco.upper()}")

    #valor da mensalidade
    st.subheader("Valor da contribuição mensal do Associado")
    valor=st.number_input("Digite o valor da contribuição mensal:", min_value=0.0, format="%.2f", step=1.0)

    if valor:
        st.success(f"Confirme o valor da mensalidade: R$ {valor:.2f}")

    #data para pagamento
    st.subheader("Data para pagamento da contribuição mensal do Associado")
    data_pg=st.selectbox("Selecione a melhor data para fazer sua doação mensal:", ["05° dia do mês", "10° dia do mês", "15° dia do mês", "20° dia do mês", "25° dia do mês"], index=None)

    if data_pg:
        data_pagamento = data_pg[:2]
        st.success(f"Confirme a data de pagamento: {data_pagamento}° dia de cada mês")

    #forma de pagamento
    st.subheader("Forma de pagamento da contribuição mensal do Associado")
    forma_pagamento=st.selectbox("Selecione a forma de pagamento:", ["Boleto Bancário", "Pix"], index=None)

    if forma_pagamento:
        st.success(f"Confirme a forma de pagamento: {forma_pagamento}")

    #botão para avançar
    if st.button(
        "**Avançar**",
        disabled=not (nome and len(cpf_cru) == 11 and dia and mes and ano and ddi and ddd and telefone and logradouro and numero and complemento and bairro and cidade and estado and pais and cep and valor > 0.0 and data_pg and forma_pagamento),
        type="primary",
        use_container_width=True
        ):
        st.session_state.nome = nome.upper()
        st.session_state.cpf = cpf_formatado
        st.session_state.data_nascimento = data_nascimento
        st.session_state.telefone = telefone
        st.session_state.email = email.lower()
        st.session_state.endereco = endereco.upper()   
        st.session_state.valor = valor
        st.session_state.data_pagamento = data_pagamento.upper()
        st.session_state.forma_pagamento = forma_pagamento.upper()
        st.session_state.etapa = 2
        st.rerun()

elif st.session_state.etapa == 2:
    st.title("Confirmação de Dados do Associado")
    st.subheader("Por favor, confirme os dados informados:")
    st.write(f"**Nome:** {st.session_state.nome}")
    st.write(f"**CPF:** {st.session_state.cpf}")
    st.write(f"**Data de Nascimento:** {st.session_state.data_nascimento}")
    st.write(f"**Telefone:** {st.session_state.telefone}")
    st.write(f"**Email:** {st.session_state.email}")
    st.write(f"**Endereço:** {st.session_state.endereco}")
    st.write(f"**Valor da Mensalidade:** R$ {st.session_state.valor:.2f}")
    st.write(f"**Data de Pagamento:** {st.session_state.data_pagamento}° dia do mês")
    st.write(f"**Forma de Pagamento:** {st.session_state.forma_pagamento}")

    colvoltar, colassociar=st.columns([1, 3])
    with colvoltar:
        if st.button("Voltar para corrigir", use_container_width=True):
            st.session_state.etapa=1
            st.rerun
    with colassociar:
        if st.button("**Me tornar um Associado**", type="primary", use_container_width=True):
            novo_associado = [st.session_state.nome, st.session_state.cpf, st.session_state.data_nascimento, st.session_state.telefone, st.session_state.email, st.session_state.endereco, st.session_state.valor, st.session_state.data_pagamento, st.session_state.forma_pagamento]
            associados.append_row(novo_associado)
            st.session_state.etapa=3

elif st.session_state.etapa == 3:
    st.title(f"Parabéns {st.session_state.nome}🎉. Você acaba de se tornar um Associado da Mãe do Infinito Amor")

elif st.session_state.etapa == 4:
    #titulo
    st.title("Cadastro Associado Mirim")

    #cadastar associado adulto
    if st.button("**Cadastrar um Associado Mãe do Infinito Amor**", type="primary", use_container_width=True):
        st.session_state.etapa = 1
        st.rerun()
    #Nome
    st.subheader("Nome do Associado Mirim")
    nome=st.text_input("Digite o nome completo do associado:")

    if nome:
        st.success(f"Confirmar Nome: {nome.upper()}")

    #cpf
    st.subheader("CPF do Associado Mirim")
    cpf_cru=st.text_input("Digite o CPF (Apenas números):", max_chars=11)
    if len(cpf_cru) == 11:
        cpf_formatado = f"{cpf_cru[:3]}.{cpf_cru[3:6]}.{cpf_cru[6:9]}-{cpf_cru[9:]}"
        soma_1 = sum(int(cpf_cru[i]) * (10 - i) for i in range(9))
        digito_1 = 11 - (soma_1 % 11)
        digito_1 = 0 if digito_1 > 9 else digito_1

        soma_2 = sum(int(cpf_cru[i]) * (11 - i) for i in range(10))
        digito_2 = 11 - (soma_2 % 11)
        digito_2 = 0 if digito_2 > 9 else digito_2

        if int(cpf_cru[9]) == digito_1 and int(cpf_cru[10]) == digito_2:
            st.success(f"CPF Válido: {cpf_formatado}")
        else:
            st.error("CPF Inválido. Por favor, verifique os números digitados.")
    elif len(cpf_cru) > 0:
        st.warning("Continue digitando... O CPF precisa ter 11 números.")

    #data de nascimento
    st.subheader("Data de Nascimento do Associado Mirim")
    coldata1, coldata2, coldata3 = st.columns([1, 4, 2])
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    with coldata1:
        dia = st.selectbox("Dia", [f"{i:02d}" for i in range(1, 32)], index=None)
    with coldata2:
        mes = st.selectbox("Mês", meses, index=None)
    with coldata3:
        ano = st.text_input("Ano", max_chars=4)

    if dia and mes and ano:
        data_nascimento = f"{dia}/{meses.index(mes)+1:02d}/{ano}"
        st.success(f"Confirme a Data de Nascimento: {data_nascimento}")

    #Nome do responsavel
    st.subheader("Nome do Responsável")
    nome_resp=st.text_input("Digite o nome completo do responsável:")

    if nome_resp:
        st.success(f"Confirmar Nome: {nome_resp.upper()}")

    #cpf responsável
    st.subheader("CPF do Responsável")
    cpf_cru_res=st.text_input("Digite o CPF (Apenas números):", max_chars=11, key="cpf_responsavel")
    if len(cpf_cru_res) == 11:
        cpf_formatado_res = f"{cpf_cru_res[:3]}.{cpf_cru_res[3:6]}.{cpf_cru_res[6:9]}-{cpf_cru_res[9:]}"
        soma_1 = sum(int(cpf_cru_res[i]) * (10 - i) for i in range(9))
        digito_1 = 11 - (soma_1 % 11)
        digito_1 = 0 if digito_1 > 9 else digito_1

        soma_2 = sum(int(cpf_cru_res[i]) * (11 - i) for i in range(10))
        digito_2 = 11 - (soma_2 % 11)
        digito_2 = 0 if digito_2 > 9 else digito_2

        if int(cpf_cru_res[9]) == digito_1 and int(cpf_cru_res[10]) == digito_2:
            st.success(f"CPF Válido: {cpf_formatado_res}")
        else:
            st.error("CPF Inválido. Por favor, verifique os números digitados.")
    elif len(cpf_cru_res) > 0:
        st.warning("Continue digitando... O CPF precisa ter 11 números.")

    #telefone
    st.subheader("Telefone para contato")
    coltel1, coltel2, coltel3 = st.columns([2, 1, 6])

    with coltel1:
        ddi = st.selectbox("DDI", ["Alemanha: +49", "Argentina: +54", "Austrália: +61", "Bolívia: +591", "Brasil: +55", "Canadá: +1", "Chile: +56", "China: +86", "Colômbia: +57", "Espanha: +34", "Estados Unidos: +1", "França: +33", "Itália: +39", "Japão: +81", "México: +52", "Paraguai: +595", "Peru: +51", "Portugal: +351", "Reino Unido: +44", "Uruguai: +598"], index=None)
    with coltel2:
        ddd = st.text_input("DDD")
    with coltel3:
        telefone = st.text_input("Telefone (Apenas números):", max_chars=9)

    if ddi and ddd and telefone:
        telefone=str(f"{ddi.split(': ')[1]} ({ddd}) {telefone}")
        st.success(f"Confirme o telefone: {telefone}")

    #email
    st.subheader("Email para contato")
    email=st.text_input("Digite o email: (não é obrigatório)")

    if email:
        st.success(f"Confirme o email: {email.lower()}")

    #endereço
    st.subheader("Endereço")
    collogradouro, colnumero,= st.columns([4, 2])
    with collogradouro:
        logradouro=st.text_input("Digite o logradouro (Rua, Avenida, Travessa, etc):")
    with colnumero:
        numero=st.text_input("Digite o número da residência:")
    colcomplemento, colbairro, colcidade = st.columns([3, 4, 4])
    with colcomplemento:
        complemento=st.text_input("Digite o complemento:")
    with colbairro:
        bairro=st.text_input("Digite o bairro:")
    with colcidade:
        cidade=st.text_input("Digite a cidade:")
    colestado, colpais, colcep = st.columns([2, 2, 2])
    with colestado:
        estado=st.text_input("Digite o estado: (Exemplo: RJ):", max_chars=2)
    with colpais:
        pais=st.text_input("Digite o país: (Exemplo: Brasil):")
    with colcep:
        cep=st.text_input("Digite o CEP (Apenas números):", max_chars=8)

    if logradouro and numero and complemento and bairro and cidade and estado and pais and cep:
        endereco = f"{logradouro}, {numero}, {complemento}, {bairro}, {cidade}-{estado}, {pais}, CEP: {cep}"
        st.success(f"Confirme o endereço: {endereco.upper()}")

    #botão avançar
    if st.button(
            "**Avançar**",
            disabled=not (nome and len(cpf_cru)==11 and dia and mes and ano and nome_resp and len(cpf_cru_res)==11 and ddi and ddd and telefone and logradouro and numero and complemento and bairro and cidade and estado and pais and cep),
            type="primary",
            use_container_width=True
    ):
        st.session_state.nome = nome.upper()
        st.session_state.cpf = cpf_formatado
        st.session_state.data_nascimento = data_nascimento
        st.session_state.nome_resp = nome_resp.upper()
        st.session_state.cpf_res = cpf_formatado_res
        st.session_state.telefone = telefone
        st.session_state.email = email.lower()
        st.session_state.endereco = endereco.upper()
        st.session_state.etapa=5
        st.rerun()

elif st.session_state.etapa == 5:
    st.title("Confirmação de Dados do Associado Mirim")
    st.subheader("Por favor, confirme os dados informados:")
    st.write(f"**Nome:** {st.session_state.nome}")
    st.write(f"**CPF:** {st.session_state.cpf}")
    st.write(f"**Data de Nascimento:** {st.session_state.data_nascimento}")
    st.write(f"**Nome do Responsável: {st.session_state.nome_resp}")
    st.write(f"CPF do Responsável: {st.session_state.cpf_res}")
    st.write(f"**Telefone:** {st.session_state.telefone}")
    st.write(f"**Email:** {st.session_state.email}")
    st.write(f"**Endereço:** {st.session_state.endereco}")

    colvoltar, colassociar=st.columns([1, 3])
    with colvoltar:
        if st.button("Voltar para corrigir", use_container_width=True):
            st.session_state.etapa=4
            st.rerun()
    with colassociar:
        if st.button("**Me tornar um Associado Mirim**", type="primary", use_container_width=True):
            novo_associado = [st.session_state.nome, st.session_state.cpf, st.session_state.data_nascimento, st.session_state.nome_resp, st.session_state.cpf_res, st.session_state.telefone, st.session_state.email, st.session_state.endereco]
            mirim.append_row(novo_associado)
            st.session_state.etapa=3


    



