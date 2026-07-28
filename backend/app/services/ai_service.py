import json
import logging
from groq import Groq
from app.core.config import settings

logger = logging.getLogger(__name__)

# Exceção customizada esperada pela sua rota resource.py
class AIServiceError(Exception):
    """Exceção disparada quando ocorre uma falha na geração via IA."""
    pass


SYSTEM_PROMPT = (
    "Você é um assistente educacional. Gere uma breve descrição e "
    "tags relevantes para o recurso informado no formato JSON rigoroso: "
    '{"description": "...", "tags": ["tag1", "tag2"]}'
)


def generate_description(title: str, resource_type: str) -> dict:
    user_prompt = f'Título: "{title}"\nTipo: {resource_type}'
    
    try:
        # Usa a chave da Groq configurada
        client = Groq(api_key=settings.groq_api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)

        # Garante que a lista de tags seja truncada para no máximo 3 itens
        if isinstance(data, dict) and "tags" in data and isinstance(data["tags"], list):
            data["tags"] = data["tags"][:3]

        return data

    except Exception as exc:
        logger.error(f"[AI Service Error] Falha na comunicação: {exc}")
        raise AIServiceError(f"Erro ao gerar descrição com IA: {exc}") from exc