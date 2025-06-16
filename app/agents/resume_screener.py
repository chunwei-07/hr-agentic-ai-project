from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import uuid
import os

from app.models.candidate import CandidateDetails
from app.utils.pii_masker import mask_pii

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                             google_api_key=google_api_key,
                             temperature=0)

def resume_screener_agent(resume_text: str) -> CandidateDetails:
    """
    Takes raw resume text, masks PII, and returns a structured CandidateDetails object.
    """
    print("--- Calling Resume Screener Agent ---")

    # Step 1: Mask PII before any other processing
    masked_resume_text = mask_pii(resume_text)

    # Step 2: Create a PydanticOutputParser for CandidateDetails
    parser = PydanticOutputParser(pydantic_object=CandidateDetails)

    # Step 3: Create the prompt template
    prompt_template = """
    You are an expert HR analyst. Your task is to parse a candidate's resume and extract key information into a structured format.
    The resume you are analyzing has had Personally Identifiable Information (PII) like names and contact details removed and replaced with placeholders. (e.g., <PERSON>, <EMAIL_ADDRESS>).

    Analyze the following masked resume:
    {masked_resume}

    **Instructions for extracting experience:**
    1.  Carefully read the entire resume to understand the candidate's work history.
    2.  Calculate the TOTAL number of years of professional experience.
    3.  Internship experience counts as professional experience.
    4.  If a range is given (e.g., "5-7 years"), use the lower number.
    5.  The final output for "experience_years" must be an integer. If no experience is mentioned anywhere, and only then, default to 0.

    **Example of your thought process:**
    - Input: "A recent graduate with 3 years of internship experience at <ORGANIZATION>." -> Output: `experience_years: 3`
    - Input: "Senior Engineer with a decade of experience." -> Output: `experience_yeras: 10`
    - Input: "Experience from 2018 to 2022 in a software role." -> Output: `experience_years: 4`
    
    Provide the final output in the required JSON format.
    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Step 4: Create the chain
    chain = prompt | llm | parser

    print("Parsing masked resume with LLM...")

    # Step 5: Invoke the chain
    # We pass the masked text to the LLM
    parsed_candidate_details = chain.invoke({"masked_resume": masked_resume_text})

    # We can programmatically set fields that the LLM shouldn't guess
    parsed_candidate_details.candidate_id = f"CAND_{uuid.uuid4().hex[:6].upper()}"
    parsed_candidate_details.pii_masked = True

    print("Resume screening complete.")
    return parsed_candidate_details