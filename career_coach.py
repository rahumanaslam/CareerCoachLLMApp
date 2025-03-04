import logging
import time
from textwrap import dedent
from agno.agent import Agent
from agno.models.ollama import Ollama
from config import model_name, agent_prompts
from tools import DuckDuckGoTools

logging.basicConfig(
    level=logging.INFO,
    format="%(module)s - %(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s",
    filename="career_coach_log.log",
)


class CareerCoachApp:
    """
    The main application class for the AI Career Coach.

    This class initializes the underlying language model (Ollama) and sets up specialized agents
    for various career-related tasks such as resume analysis, job market research, skills development,
    interview preparation, networking strategies, and general career advice. It also provides a utility
    method to generate responses in a streaming format for interactive user experiences.

    Attributes:
        llama_model (Ollama): An instance of the Ollama language model used by all agents.
        resume_analyzer (Agent): Agent for analyzing resumes and providing feedback.
        market_researcher (Agent): Agent for researching job markets and providing insights.
        skills_developer (Agent): Agent for creating personalized skills development plans.
        interview_coach (Agent): Agent for conducting mock interviews and providing feedback.
        networking_strategist (Agent): Agent for generating networking strategies.
        ask_career_coach (Agent): Agent for answering open-ended career-related questions.
    """

    def __init__(self):
        """
        Initializes the CareerCoachApp by setting up the Ollama language model and configuring specialized agents.

        - Sets up agents for specific career-related tasks using predefined prompts and tools.
        """
        logging.debug("Initializing Ollama model...")
        self.llama_model = Ollama(id=model_name)
        self.setup_agents()

    @staticmethod
    def response_generator(agent, prompt):
        """
        Generates a streaming response from the given agent for the specified prompt.

        This method splits the response into words and yields them one by one to simulate real-time interaction.
        It introduces small delays between words and lines to enhance the user experience.

        Parameters:
            agent (Agent): The agent responsible for generating the response.
            prompt (str): The input prompt for which the response is generated.

        Yields:
            str: A word or line of the response.
        """
        logging.debug(f"Generating response for '{prompt}'")
        response = agent.run(prompt, stream=False)
        response = str(response.content)
        lines = response.split("\n")
        for line in lines:
            for word in line.split():
                yield word + " "
                time.sleep(0.01)
            yield "\n"
            time.sleep(0.01)
        logging.debug("Response generation complete")

    def setup_agents(self):
        """
        Configures specialized agents for various career-related tasks.

        Each agent is initialized with the Ollama language model, a description, instructions, and tools.
        The agents are designed to handle specific tasks such as resume analysis, job market research,
        skills development, interview preparation, networking strategies, and general career advice.

        Agents:
            - resume_analyzer: Analyzes resumes and compares them with job descriptions.
            - market_researcher: Provides insights into job markets based on role and location.
            - skills_developer: Creates personalized learning plans for skill development.
            - interview_coach: Conducts mock interviews and provides feedback.
            - networking_strategist: Generates networking strategies based on user goals.
            - ask_career_coach: Answers open-ended career-related questions.

        Tools:
            - DuckDuckGoTools: Used by agents to fetch external data when needed.
        """
        logging.debug("Setting up agents...")

        self.resume_analyzer = Agent(
            name="ResumeAnalyzer",
            model=self.llama_model,
            description=dedent(agent_prompts["resume_analysis"]["description"]),
            instructions=agent_prompts["resume_analysis"]["instructions"],
            tools=[DuckDuckGoTools()],
            markdown=True,
        )

        self.market_researcher = Agent(
            name="MarketResearcher",
            model=self.llama_model,
            description=dedent(agent_prompts["job_market_research"]["description"]),
            instructions=agent_prompts["job_market_research"]["instructions"],
            tools=[DuckDuckGoTools()],
            markdown=True,
        )

        self.skills_developer = Agent(
            name="SkillsDeveloper",
            model=self.llama_model,
            description=dedent(agent_prompts["skills_development"]["description"]),
            instructions=agent_prompts["skills_development"]["instructions"],
            tools=[DuckDuckGoTools()],
            markdown=True,
        )

        self.interview_coach = Agent(
            name="InterviewCoach",
            model=self.llama_model,
            description=dedent(agent_prompts["interview_coach"]["description"]),
            instructions=agent_prompts["interview_coach"]["instructions"],
            tools=[DuckDuckGoTools()],
            markdown=True,
        )

        self.networking_strategist = Agent(
            name="NetworkingStrategist",
            model=self.llama_model,
            description=dedent(agent_prompts["networking_strategist"]["description"]),
            instructions=agent_prompts["networking_strategist"]["instructions"],
            tools=[DuckDuckGoTools()],
            markdown=True,
        )

        self.ask_career_coach = Agent(
            name="AskCareerCoach",
            model=self.llama_model,
            description=dedent(agent_prompts["ask_career_coach"]["description"]),
            instructions=agent_prompts["ask_career_coach"]["instructions"],
            tools=[DuckDuckGoTools()],
            markdown=True,
        )
