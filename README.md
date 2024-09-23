# Category-Based Narrative Analysis with Azure OpenAI

## Overview

This is an Azure Function that utilizes Azure OpenAI to perform category-based narrative analysis. It takes in a JSON input containing a user-provided narrative and outputs a structured response with suspected crimes, confidence levels, and evidence from the input text.

## Requirements

* Python 3.x
* Azure Functions Runtime
* Azure OpenAI API (with `AZURE_OPENAI_DEPLOYMENT` and `AZURE_OPENAI_API_BASE` environment variables set)

## Usage

1. Deploy this function to an Azure Function App.
2. Set the `AZURE_OPENAI_DEPLOYMENT` and `AZURE_OPENAI_API_BASE` environment variables to your Azure OpenAI deployment and API base URL, respectively.
3. Send a JSON input containing a user-provided narrative to the `/category_trigger` endpoint.

## Input Format

The input JSON should have the following format:
```json
{
    "narrative": "<user-provided text>"
}
```
Replace `<user-provided text>` with the actual user-provided narrative.

## Output Format

The output will be a JSON response with the following structure:
```json
{
    "summary": "...",
    "suspected_crimes": ["...", ...],
    "confidence": 0.99,
    "evidence": [...]
}
```
* `summary`: A brief summary of the narrative.
* `suspected_crimes`: A list of suspected crimes (categories) with confidence levels.
* `confidence`: The overall confidence level of the response.
* `evidence`: A list of evidence from the input text that led to the decision.

## Notes

* This function uses a pre-defined prompt template stored in `./prompts/catprompt.txt`.
* You can modify this prompt template to suit your specific use case.
* The `CategoryEvidence` model represents a single piece of evidence with a category and confidence level.
* The `SummaryResponse` model represents the final output response with summary, suspected crimes, confidence, and evidence.