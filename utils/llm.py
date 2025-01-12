from langchain.llms import Ollama
from langchain.prompts import PromptTemplate


# Función para generar resúmenes con Ollama
def generate_summary_adjusted(articulo):
    try:
        if not all(k in articulo for k in ['titulo', 'resumen', 'enlace']):
            return "Error: El artículo no contiene toda la información requerida."

        llm = Ollama(model="llama3.1", temperature=0.7)
        prompt_template = PromptTemplate(
        input_variables=["resumen"],
        template="Resumen del artículo: {resumen}. Por favor, genera un resumen breve y ajustado a 280 caracteres."
        )
        prompt = prompt_template.format(resumen=articulo['resumen'])
        response = llm.invoke(prompt)

        if not response:
            return "Error: El resumen generado está vacío."

        tweet = f" \"{articulo['titulo']}\" {response} Más aquí: {articulo['enlace']}"

        if len(tweet) > 280:
            espacio_para_enlace = len(f"... Más aquí: {articulo['enlace']}")
            tweet = tweet[:280 - espacio_para_enlace] + f"... Más aquí: {articulo['enlace']}"

        return tweet

    except Exception as e:
        return f"Error al generar resumen: {str(e)}"