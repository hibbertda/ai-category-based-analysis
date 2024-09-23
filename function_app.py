import azure.functions as func
import os
import logging
import datetime
import json

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal, List, Optional

# Load prompt from file
def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Defined category literals
Category= Literal[    
    "Benefits/Marriage Fraud",
    "Bulk Cash Smuggling/Financial Crimes",
    "Child Exploitation/Pornography",
    "Cyber Crimes",
    "Employment/Exploitation of Unlawful Workers",
    "F/M Student Violations, Including OPT",
    "Fugitive Criminal Alien",
    "Gang Related",
    "Human Rights Violators",
    "Human Smuggling",
    "Human Trafficking (Forced Labor/Slavery)",
    "Immigration Telefraud",
    "Intellectual Property Rights",
    "Narcotics Smuggling",
    "Terrorism Related",
    "Trade Exportation Violation",
    "Other"
]

# Base model for evidence response
class CategoryEvidence(BaseModel):
    Category: str = Field(
        ..., description="category the evidence applies.", example="worried"
    )
    confidence: str = Field(
        ..., description="Confidence level as Float of selection", example=0.99
    )
    phrase: list[str] = Field(
        ..., description="The phase of the text", example=[
            "Im calling because... because I think I just saw some really bad stuff happen."
            ]
    )

# Category response model
class SummaryResponse(BaseModel):
    summary: str = Field(
        ..., description="The summary of the narrative", example="Pam bought bread from the store."
    )
    #suspected_crime: str = Field(
    suspected_crimes: list[Category] = Field(
        ..., description="List of categories, list more than one category if needed.", example="Theft"
    )
    confidence: float = Field(
        ..., description="The confidence of the category selection.", example=0.99
    )
    evidence: List[CategoryEvidence] = Field(
        ..., description="The parts of the text that lead to the decision", example=[
            {
                "category":"Theft", 
                "phase":["Im calling because... because I think I just saw some really bad stuff happen."]
                }
            ]
    )    

# Initialize Azure OpenAI
llm = AzureChatOpenAI(
    azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT'),
    temperature=0,
    top_p=1.0,
    verbose=True,
    azure_endpoint=os.getenv('AZURE_OPENAI_API_BASE')
)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ADMIN)

@app.route(route="category_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        narrative = req.get_json()
        logging.info(narrative)
    except ValueError as e:
        logging.error(f"Error parsing JSON: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON format"}),
            status_code=400,
            mimetype="application/json"
        )
    
    catPromptTemplate = load_prompt('./prompts/catprompt.txt')
    catPrompt = ChatPromptTemplate.from_template(catPromptTemplate)
    structured_category = llm.with_structured_output(SummaryResponse)

    results = structured_category.invoke(
        catPrompt.invoke(
            {
                "user_input": narrative
            }
        )
    )

    return func.HttpResponse(json.dumps(results.dict(), indent=4), mimetype="application/json")