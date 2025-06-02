# Agentic AI Prototype

An intelligent API that provides country information, performs mathematical calculations, and answers general questions. The system uses natural language processing to understand user queries and provide accurate answers.

## Features

- **Country Information:** Capital, population, area, and population density.
- **Country Data Calculations:** e.g., "What is the area of Brazil multiplied by 3?"
- **Math Calculations:** e.g., "What is 2 + 2?"
- **General Questions:** e.g., "Who are you?", "What can you do?"

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/AudioBF/Agentic_AI_Prototype.git
   cd Agentic_AI_Prototype
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure environment variables (optional):
   ```sh
   cp .env.example .env
   # Edit .env as needed
   ```

## Usage

Start the API server:
```sh
python app/main.py
```

## Example Queries

- "What is the capital of Brazil?"
- "France's population"
- "Area of Japan"
- "What is the population density of Brazil?"
- "What is the area of Brazil multiplied by 3?"
- "What is 2 + 2?"
- "And its capital?" (after a previous country question)

## Known Limitations

- Some natural language questions may not be recognized (e.g., "How many people live in Canada?", "How big is Canada?").
- Some specific patterns may not work (e.g., "Canada has a capital", "Multiply the area of France by 2").
- The country database is limited to a few examples.

## Project Structure

```
Agentic_AI_Prototype/
├── app/
│   ├── agent.py          # Main agent logic
│   ├── config.py         # Configuration
│   ├── memory.py         # Memory management
│   ├── tools.py          # Helper functions
│   └── main.py           # API entry point
├── tests/
│   └── test_api.py       # Automated tests
├── requirements.txt      # Dependencies
├── .env.example         # Example configuration
├── LICENSE              # MIT License
└── README.md            # Documentation
```

## Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## Roadmap

- [ ] Implement a more sophisticated NLP parser
- [ ] Add more countries to the database
- [ ] Improve fallback system
- [ ] Add more automated tests
- [ ] Implement caching for better performance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

AudioBF - [@AudioBF](https://github.com/AudioBF)

Project Link: [https://github.com/AudioBF/Agentic_AI_Prototype](https://github.com/AudioBF/Agentic_AI_Prototype)
