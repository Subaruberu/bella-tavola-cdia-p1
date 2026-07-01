# Bella Tavola — API de Restaurante com Pipeline de ML e Infraestrutura MLOps

**Projeto de curso — Ciência de Dados e Inteligência Artificial, PUC-SP**

## Visão geral

Bella Tavola é uma API para um sistema de restaurante construída para demonstrar, de ponta a ponta, o ciclo de vida de um produto de dados: da API de negócio ao pipeline de machine learning, passando por containerização e automação de deploy.

## Arquitetura

- **API**: FastAPI, expondo endpoints REST para o domínio do restaurante (cardápio, pedidos, recomendações)
- **Pipeline de ML**: modelo integrado à API para tarefas preditivas/recomendação, com pipeline de treino e inferência separados da camada de serviço
- **Containerização**: Docker, isolando dependências e garantindo paridade entre ambiente de desenvolvimento e produção
- **CI/CD**: GitHub Actions automatizando testes e build a cada push, reduzindo fricção entre desenvolvimento e deploy

## Decisões técnicas relevantes

- Separação clara entre lógica de negócio (API) e lógica de modelo (pipeline de ML), permitindo evoluir cada camada de forma independente
- Uso de FastAPI pela tipagem nativa (Pydantic) e geração automática de documentação OpenAPI, reduzindo a distância entre código e contrato de API
- Pipeline de CI/CD pensado desde o início do projeto, não como adição posterior — refletindo prática de MLOps real de mercado

## Stack técnica

Python · FastAPI · Docker · GitHub Actions · Pydantic · (modelo de ML conforme pipeline do projeto)

## Principais competências demonstradas

- Design de API RESTful com boas práticas (tipagem, documentação automática, separação de responsabilidades)
- Containerização de aplicações Python para portabilidade e reprodutibilidade
- Automação de CI/CD, competência frequentemente exigida em vagas júnior de Engenharia de ML/MLOps
- Integração de modelo de ML a um serviço real, não apenas em notebook isolado
