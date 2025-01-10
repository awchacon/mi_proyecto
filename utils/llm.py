from langchain.llms import Ollama
from langchain.prompts import PromptTemplate


# Función para generar resúmenes con Ollama
def generar_resumen_ajustado(articulo):
    try:
        if not all(k in articulo for k in ['titulo', 'resumen', 'enlace']):
            return "Error: El artículo no contiene toda la información requerida."

        # Inicializar el modelo de Ollama (CORREGIDO)
        llm = Ollama(model="llama3.1", temperature=0.7)
        prompt_template = PromptTemplate(
        input_variables=["resumen"],
        template="Resumen del artículo: {resumen}. Por favor, genera un resumen breve y ajustado a 280 caracteres."
        )
        prompt = prompt_template.format(resumen=articulo['resumen'])
        response = llm.invoke(prompt)

        # Invocar al LLM con .invoke (CORREGIDO)
        response = llm.invoke(prompt) # Usar invoke en lugar de _call o llm(prompt)

        if not response:
            return "Error: El resumen generado está vacío."

        tweet = f" \"{articulo['titulo']}\" {response} Más aquí: {articulo['enlace']}"

        if len(tweet) > 280:
            espacio_para_enlace = len(f"... Más aquí: {articulo['enlace']}")
            tweet = tweet[:280 - espacio_para_enlace] + f"... Más aquí: {articulo['enlace']}"

        return tweet

    except Exception as e:
        return f"Error al generar resumen: {str(e)}"