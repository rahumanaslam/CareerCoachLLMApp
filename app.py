import time
import logging
import streamlit as st
from career_coach import CareerCoachApp


st.set_page_config(page_title="AI Career Coach", page_icon="💼")

logging.basicConfig(
    level=logging.INFO,
    format="%(module)s - %(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s",
    filename="career_coach_log.log",
)


class StreamlitInterface:
    """
    A class to encapsulate the Streamlit-based user interface for the AI Career Coach application.
    This class provides methods to render different pages of the application, such as Dashboard,
    Resume Analysis, Job Market Research, etc. Each method corresponds to a specific feature of the app.
    """

    @staticmethod
    def dashboard(app):
        """
        Renders the Career Development Dashboard page.

        This page allows users to input their profile details (e.g., industry, experience, current role, target role)
        and generates a weekly action plan tailored to their career goals.

        Parameters:
            app (CareerCoachApp): An instance of the CareerCoachApp class containing the logic for generating action plans.

        Features:
            - User inputs: Industry, Years of Experience, Current Role, Target Role.
            - Generates a personalized weekly action plan using the `skills_developer` module.
        """
        logging.info("Dashboard page")
        st.header("Career Development Dashboard")

        with st.expander("Your Profile"):
            industry = st.text_input(
                "Industry", placeholder="e.g., Technology, Healthcare"
            )
            experience = st.slider("Years of Experience", 0, 30, 5)
            current_role = st.text_input(
                "Current Role", placeholder="e.g., Software Engineer"
            )
            target_role = st.text_input(
                "Target Role", placeholder="e.g., Senior Software Engineer"
            )

        st.subheader("Weekly Action Items")
        if st.button("Generate Action Plan"):
            with st.spinner("Creating your action plan..."):
                action_plan = app.skills_developer.run(
                    f"Create a weekly action plan for a {current_role} targeting {target_role} role "
                    f"in {industry} with {experience} years of experience. Format document as a clear markdown document with headers and subheaders",
                    stream=False,
                )
                st.write(action_plan.content)

    @staticmethod
    def resume_analysis(app):
        """
        Renders the Resume Analysis page.

        This page allows users to paste their resume text and optionally a job description for analysis.
        The app evaluates the resume and provides feedback on how well it matches the job description.

        Parameters:
            app (CareerCoachApp): An instance of the CareerCoachApp class containing the logic for resume analysis.

        Features:
            - Analyzes resume content.
            - Compares resume with an optional job description.
            - Provides actionable insights to improve the resume.
        """
        logging.info("Resume Analysis page")
        st.header("Resume Analysis")
        resume_text = st.text_area("Paste your resume text here:", height=300)
        job_description = st.text_area(
            "Paste the job description (optional):", height=150
        )

        if st.button("Analyze Resume"):
            with st.spinner("Analyzing your resume..."):
                analysis = app.resume_analyzer.run(
                    f"Analyze this resume:\n{resume_text}\n"
                    + (
                        f"Compare with job description:\n{job_description}"
                        if job_description
                        else ""
                    ),
                    stream=False,
                )
                st.write(analysis.content)

    @staticmethod
    def job_market_research(app):
        """
        Renders the Job Market Research page.

        This page allows users to research the job market for a specific role and location.
        It provides insights into salary ranges, required skills, and market demand.

        Parameters:
            app (CareerCoachApp): An instance of the CareerCoachApp class containing the logic for job market research.

        Features:
            - Inputs: Job Title, Location.
            - Outputs: Salary ranges, required skills, and market demand in a markdown format.
        """
        logging.info("Job Market Research page")
        st.header("Job Market Research")
        role = st.text_input("Job Title", placeholder="e.g., Data Scientist")
        location = st.text_input("Location", placeholder="e.g., San Francisco")

        if st.button("Research Market"):
            with st.spinner("Researching job market..."):
                research = app.market_researcher.run(
                    f"Research the job market for {role} in {location}. "
                    "Include salary ranges, required skills, and market demand. Format document as a clear markdown document with headers and subheaders",
                    stream=False,
                )
                st.write(research.content)

    @staticmethod
    def skills_development(app):
        """
        Renders the Skills Development Plan page.

        This page helps users create a learning plan for developing specific skills within a given timeframe.

        Parameters:
            app (CareerCoachApp): An instance of the CareerCoachApp class containing the logic for skills development.

        Features:
            - Inputs: Target skills, Learning timeframe (in months).
            - Outputs: A detailed learning plan in markdown format.
        """
        logging.info("Skills Development page")
        st.header("Skills Development Plan")
        target_skills = st.text_area("What skills do you want to develop?")
        timeframe = st.slider("Learning timeframe (months)", 1, 12, 3)

        if st.button("Create Learning Plan"):
            with st.spinner("Creating your learning plan..."):
                plan = app.skills_developer.run(
                    f"Create a {timeframe}-month learning plan for: {target_skills}. Format document as a clear markdown document with headers and subheaders",
                    stream=False,
                )
                st.write(plan.content)

    @staticmethod
    def interview_preparation(app):
        """
        Renders the Interview Preparation page.

        This page simulates a mock interview session for a specific position and question type.
        It provides feedback on user responses and conducts a final assessment after 5-7 questions.

        Parameters:
            app (CareerCoachApp): An instance of the CareerCoachApp class containing the logic for interview preparation.

        Features:
            - Inputs: Position, Question Type (Technical, Behavioral, Leadership, Problem Solving).
            - Interactive chat-based mock interview.
            - Real-time feedback and final assessment.
        """
        logging.info("Interview Preparation page")
        st.header("Interview Coach")

        # Reserve space for better positioning
        top_placeholder = st.empty()

        # Store chat history
        if "interview_messages" not in st.session_state:
            st.session_state.interview_messages = []

        if "interview_ongoing" not in st.session_state:
            st.session_state.interview_ongoing = False

        # User inputs
        position = top_placeholder.text_input("Position you're interviewing for:")
        question_type = st.selectbox(
            "Question Type",
            ["Technical", "Behavioral", "Leadership", "Problem Solving"],
        )

        if st.button("Start Mock Interview") and not st.session_state.interview_ongoing:
            st.session_state.interview_ongoing = True
            st.session_state.interview_messages.append(
                {
                    "role": "assistant",
                    "content": "Let's begin your mock interview!",
                }
            )
            st.rerun()

        # Push content down
        st.write("---")

        # Display previous messages properly positioned
        for message in st.session_state.interview_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat interaction
        if st.session_state.interview_ongoing:
            if prompt := st.chat_input("Your Answer:"):
                # Append user's response to chat history
                st.session_state.interview_messages.append(
                    {"role": "user", "content": prompt}
                )

                with st.chat_message("user"):
                    st.markdown(prompt)

                # Construct dynamic prompt for the agent
                conversation_history = "\n".join(
                    [
                        f"{msg['role']}: {msg['content']}"
                        for msg in st.session_state.interview_messages
                    ]
                )
                dynamic_prompt = (
                    f"You are conducting a mock interview for a {position} position. "
                    f"The question type is {question_type}. Here is the conversation so far:\n"
                    f"{conversation_history}\n"
                    "Based on the user's latest response, provide feedback and ask the next question. "
                    "If this is the final question, provide a final assessment."
                )

                # Generate assistant's response
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    response_text = ""

                    for word in CareerCoachApp.response_generator(
                        app.interview_coach,
                        dynamic_prompt,
                    ):
                        response_text += word
                        placeholder.markdown(response_text)
                        time.sleep(0.01)

                    st.session_state.interview_messages.append(
                        {"role": "assistant", "content": response_text}
                    )

    @staticmethod
    def networking_strategy(app):
        """
        Renders the Networking Strategy page.

        This page helps users generate a networking strategy based on their goals and preferred platform.

        Parameters:
            app (CareerCoachApp): An instance of the CareerCoachApp class containing the logic for networking strategies.

        Features:
            - Inputs: Networking Goal, Platform Focus (e.g., LinkedIn, Industry Events).
            - Outputs: A detailed networking strategy in markdown format.
        """
        logging.info("Networking Strategy page")
        st.header("Networking Strategy")
        goal = st.text_input("Networking Goal", placeholder="e.g., Change industries")
        platform = st.selectbox(
            "Platform Focus",
            [
                "LinkedIn",
                "Industry Events",
                "Professional Associations",
                "Cold Outreach",
            ],
        )

        if st.button("Generate Strategy"):
            with st.spinner("Creating networking strategy..."):
                strategy = app.networking_strategist.run(
                    f"Create a networking strategy for {goal} focusing on {platform}. Format document as a clear markdown document with headers and subheaders",
                    stream=False,
                )
                st.write(strategy.content)

    @staticmethod
    def ask_career_coach(app):
        """
        Renders the Ask Career Coach page.

        This page allows users to ask open-ended questions to the AI Career Coach.
        The app provides real-time responses in a chat-based interface.

        Parameters:
            app (CareerCoachApp): An instance of the CareerCoachApp class containing the logic for the career coach.

        Features:
            - Interactive chat-based Q&A with the AI Career Coach.
            - Maintains chat history for context-aware responses.
        """
        logging.info("Ask Career Coach page")
        st.header("Ask Career Coach")

        if "career_coach_messages" not in st.session_state:
            st.session_state.career_coach_messages = []

        for message in st.session_state.career_coach_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask Anything to the Career Coach"):
            st.session_state.career_coach_messages.append(
                {"role": "user", "content": prompt}
            )

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                placeholder = st.empty()
                response_text = ""
                for word in CareerCoachApp.response_generator(
                    app.ask_career_coach, prompt
                ):
                    response_text += word
                    placeholder.markdown(response_text)
                    time.sleep(0.01)

            st.session_state.career_coach_messages.append(
                {"role": "assistant", "content": response_text}
            )


