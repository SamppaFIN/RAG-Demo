import os
import time
import json
import asyncio
import numpy as np
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIRAGService:
    def __init__(self):
        """Initialize the OpenAI RAG service with API key and candy data."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Load candy data
        self.candies = self._load_candy_data()
        self.candy_embeddings = self._precompute_embeddings()
        
        # Translations for UI
        self.translations = {
            "query_processing": {
                "en": "Query Processing",
                "fi": "Kyselyn käsittely"
            },
            "query_embedding": {
                "en": "Query Embedding",
                "fi": "Kyselyn vektorointi"
            },
            "vector_search": {
                "en": "Vector Search",
                "fi": "Vektorihaku"
            },
            "context_preparation": {
                "en": "Context Preparation",
                "fi": "Kontekstin valmistelu"
            },
            "ai_generation": {
                "en": "AI Generation",
                "fi": "Tekoäly-generointi"
            }
        }

    def _load_candy_data(self) -> List[Dict[str, Any]]:
        """Load the comprehensive candy dataset."""
        return [
            {
                "id": 1,
                "name": "Dark Chocolate Truffle",
                "category": "chocolate",
                "description": "Rich, velvety dark chocolate truffle with 70% cocoa content. Silky smooth ganache center.",
                "sweetness": 6,
                "flavors": ["dark chocolate", "cocoa", "vanilla"],
                "texture": "smooth",
                "origin": "Belgium"
            },
            {
                "id": 2,
                "name": "Strawberry Sour Belt",
                "category": "sour",
                "description": "Tangy strawberry-flavored sour candy with a chewy texture and sugar coating.",
                "sweetness": 8,
                "flavors": ["strawberry", "citric acid", "artificial fruit"],
                "texture": "chewy",
                "origin": "USA"
            },
            {
                "id": 3,
                "name": "Vanilla Caramel Fudge",
                "category": "caramel",
                "description": "Creamy vanilla fudge with ribbon of golden caramel. Made with real Madagascar vanilla.",
                "sweetness": 9,
                "flavors": ["vanilla", "caramel", "butter", "cream"],
                "texture": "soft",
                "origin": "France"
            },
            {
                "id": 4,
                "name": "Lemon Drop Hard Candy",
                "category": "citrus",
                "description": "Classic hard candy with intense lemon flavor. Bright yellow color with crystalline texture.",
                "sweetness": 7,
                "flavors": ["lemon", "citrus", "tartaric acid"],
                "texture": "hard",
                "origin": "UK"
            },
            {
                "id": 5,
                "name": "Mint Chocolate Chip",
                "category": "chocolate",
                "description": "Cool peppermint chocolate with dark chocolate chips. Refreshing and indulgent.",
                "sweetness": 7,
                "flavors": ["peppermint", "chocolate", "cream"],
                "texture": "creamy",
                "origin": "Italy"
            },
            {
                "id": 6,
                "name": "Gummy Rainbow Bears",
                "category": "gummy",
                "description": "Soft, chewy gummy bears in assorted fruit flavors. Each color represents a different taste.",
                "sweetness": 8,
                "flavors": ["mixed fruit", "cherry", "orange", "lemon", "strawberry", "lime"],
                "texture": "gummy",
                "origin": "Germany"
            }
        ]

    def _precompute_embeddings(self) -> Dict[int, List[float]]:
        """Precompute embeddings for all candies using OpenAI's text-embedding-3-small model."""
        embeddings = {}
        
        for candy in self.candies:
            # Create a comprehensive text representation
            text = f"{candy['name']} {candy['category']} {candy['description']} {' '.join(candy['flavors'])} {candy['texture']} sweetness level {candy['sweetness']}"
            
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                embeddings[candy['id']] = response.data[0].embedding
                logger.info(f"Generated embedding for {candy['name']}")
            except Exception as e:
                logger.error(f"Failed to generate embedding for {candy['name']}: {e}")
                # Fallback to random embedding for demo purposes
                embeddings[candy['id']] = np.random.normal(0, 1, 1536).tolist()
        
        return embeddings

    def _generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for the user query using OpenAI."""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            # Fallback to random embedding
            return np.random.normal(0, 1, 1536).tolist()

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)
        
        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

    def _search_similar_candies(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """Find the most similar candies based on embedding similarity."""
        similarities = []
        
        for candy in self.candies:
            candy_embedding = self.candy_embeddings[candy['id']]
            similarity = self._cosine_similarity(query_embedding, candy_embedding)
            
            similarities.append({
                'candy': candy,
                'similarity': similarity,
                'rank': 0  # Will be set after sorting
            })
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Add ranks
        for i, item in enumerate(similarities[:top_k]):
            item['rank'] = i + 1
        
        return similarities[:top_k]

    def _generate_ai_response(self, query: str, context_candies: List[Dict[str, Any]], language: str) -> str:
        """Generate AI response using OpenAI based on the retrieved context."""
        # Prepare context information
        context_info = []
        for item in context_candies:
            candy = item['candy']
            context_info.append(f"- {candy['name']}: {candy['description']} (Sweetness: {candy['sweetness']}/10)")
        
        context_text = "\n".join(context_info)
        
        # Create system prompt based on language
        if language == 'fi':
            system_prompt = """Olet ystävällinen makeiskaupan asiantuntija. Vastaa kysymyksiin makeisista ja herkkuista perustuen annettuun kontekstiin. 
            Pidä vastaus hauska, informatiivinen ja noin 2-3 virkettä pitkä. Käytä emojeja sopivasti."""
            user_prompt = f"Konteksti makeisista:\n{context_text}\n\nKysymys: {query}"
        else:
            system_prompt = """You are a friendly candy store expert. Answer questions about candies and sweets based on the provided context. 
            Keep the response fun, informative, and about 2-3 sentences long. Use emojis appropriately."""
            user_prompt = f"Context about candies:\n{context_text}\n\nQuestion: {query}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Fallback response
            if language == 'fi':
                return f"Anteeksi, kohtasin teknisen ongelman. Löysin kuitenkin nämä herkut sinulle: {', '.join([item['candy']['name'] for item in context_candies[:2]])} 🍭"
            else:
                return f"Sorry, I encountered a technical issue. However, I found these treats for you: {', '.join([item['candy']['name'] for item in context_candies[:2]])} 🍭"

    async def process_query_with_steps(self, query: str, language: str = 'en') -> Dict[str, Any]:
        """Process a query through the complete RAG pipeline with detailed step information."""
        start_time = time.time()
        steps = []

        # Step 1: Query Processing
        step_start = time.time()
        processed_query = query.lower().strip()
        tokens = processed_query.split()
        stop_words = ['the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by']
        filtered_tokens = [token for token in tokens if token not in stop_words]
        step_time = time.time() - step_start

        steps.append({
            "step": "query_processing",
            "title": self.translations["query_processing"],
            "description": {
                "en": f"🔍 PROCESSING: Your query '{query}' is being analyzed and prepared for embedding generation.",
                "fi": f"🔍 KÄSITTELY: Kyselyäsi '{query}' analysoidaan ja valmistellaan vektorointia varten."
            },
            "data": {
                "original_query": query,
                "processed_query": processed_query,
                "tokenization": {
                    "raw_tokens": tokens,
                    "filtered_tokens": filtered_tokens,
                    "removed_stop_words": [t for t in tokens if t in stop_words],
                    "token_count": len(filtered_tokens)
                },
                "preprocessing_steps": [
                    "1. Case normalization (toLowerCase())",
                    "2. Whitespace trimming",
                    "3. Tokenization by whitespace",
                    "4. Stop-word filtering",
                    "5. Prepared for OpenAI embedding"
                ],
                "language": language
            },
            "processing_time": step_time
        })

        # Step 2: Query Embedding
        step_start = time.time()
        query_embedding = self._generate_query_embedding(processed_query)
        step_time = time.time() - step_start

        steps.append({
            "step": "query_embedding",
            "title": self.translations["query_embedding"],
            "description": {
                "en": f"🧠 EMBEDDING: Converting your query to a 1536-dimensional vector using OpenAI's text-embedding-3-small model.",
                "fi": f"🧠 VEKTOROINTI: Muunnetaan kyselysi 1536-ulotteiseksi vektoriksi OpenAI:n text-embedding-3-small mallilla."
            },
            "data": {
                "model_info": {
                    "model": "text-embedding-3-small",
                    "provider": "OpenAI",
                    "dimensions": 1536,
                    "max_sequence_length": 8191
                },
                "embedding_vector": {
                    "magnitude": float(np.linalg.norm(query_embedding)),
                    "sample_values": query_embedding[:10],
                    "dimensions": len(query_embedding)
                },
                "vector_properties": {
                    "min_value": float(min(query_embedding)),
                    "max_value": float(max(query_embedding)),
                    "mean": float(np.mean(query_embedding)),
                    "std_dev": float(np.std(query_embedding))
                },
                "semantic_encoding": f"Query encoded into high-dimensional semantic space representing meaning and context"
            },
            "processing_time": step_time
        })

        # Step 3: Vector Search
        step_start = time.time()
        similar_candies = self._search_similar_candies(query_embedding, top_k=3)
        step_time = time.time() - step_start

        top_matches = []
        for item in similar_candies:
            candy = item['candy']
            top_matches.append({
                "rank": item['rank'],
                "candy_name": candy['name'],
                "category": candy['category'],
                "cosine_similarity": item['similarity'],
                "similarity_explanation": f"Cosine similarity: {item['similarity']:.3f}",
                "matched_concepts": candy['flavors'][:2]  # Top flavor concepts
            })

        steps.append({
            "step": "vector_search",
            "title": self.translations["vector_search"],
            "description": {
                "en": f"🎯 SEARCH: Finding most similar candies using cosine similarity in 1536D vector space.",
                "fi": f"🎯 HAKU: Etsitään samankaltaisimpia makeisia käyttäen kosinisamankaltaisuutta 1536D vektoriavaruudessa."
            },
            "data": {
                "search_algorithm": {
                    "method": "Cosine Similarity",
                    "formula": "cos(θ) = (A·B) / (||A|| × ||B||)",
                    "database_size": len(self.candies),
                    "vector_dimensions": 1536
                },
                "top_matches": top_matches,
                "similarity_distribution": {
                    "highest_score": max([item['similarity'] for item in similar_candies]),
                    "average_score": np.mean([item['similarity'] for item in similar_candies])
                },
                "vector_space_analysis": f"Semantic similarity computed in OpenAI's embedding space"
            },
            "processing_time": step_time
        })

        # Step 4: Context Preparation
        step_start = time.time()
        context_text = "\n".join([f"- {item['candy']['name']}: {item['candy']['description']}" for item in similar_candies])
        step_time = time.time() - step_start

        steps.append({
            "step": "context_preparation",
            "title": self.translations["context_preparation"],
            "description": {
                "en": f"📋 CONTEXT: Preparing retrieved candy information for OpenAI prompt injection.",
                "fi": f"📋 KONTEKSTI: Valmistellaan haetut makeistiedot OpenAI-kehotteen syöttämistä varten."
            },
            "data": {
                "context_window": {
                    "total_tokens": len(context_text.split()),
                    "max_context_length": 4096,
                    "utilization": f"{(len(context_text.split()) / 4096 * 100):.1f}%",
                    "chunks_included": len(similar_candies)
                },
                "context_structure": [
                    {
                        "candy_name": item['candy']['name'],
                        "similarity_rank": item['rank'],
                        "token_count": len(item['candy']['description'].split()),
                        "metadata": f"Sweetness: {item['candy']['sweetness']}/10"
                    }
                    for item in similar_candies
                ],
                "context_preview": context_text[:200] + "..." if len(context_text) > 200 else context_text
            },
            "processing_time": step_time
        })

        # Step 5: AI Generation
        step_start = time.time()
        final_answer = self._generate_ai_response(query, similar_candies, language)
        step_time = time.time() - step_start

        steps.append({
            "step": "ai_generation",
            "title": self.translations["ai_generation"],
            "description": {
                "en": f"✨ GENERATION: OpenAI GPT-3.5-turbo generating contextual response using retrieved candy information.",
                "fi": f"✨ GENEROINTI: OpenAI GPT-3.5-turbo generoi kontekstuaalisen vastauksen käyttäen haettuja makeistietoja."
            },
            "data": {
                "generation_model": {
                    "model": "gpt-3.5-turbo",
                    "provider": "OpenAI",
                    "max_tokens": 150,
                    "temperature": 0.7
                },
                "prompt_engineering": {
                    "system_prompt": "Friendly candy store expert providing contextual responses",
                    "context_injection": "Retrieved candy information injected as context",
                    "response_strategy": "Informative, fun, 2-3 sentences with emojis"
                },
                "output_analysis": {
                    "character_count": len(final_answer),
                    "word_count": len(final_answer.split()),
                    "sources_referenced": len(similar_candies),
                    "generation_method": "Real OpenAI API call with context"
                }
            },
            "processing_time": step_time
        })

        total_time = time.time() - start_time

        return {
            "query": query,
            "language": language,
            "steps": steps,
            "final_answer": {
                "en": final_answer if language == 'en' else final_answer,
                "fi": final_answer if language == 'fi' else final_answer
            },
            "total_time": total_time,
            "candies_found": [item['candy'] for item in similar_candies]
        }

    async def get_all_candies(self) -> List[Dict[str, Any]]:
        """Return all available candies."""
        return self.candies

    async def reset_demo(self) -> Dict[str, str]:
        """Reset the demo state."""
        return {"status": "reset", "message": "Demo reset successfully"} 