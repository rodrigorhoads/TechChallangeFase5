# 🛡️ FIAP Threat Modeler IA

> **Automatizando a Modelagem de Ameaças em Arquiteturas de Nuvem usando Visão Computacional.**

![Tela do Projeto](https://github.com/rodrigorhoads/TechChallangeFase5/blob/main/tela%20do%20techchallenge.png)

---

## 💡 O Problema
A modelagem de ameaças (Threat Modeling) é uma etapa crucial de segurança em projetos Cloud, mas geralmente é um processo manual, demorado e que exige especialistas. Em metodologias ágeis, a documentação de segurança muitas vezes não acompanha a velocidade das mudanças na arquitetura.

## 🚀 A Solução
O **FIAP Threat Modeler IA** é uma prova de conceito (MVP) que utiliza Visão Computacional para ler diagramas de arquitetura (AWS, Azure, GCP), identificar componentes-chave e gerar automaticamente um relatório de vulnerabilidades e contramedidas baseado na metodologia **STRIDE**.

### ✨ Principais Funcionalidades
- **Detecção Automática:** Identifica 4 grandes grupos de componentes em imagens de arquitetura (Bancos de Dados, Servidores, Usuários e Portões de Segurança).
- **Inteligência STRIDE:** Mapeia os componentes detectados para ameaças conhecidas (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
- **Interface Amigável:** Aplicação web intuitiva construída com Streamlit, permitindo upload de imagens e ajuste dinâmico da sensibilidade da IA.
- **Geração de Contramedidas:** Sugere ações práticas de mitigação para cada ameaça detectada.

---

## 🧠 Como a IA funciona?
O modelo de Visão Computacional foi treinado utilizando o algoritmo **YOLOv8** (You Only Look Once).

As classes de detecção foram generalizadas para focar no comportamento de segurança:
1. `DATA_STORE`: Componentes que guardam dados (Ex: S3, RDS, ECR). *Foco STRIDE: Tampering & Information Disclosure.*
2. `SERVER`: Componentes de processamento (Ex: EC2, Lambda, API Gateway). *Foco STRIDE: DoS & Elevation of Privilege.*
3. `SECURITY_GATE`: Controles de acesso (Ex: WAF, Cognito). *Foco STRIDE: Tampering.*
4. `USER`: Ent
