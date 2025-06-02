# Agentic AI Prototype

Uma API inteligente que fornece informações sobre países, realiza cálculos matemáticos e responde perguntas gerais. O sistema utiliza processamento de linguagem natural para entender perguntas em linguagem natural e fornecer respostas precisas.

## Funcionalidades

### 1. Informações sobre Países
- **Capital**: "What is the capital of Brazil?"
- **População**: "France's population"
- **Área**: "Area of Japan"
- **Densidade Populacional**: "What is the population density of Brazil?"

### 2. Cálculos com Dados de Países
- Multiplicação de área: "What is the area of Brazil multiplied by 3?"
- Cálculos com população: "Japan's population times 2"

### 3. Cálculos Matemáticos
- Operações básicas: "What is 2 + 2?"
- Expressões complexas: "Calculate 5 * 10"

### 4. Perguntas Gerais
- "Who are you?"
- "What can you do?"
- "How are you?"

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/AudioBF/Agentic_AI_Prototype.git
cd Agentic_AI_Prototype
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Uso

### Iniciando o Servidor
```bash
python app/main.py
```

### Exemplos de Uso

#### Perguntas sobre Países
```python
# Capital
"What is the capital of Brazil?"  # Retorna: "The capital of Brazil is Brasília."

# População
"France's population"  # Retorna: "The population of France is 67,390,000 people."

# Área
"Area of Japan"  # Retorna: "The area of Japan is 377,975 km²."

# Densidade Populacional
"What is the population density of Brazil?"  # Retorna: "The population density of Brazil is 25.17 people per km²."
```

#### Cálculos
```python
# Multiplicação de Área
"What is the area of Brazil multiplied by 3?"  # Retorna: "The area of Brazil is 8,515,770 km². Multiplied by 3, that is 25,547,310 km²."

# Cálculos Matemáticos
"What is 2 + 2?"  # Retorna: "2 + 2 = 4"
```

## Limitações Conhecidas

1. **Perguntas Naturais**: Algumas perguntas em linguagem natural podem não ser reconhecidas:
   - "How many people live in Canada?"
   - "How big is Canada?"

2. **Padrões Específicos**: Alguns padrões de pergunta podem não funcionar:
   - "Canada has a capital"
   - "Multiply the area of France by 2"

## Estrutura do Projeto

```
Agentic_AI_Prototype/
├── app/
│   ├── agent.py          # Lógica principal do agente
│   ├── config.py         # Configurações
│   ├── memory.py         # Gerenciamento de memória
│   ├── tools.py          # Funções auxiliares
│   └── main.py           # Ponto de entrada da API
├── tests/
│   └── test_api.py       # Testes automatizados
├── requirements.txt      # Dependências
├── .env.example         # Exemplo de configuração
└── README.md            # Documentação
```

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Roadmap

- [ ] Implementar parser NLP mais sofisticado
- [ ] Adicionar mais países à base de dados
- [ ] Melhorar sistema de fallback
- [ ] Adicionar mais testes automatizados
- [ ] Implementar cache para melhor performance

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

AudioBF - [@AudioBF](https://github.com/AudioBF)

Link do Projeto: [https://github.com/AudioBF/Agentic_AI_Prototype](https://github.com/AudioBF/Agentic_AI_Prototype)
