# PLACE HOLDER READ ME FOR NOW



# AI Hangout - Multi-Agent Chat System

A sophisticated multi-agent chat system that brings together four unique AI personalities in a dynamic group conversation. Built with CrewAI and LangGraph, this project demonstrates the power of collaborative AI with specialized agents working together to create engaging discussions.

## About the Project

AI Hangout allows you to chat with four distinct AI personalities simultaneously:
- 🖥️ **Tech Enthusiast**: Passionate about technology and innovation
- 🎬 **Film Critic**: Expert in cinema and storytelling
- 💪 **Fitness Coach**: Focused on health and wellness
- 🧠 **Philosopher**: Asks thought-provoking questions

Each agent has their own expertise, communication style, and perspective, creating rich, multi-faceted conversations on any topic.

For a detailed explanation of the concepts behind this project, check out my Medium article: [My AI Agents Don't Steal My Lunch from the Fridge: Creating Ideal Coworkers with CrewAI and Langraph](https://medium.com/@yourhandle/article-link)

## Features

- **Multi-Agent Collaboration**: Four distinct AI agents with unique personalities and expertise
- **Dynamic Conversations**: Real-time responses from all agents
- **Web Interface**: Clean, modern UI for easy interaction
- **API Backend**: RESTful API for extensibility
- **Docker Support**: Easy deployment and consistent environments
- **Persistent Storage**: Conversation history saved locally

## Tech Stack

- **Backend**: Python, CrewAI, LangGraph
- **Frontend**: Flask, HTML, CSS, JavaScript
- **LLM Provider**: Groq (Llama 3)
- **Deployment**: Docker, Docker Compose

## Prerequisites

- Python 3.10+
- Docker and Docker Compose (for containerized deployment)
- Groq API key

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-hangout.git
   cd ai-hangout
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install flask
   ```

4. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

### Running Locally

1. Start the backend API:
   ```bash
   python main.py --mode api
   ```

2. In a new terminal, start the Flask frontend:
   ```bash
   cd frontend
   python app.py
   ```

3. Open your browser and navigate to `http://localhost:5000`

### Docker Deployment

1. Build and run with Docker Compose:
   ```bash
   docker-compose build
   docker-compose up
   ```

2. Access the application at `http://localhost:5000`

## Project Structure

```
ai_hangout/
├── agents/                 # AI agent configurations
├── config/                 # Configuration settings
├── frontend/              # Flask web interface
│   ├── app.py            # Flask application
│   ├── static/           # CSS and JavaScript
│   └── templates/        # HTML templates
├── models/                # Data models
├── services/              # External service integrations
├── utils/                 # Utility functions
├── workflows/             # LangGraph workflows
├── docker-compose.yml     # Docker configuration
├── Dockerfile            # Container definition
├── main.py               # Main application entry
└── requirements.txt      # Python dependencies
```

## Deployment

### Free Hosting Options

The project can be deployed for free on various platforms:

1. **Render.com** (Recommended)
   - Connect your GitHub repository
   - Add GROQ_API_KEY as environment variable
   - Deploy automatically

2. **Railway.app**
   - Import from GitHub
   - Configure environment variables
   - Deploy with one click

3. **Fly.io**
   - Use the provided fly.toml configuration
   - Deploy with flyctl

See the [Deployment Guide](deployment-guide.md) for detailed instructions.

## Usage

1. Enter a topic to discuss
2. All four AI agents will respond with their unique perspectives
3. Continue the conversation by sending your own messages
4. Each agent maintains their personality throughout the discussion

## API Endpoints

- `POST /api/start-conversation`: Start a new conversation
- `GET /api/continue-conversation/{id}`: Get agent responses
- `POST /api/add-message/{id}`: Add a user message

## Configuration

Key settings can be adjusted in `config/settings.py`:
- `DEFAULT_MODEL`: The Groq model to use (default: llama3-8b-8192)
- `MAX_ITERATIONS`: Maximum conversation turns per round
- `DEFAULT_TEMPERATURE`: Controls response creativity

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [LangGraph](https://github.com/langchain-ai/langgraph) for conversation flow management
- [Groq](https://groq.com/) for fast LLM inference

## Author

**Ibrahim Akhtar**
- Medium: [@yourhandle](https://medium.com/@yourhandle)
- LinkedIn: [Ibrahim Akhtar](https://www.linkedin.com/in/yourprofile)
- GitHub: [@yourusername](https://github.com/yourusername)

## Support

If you find this project helpful, please give it a ⭐️ on GitHub!

For questions or support, please open an issue in the repository.

---

*Article count since unemployment: 2* 🚀