import streamlit as st
from ultralytics import YOLO
from collections import Counter
from PIL import Image
import cv2
import numpy as np

# ==========================================
# 1. BASE DE CONHECIMENTO STRIDE
# ==========================================
STRIDE_DB = {
    "DATA_STORE": {
        "descricao": "Armazenamento de Dados",
        "ameacas": [
            "**[T] Tampering (Violação):** Alteração maliciosa de dados.",
            "**[I] Information Disclosure:** Acesso não autorizado a dados sensíveis."
        ],
        "contramedidas": [
            "Implementar criptografia em repouso (ex: AWS KMS).",
            "Configurar controles de acesso rigorosos e backups automatizados."
        ]
    },
    "SERVER": {
        "descricao": "Processamento e Roteamento",
        "ameacas": [
            "**[D] Denial of Service (DoS):** Sobrecarga do serviço.",
            "**[E] Elevation of Privilege:** Atacante ganhando permissões de admin."
        ],
        "contramedidas": [
            "Implementar Rate Limiting e Auto Scaling.",
            "Aplicar o princípio de Least Privilege nas roles de execução."
        ]
    },
    "USER": {
        "descricao": "Entidades de Usuário/Cliente",
        "ameacas": [
            "**[S] Spoofing:** Atacante se passando por um usuário legítimo."
        ],
        "contramedidas": [
            "Exigir Autenticação Multifator (MFA).",
            "Utilizar tokens de sessão com tempo de expiração curto."
        ]
    },
    "SECURITY_GATE": {
        "descricao": "Controles de Segurança",
        "ameacas": [
            "**[T] Tampering:** Modificação indevida das regras de firewall."
        ],
        "contramedidas": [
            "Restringir acesso às configurações apenas para admins master.",
            "Monitorar alterações usando CloudTrail ou equivalente."
        ]
    }
}

# ==========================================
# 2. CONFIGURAÇÃO DA PÁGINA E MODELO
# ==========================================
st.set_page_config(page_title="Detector de Ameaças IA", page_icon="🛡️", layout="centered")


# O cache evita que o modelo seja recarregado toda vez que você clica num botão
@st.cache_resource
def carregar_modelo():
    return YOLO('best.pt')


try:
    model = carregar_modelo()
except Exception as e:
    st.error("⚠️ Erro: Arquivo 'best.pt' não encontrado na pasta. Coloque o modelo aqui para continuar.")
    st.stop()

# ==========================================
# 3. INTERFACE VISUAL
# ==========================================
st.title("Detector de Ameaças")
st.markdown("Faça o upload de um diagrama de arquitetura para análise automática baseada na metodologia STRIDE.")

# Controle de Confiança (Slider)
confianca = st.slider(
    "Ajuste a sensibilidade da IA (Confiança):",
    min_value=0.05,
    max_value=0.90,
    value=0.25,  # Começamos com 25% para ele achar mais itens
    step=0.05,
    help="Diminua se a IA não estiver achando os ícones. Aumente se estiver marcando coisas erradas."
)

# Botão de Upload
arquivo_upload = st.file_uploader("Selecione a imagem do diagrama (JPG/PNG)", type=["jpg", "jpeg", "png"])

if arquivo_upload is not None:
    # Mostra a imagem original
    imagem_pil = Image.open(arquivo_upload).convert("RGB")  # Força o padrão RGB

    col1, col2 = st.columns(2)
    with col1:
        st.image(imagem_pil, caption="Arquitetura Original", use_container_width=True)

    if st.button("🔍 Analisar Ameaças", type="primary"):
        with st.spinner("A IA está analisando os componentes..."):

            # TRUQUE: Salvar a imagem temporariamente garante que o YOLO leia EXATAMENTE
            # igual ao terminal, resolvendo o problema de detecções sumindo.
            caminho_temp = "temp_diagrama.jpg"
            imagem_pil.save(caminho_temp)

            # Faz a detecção usando o arquivo salvo e a confiança do slider
            resultados = model.predict(caminho_temp, conf=confianca)

            # Pega a imagem com os quadrados desenhados
            img_anotada = resultados[0].plot()
            img_anotada_rgb = cv2.cvtColor(img_anotada, cv2.COLOR_BGR2RGB)

            with col2:
                st.image(img_anotada_rgb, caption="Componentes Detectados", use_container_width=True)

            # Limpa a imagem temporária (opcional, mas uma boa prática)
            import os

            if os.path.exists(caminho_temp):
                os.remove(caminho_temp)

            # ==========================================
            # 4. GERAÇÃO DO RELATÓRIO NA TELA
            # ==========================================
            st.divider()
            st.subheader("📋 Relatório STRIDE de Vulnerabilidades")

            nomes_classes = model.names
            classes_detectadas = [nomes_classes[int(box.cls[0])] for box in resultados[0].boxes]
            contagem = Counter(classes_detectadas)

            if not contagem:
                st.warning("Nenhum componente reconhecido. Tente diminuir a sensibilidade na barra acima.")
            else:
                st.success(f"Foram identificados {len(classes_detectadas)} componentes na arquitetura.")

                # Exibe o relatório
                for classe, qtd in contagem.items():
                    classe_upper = str(classe).upper()
                    if classe_upper in STRIDE_DB:
                        dados = STRIDE_DB[classe_upper]
                        with st.expander(f"🔴 {qtd}x {classe_upper} ({dados['descricao']})", expanded=True):
                            st.markdown("##### ⚠️ Possíveis Ameaças:")
                            for ameaca in dados['ameacas']:
                                st.markdown(f"- {ameaca}")
                            st.markdown("##### 🛡️ Contramedidas Recomendadas:")
                            for contramedida in dados['contramedidas']:
                                st.markdown(f"- {contramedida}")