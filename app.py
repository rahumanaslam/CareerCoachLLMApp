import os
import time
import logging
import streamlit as st
from docling.document_converter import DocumentConverter
from database import DatabaseUtils
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

        st.subheader("Your Profile")
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
            if not (industry and experience and current_role and target_role):
                st.error("Please fill out all the fields before generating the action plan.")
            else:
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
        resume_text = str()
        resume_file = st.file_uploader(
            "Upload your resume file here:", type=["pdf", "docx", "doc"]
        )
        if resume_file is not None:
            logging.info("Resume file uploaded")
            temp_file_path = f"temp_{resume_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(resume_file.getvalue())

            converter = DocumentConverter()
            result = converter.convert(temp_file_path)
            logging.info("Resume converted")
            resume_text = result.document.export_to_text()
            os.remove(temp_file_path)
        job_description = st.text_area(
            "Paste the job description (optional):", height=150
        )

        if st.button("Analyze Resume"):
            if not resume_text: 
                st.error("Please paste your resume text before analyzing it.")
            else:
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
            if not role or not location:
                st.error("Please enter a job title and location to research the market.")
            else:
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
            if not target_skills:
                st.error("Please enter the skills you want to develop.")
            else:
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
        It provides feedback on user responses.

        Parameters:
            app (CareerCoachApp): An instance of the CareerCoachApp class containing the logic for interview preparation.

        Features:
            - Inputs: Position, Question Type (Technical, Behavioral, Leadership, Problem Solving).
            - Interactive chat-based mock interview.
            - Real-time feedback.
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
            if not position: 
                st.error("Please enter a valid position.")
            elif not question_type:
                st.error("Please select a valid question type.")
            else:
                st.session_state.interview_ongoing = True
                st.session_state.interview_messages.append(
                    {
                        "role": "assistant",
                        "content": "Let's begin your interview! Tell me about yourself",
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
            if not goal or not platform:
                st.error("Please enter a goal and platform to generate the strategy.")
            else:
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
    
    @staticmethod
    def show_login_page(db_utils):
        """
        Renders the Login and Signup page for the AI Career Development Coach application.

        This page provides a user authentication interface with two tabs: 
        1. Login - Allows existing users to authenticate using their credentials.
        2. Signup - Enables new users to create an account by providing required details.

        Parameters:
            db_utils (DBUtils): An instance of the DBUtils class responsible for database operations 
                                such as user authentication and account creation.

        Features:
            - Displays a clean, tab-based interface for login and signup functionality.
            - Validates user credentials during login and provides appropriate feedback.
            - Ensures robust validation for signup, including password matching and required field checks.
            - Handles account creation and notifies users of success or failure during signup.
            - Redirects authenticated users to the main application and maintains session state.
        """
        st.title("AI Career Development Coach 💼")
        st.caption("Your personal AI-powered career development suite")
        tab1, tab2 = st.tabs(["login", "signup"])

        with tab1:
            st.subheader("Login")
            username = st.text_input(
                "Username", key="login_username"
            )
            password = st.text_input(
                "Password", type="password", key="login_password"
            )
            if st.button("Login"):
                if db_utils.authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with tab2:
            st.subheader("Create an Account")
            new_username = st.text_input(
                "username", key="signup_username"
            )
            new_email = st.text_input(
                "email", key="signup_email"
            )
            new_password = st.text_input(
                "password",
                type="password",
                key="signup_password"
            )
            confirm_password = st.text_input(
                "password",
                type="password",
                key="confirm_password"
            )
            if st.button("Sign up"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif not new_username or not new_password or not new_email:
                    st.error("All fields are required for signup")
                else:
                    if db_utils.create_user(new_username,
                                new_password,
                                new_email):
                        st.success("Account Created successfully! Please login.")
                    else:
                        st.error("Username or email already exists")

    @staticmethod
    def show_app():
        """
        Renders the main application interface for the AI Career Development Coach.

        This method serves as the entry point for the application, providing users with a personalized AI-powered career development suite. 
        It includes a sidebar for navigation and logout functionality, along with a dropdown menu to select various services offered by the app.

        Parameters:
            None

        Features:
            - Displays the app title and caption, welcoming users to the career development suite.
            - Provides a "Logout" button in the sidebar to allow users to log out and reset their session.
            - Displays the logged-in user's username in the sidebar for easy identification.
            - Offers a dropdown menu in the sidebar for users to navigate between different services:
                1. Dashboard: Overview of career insights and progress.
                2. Resume Analysis: Analyzes resumes and provides actionable feedback.
                3. Job Market Research: Assists users in researching job market trends.
                4. Skills Development: Guides users in identifying and developing key skills.
                5. Interview Preparation: Prepares users for interviews with tailored advice.
                6. Networking Strategy: Helps users build and optimize their professional network.
                7. Ask Career Coach: Provides an interactive Q&A interface with the AI Career Coach.
            - Dynamically renders the selected page using corresponding methods from the StreamlitInterface class.
        """
        logging.info("Starting AI Career Development Coach App")
        st.title("AI Career Development Coach 💼")
        st.caption("Your personal AI-powered career development suite")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
        st.sidebar.write(f"Logged in as: {st.session_state.username}")
        app = CareerCoachApp()
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


def main():
    """
    The main entry point for the AI Career Development Coach application.

    This function initializes the application, manages user authentication state, and determines 
    whether to display the login page or the main application interface. It ensures proper session 
    state management for user authentication and username tracking.

    Parameters:
        None

    Features:
        - Initializes the DatabaseUtils instance to handle database operations.
        - Manages session state variables:
            - 'authenticated': Tracks whether the user is logged in.
            - 'username': Stores the logged-in user's username.
        - Displays the login page if the user is not authenticated.
        - Displays the main application interface if the user is authenticated.
        - Ensures seamless navigation between authentication and application views.
    """
    db_utils = DatabaseUtils()
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if not st.session_state.authenticated:
        StreamlitInterface.show_login_page(db_utils)
    else:
        StreamlitInterface.show_app()


if __name__ == "__main__":
    main()
