# 🌊 Wave Model Core (English Version)

## 📌 Overview
The **CreateBeachProfileService** module is a core tool for analyzing and visualizing ocean wave breaking points.  
It processes bathymetric profile data and wave conditions to:
- Calculate breaking depths
- Identify exact points on the profiles
- Generate visual representations  

Designed to integrate into a larger numerical model, it aims for **efficiency** and **clarity** in coastal oceanographic analysis.

---

## 🚀 Key Features

- **Data Ingestion:**  
  Downloads beach profile data and wave conditions from remote storage (e.g., MinIO, GCS).

- **Profile Preparation:**  
  Transforms and normalizes raw bathymetric data for analysis.

- **Wave Breaking Calculation:**  
  Computes breaking depth for various wave heights using specific oceanographic methods (e.g., Miche’s criterion).

- **Identification and Visualization:**  
  Locates the breaking point on the beach profile and generates detailed 2D plots, highlighting the breaking point and water/land regions.

- **Output Management:**  
  Stores the generated images back in remote storage and manages local temporary files.

---

## 🔄 Processing Structure and Workflow

The module orchestrates a workflow that involves:

1. **Downloading and reading** CSV files containing beach profiles and wave data.  
2. **Transforming and cleaning** raw data.  
3. **Calculating** breaking depths for each provided condition.  
4. **Iterative processing** of each profile with each calculated wave condition.  
5. **Defining** the breaking point.  
6. **Plotting** the profile and breaking point on a graph.  
7. **Uploading** the resulting image to cloud storage.  
8. **Cleaning up** temporary files.

---

## 📦 Essential Dependencies

This module requires the following libraries and services:

- **pandas:** For tabular data manipulation.  
- **matplotlib:** For graph generation.  
- **os:** For file system operations.  
- **modules.storage.storage_service:** A custom service for interacting with remote storage solutions (MinIO, Google Cloud Storage).  
- **modules.wave.services.calculate_wave_break_service:** A custom service encapsulating the wave breaking calculation logic.

<br>
<br>
<br>
<br>
<br>

# 🌊 Wave Model Core (Versão PT-BR)

## 📌 Visão Geral
O módulo **CreateBeachProfileService** é uma ferramenta central para a análise e visualização de pontos de quebra de ondas oceânicas.  
Ele processa dados de perfis batimétricos e condições de onda para:
- Calcular profundidades de quebra
- Identificar pontos exatos nos perfis
- Gerar representações visuais  

Projetado para integrar um modelo numérico maior, busca **eficiência** e **clareza** na análise oceanográfica costeira.

---

## 🚀 Funcionalidades Principais

- **Ingestão de Dados:**  
  Baixa dados de perfis de praia e condições de onda de armazenamento remoto (MinIO).

- **Preparação de Perfis:**  
  Transforma e normaliza dados batimétricos brutos para análise.

- **Cálculo de Quebra de Ondas:**  
  Computa a profundidade de quebra para diversas alturas de onda, utilizando métodos oceanográficos específicos (e.g., critério de Miche).

- **Identificação e Visualização:**  
  Localiza o ponto de quebra no perfil da praia e gera gráficos 2D detalhados, destacando esse ponto e as regiões de água/terra.

- **Gerenciamento de Saída:**  
  Armazena as imagens geradas de volta no armazenamento remoto e gerencia arquivos temporários locais.

---

## 🔄 Estrutura e Fluxo de Processamento

O módulo orquestra um fluxo de trabalho que envolve:

1. **Download e leitura** de arquivos CSV de perfil de praia e dados de onda.  
2. **Transformação e limpeza** dos dados brutos.  
3. **Cálculo** das profundidades de quebra de onda para cada condição fornecida.  
4. **Processamento iterativo** de cada perfil com cada condição de onda calculada.  
5. **Definição do ponto de quebra.**  
6. **Plotagem** do perfil e do ponto de quebra em um gráfico.  
7. **Upload** da imagem resultante para o armazenamento em nuvem.  
8. **Limpeza** dos arquivos temporários.

---

## 📦 Dependências Essenciais

Este módulo requer as seguintes bibliotecas e serviços:

- **pandas:** Manipulação de dados tabulares.  
- **matplotlib:** Geração de gráficos.  
- **os:** Operações de sistema de arquivos.  
- **modules.storage.storage_service:** Serviço customizado para interação com soluções de armazenamento remoto (MinIO).  
- **modules.wave.services.calculate_wave_break_service:** Serviço customizado que encapsula a lógica de cálculo de quebra de ondas.
