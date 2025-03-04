# Career Coach LLM App

## Overview

This **Career Coach LLM App* is designed to provide personalized career guidance using large language models. This project consists of several modules:

- **app**: Contains the main application code
- **career_coach_llm**: Included the core logic for the career coaching LLM.
- **experiments**: Houses various experiments and research related to improving the LLM's performance.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)

## Installation

To get started with the Career Coach LLM App. follow these steps:

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.10 or higher
- Git
- Ollama
  
### Setup

1. Install Ollama and pull the model:

Download Ollama from https://ollama.com/

Install the `llama3.2` model by running the following command:

```bash
ollama pull llama3.2
ollama serve
```

2. Clone the repository:

```bash
git clone https://github.com/rahumanaslam/CareerCoachApp.git
cd career-coach-llm
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

To run the application, execute the following command:

```bash
streamlit run app.py
```

This will start the Streamlit application, allowing you to interact with the different modules and features.