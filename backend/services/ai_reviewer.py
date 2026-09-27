# LangChain / OpenAI connection logic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def review_code_with_ai(code: str, calculated_complexity: str) -> str:
    """
    Sends the code and the AST-calculated time complexity to OpenAI for a qualitative review.
    """
    # Initialize the LLM (Requires OPENAI_API_KEY in environment variables)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    # Define the instruction template for the AI
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Senior Software Engineer reviewing code. Be concise, direct, and focus on best practices, edge cases, and maintainability. Do not use markdown headers, just return a brief, professional paragraph."),
        ("user", """
        Review the following Python code.
        
        My AST parser estimated the Time Complexity as: {complexity}
        
        Provide qualitative feedback on how this code can be improved in terms of readability, logic, or performance. If the complexity is O(N^2) or worse, suggest a way to optimize it.

        Code:
        {code}
        """)
    ])

    # Create the LangChain processing pipeline
    chain = prompt | llm | StrOutputParser()

    # Execute the chain
    result = chain.invoke({
        "code": code,
        "complexity": calculated_complexity
    })

    return result