import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from app.models.job import JobDetails
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                             google_api_key=google_api_key,
                             temperature=0)

def job_parser_agent(job_description_text: str) -> JobDetails:
    """
    Takes raw job description text and returns a structured JobDetails object.
    """
    # 1. Create a PydanticOutputParser
    # This automatically generates format instructions for the LLM
    parser = PydanticOutputParser(pydantic_object=JobDetails)

    # 2. Create the prompt template
    prompt_template = """
    You are an expert HR analyst. Your task is to parse a raw job description and extract key information into a structured format.

    Analyze the following job description:
    {job_description}

    Please provide the output in the required JSON format.
    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # 3. Create the chain using LangChain Expression Language (LCEL)
    chain = prompt | llm | parser

    print("--- Calling Job Parser Agent ---")
    print("Parsing job description with LLM...")

    # 4. Invoke the chain with input
    parsed_job_details = chain.invoke({"job_description": job_description_text})

    print("Job parsing complete.")
    return parsed_job_details