def main():
    """
    The entry point of the AI Career Development Coach application.

    This function initializes the Streamlit app, sets up the navigation sidebar,
    and routes users to the selected service page. It also initializes the CareerCoachApp instance.

    Features:
        - Sets the page title and icon.
        - Provides a sidebar for navigation between different services.
        - Dynamically renders the selected page using the StreamlitInterface class.
    """
    logging.info("Starting AI Career Development Coach App")
    st.title("AI Career Development Coach 💼")
    st.caption("Your personal AI-powered career development suite")

    app = CareerCoachApp()

    # Main Navigation
    page = st.sidebar.selectbox(
        "Select Service",
        [
            "Dashboard",
            "Resume Analysis",
            "Job Market Research",
            "Skills Development",
            "Interview Preparation",
            "Networking Strategy",
            "Ask Career Coach",
        ],
    )

    if page == "Dashboard":
        StreamlitInterface.dashboard(app)

    elif page == "Resume Analysis":
        StreamlitInterface.resume_analysis(app)

    elif page == "Job Market Research":
        StreamlitInterface.job_market_research(app)

    elif page == "Skills Development":
        StreamlitInterface.skills_development(app)

    elif page == "Interview Preparation":
        StreamlitInterface.interview_preparation(app)

    elif page == "Networking Strategy":
        StreamlitInterface.networking_strategy(app)

    elif page == "Ask Career Coach":
        StreamlitInterface.ask_career_coach(app)


if __name__ == "__main__":
    main()
