from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.gemini import gemini_key, gemini_model
from src.model import PetitionAnalysisOutput

class PetitionAnalyzer:
    def __init__(self):
        self.GEMINI_API_KEY = gemini_key()
        self.GEMINI_MODEL = gemini_model()
        self.parser = PydanticOutputParser(pydantic_object=PetitionAnalysisOutput)
        
        self.prompt = PromptTemplate(
            template=""" You are an expert government petition analyst for the Indian government. Analyze the following petition and extract relevant information:
            Petition: "{petition_text}"
            Additional context (if any): "{additional_context}"
            Categorize this petition into the most appropriate Indian government ministry or department, determine its urgency and importance, identify the category and subcategory, estimate resolution time, and provide other relevant information.
            For the department, choose the most appropriate from: 
            Ministry of Health and Family Welfare, Ministry of Education, Ministry of Road Transport and Highways, Ministry of Railways, Ministry of Finance, Ministry of Housing and Urban Affairs, Ministry of Environment, Forest and Climate Change, Ministry of Agriculture and Farmers Welfare, Ministry of Rural Development, Ministry of Home Affairs, Ministry of Jal Shakti, Ministry of Power, or Others.

            For urgency_level and importance_level, use a scale of 1-5 where:
            - Urgency 5: Immediate action required (life-threatening, time-critical)
            - Urgency 4: Very urgent (significant negative impact if delayed)
            - Urgency 3: Moderately urgent (should be addressed soon)
            - Urgency 2: Slightly urgent (can be addressed in regular course of business)
            - Urgency 1: Not urgent (can be delayed without significant impact)

            Similar scale for importance_level, where 5 means critical importance to many people or communities.
            Consider relevant Indian policies, schemes, and local governance structures (Panchayats, Municipal Corporations, etc.) when analyzing the petition. 
            Determine if this petition is repetitive by checking if it addresses issues similar to common or recurring grievances in the Indian context. Flag cases that require special follow-up or attention from specific authorities.
            Provide a list of key points extracted from the petition and recommend specific actions aligned with existing Indian government programs, schemes, or initiatives where applicable.

            Return the output in the following JSON format:
            {format_instruction}
            """,
            input_variables=["petition_text", "additional_context"],
            partial_variables={"format_instruction": self.parser.get_format_instructions()},
        )
        
        # Create the LLM and chain
        self.llm = GoogleGenerativeAI(model=self.GEMINI_MODEL, google_api_key=self.GEMINI_API_KEY)
        self.petition_analysis_chain = self.prompt | self.llm | self.parser
    
    def get_response(self, petition_text, additional_context=""):
        """
        Analyze a petition using the Gemini model and return structured analysis in the Indian context.
        
        Args:
            petition_text (str): The text of the petition to analyze
            additional_context (str, optional): Any additional context about the petition. Defaults to "".
            
        Returns:
            PetitionAnalysisOutput: Structured analysis of the petition
        """
        return self.petition_analysis_chain.invoke({
            "petition_text": petition_text,
            "additional_context": additional_context
        })