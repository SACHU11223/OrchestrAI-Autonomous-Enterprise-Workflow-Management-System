"""
OrchestrAI - Hugging Face Models Service
Provides ML processing for sentiment and classification via Hugging Face Inference API.
"""
import requests
from typing import Dict, Any, List
from core.config import get_settings

settings = get_settings()

class HuggingFaceClient:
    def __init__(self):
        self.api_key = settings.HF_API_KEY
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        self.base_url = "https://api-inference.huggingface.co/models"

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Calls a BERT or DistilBERT model to classify sentiment.
        Returns positive, neutral, or negative.
        """
        # If no key is set, we gracefully fallback to None so agents can use LLM instead
        if not self.api_key:
            return None

        # Using a reliable distilbert sentiment model
        model = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        url = f"{self.base_url}/{model}"
        
        try:
            response = requests.post(url, headers=self.headers, json={"inputs": text}, timeout=10)
            if response.status_code == 200:
                result = response.json()
                
                # Model returns format like [[{"label": "positive", "score": 0.98}, ...]]
                if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
                    scores = result[0]
                    # Sort by highest score
                    scores.sort(key=lambda x: x.get("score", 0), reverse=True)
                    top_prediction = scores[0]
                    
                    sentiment = top_prediction.get("label", "neutral").lower()
                    
                    # Convert labels if the model uses different terms
                    if "param_pos" in sentiment or sentiment == "positive":
                        mapped_sentiment = "positive"
                    elif "param_neg" in sentiment or sentiment == "negative":
                        mapped_sentiment = "negative"
                    else:
                        mapped_sentiment = "neutral"

                    return {
                        "sentiment": mapped_sentiment,
                        "score": top_prediction.get("score", 0.5),
                        "source": "hugging_face"
                    }
            else:
                print(f"hf_models warning: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"hf_models error: {e}")
            
        return None

hf_client = HuggingFaceClient()
