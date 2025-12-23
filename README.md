# CID: The Silicon Casefiles

A narrative-driven, AI-integrated detective simulation game inspired by the legendary Indian TV show CID.

## 🕵️ Game Features

- **Forensic Logic**: Use OpenCV-powered image enhancement and evidence analysis
- **Team Coordination**: Work with ACP Pradyuman, Daya, Abhijeet, and Dr. Salunkhe
- **Dynamic Interrogations**: AI-powered suspect dialogue using LLM integration
- **Evidence Graph System**: Connect clues logically to solve cases
- **Multiple Investigation Areas**: Crime scenes, forensic lab, and interrogation rooms

## 🛠️ Technical Stack

- **Python 3.10+**: Core programming language
- **Pygame**: 2D graphics, sound, and user input
- **OpenCV**: Image processing for forensic analysis
- **LLM Integration**: Gemini API / Ollama for dynamic dialogue
- **JSON/SQLite**: Game state and evidence storage

## 📦 Installation

1. Clone the repository:
```bash
git clone  https://github.com/farhat-1203/cid-mystery-engine.git
cd cid-silicon-casefiles
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up AI integration:
   - For Ollama: Install Ollama and pull a model like `llama2`  // implemented here //
   - For Gemini: Set your API key in the config

## 🎮 How to Play

1. Run the game:
```bash
python main.py
```

2. **Navigation**:
   - Arrow Keys: Navigate menus
   - Enter: Select options
   - Escape: Go back
   - Tab: Switch team members (in interrogation)

3. **Game Areas**:
   - **Bureau**: Central hub for case management
   - **Crime Scene**: Click on evidence markers to investigate
   - **Forensic Lab**: Analyze evidence with Dr. Salunkhe
   - **Interrogation**: Question suspects using different team approaches

## 🧩 Core Mechanics

### Evidence Graph System
Connect clues found at crime scenes to build logical deduction paths. The more connections you make, the stronger your case becomes.

### AI Interrogation
- Each team member has a unique questioning style
- Suspects have hidden stress meters that increase with pressure
- Present evidence during questioning for maximum impact
- Watch for behavioral changes and breakthrough moments

### Forensic Analysis
- Image enhancement using OpenCV
- Fingerprint analysis simulation
- Face detection in security footage
- Scientific evidence processing

## 🎯 Team Members & Specialties

- **ACP Pradyuman**: Logic & Leadership - Balanced questioning approach
- **Inspector Daya**: Intimidation & Action - High-pressure interrogation
- **Inspector Abhijeet**: Observation & Analysis - Gentle but persistent
- **Dr. Salunkhe**: Forensics & Science - Scientific methodology

## 🔧 Configuration

### AI Integration
Edit `src/engine/config.py` to configure:
- Gemini API key
- Ollama base URL
- Other game settings

### Adding Cases
The modular structure allows easy addition of new cases, suspects, and evidence types.

## 🚀 Development

The project follows a modular architecture:

```
src/
├── engine/          # Core game engine
├── states/          # Game state management
├── modules/         # Specialized systems (forensics, interrogation)
└── assets/          # Game assets (future)
```

## 📝 Master Prompt for AI Development

Use this prompt when asking AI tools to help extend the game:

> "I am developing a Python-based detective game titled 'CID: The Silicon Casefiles'. The gameplay is inspired by the Indian TV show CID. I need to build a system where the player acts as a Lead Investigator managing a team (ACP Pradyuman for logic, Daya for intimidation, Abhijeet for observation, and Dr. Salunkhe for forensics).
> 
> Core Mechanics: Evidence Graph system, AI Interrogation with stress meters, Forensic minigames using OpenCV. Please provide a Python implementation for [specific module]. Use Pygame for the interface and ensure the code is modular."

## 🎵 Audio Integration

The game is designed to support the iconic CID soundtrack and voice clips through Pygame's audio system.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the modular architecture
4. Test your changes
5. Submit a pull request

## 📄 License

This project is for educational and entertainment purposes. CID is a trademark of Sony Entertainment Television.

---

*"Kuch toh gadbad hai, Daya!"* 🔍
