import asyncio
import json
import time
from typing import List, Dict, Any, Tuple
import logging
import os
from pathlib import Path

import chromadb
from chromadb.config import Settings
import openai
from sentence_transformers import SentenceTransformer
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.client = None
        self.collection = None
        self.embedding_model = None
        self.candies_data = []
        
        # OpenAI API key (you'll need to set this)
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Translations for UI
        self.translations = {
            "query_processing": {
                "en": "Processing Your Query",
                "fi": "Kyselyn Käsittely"
            },
            "query_embedding": {
                "en": "Converting Query to Vector",
                "fi": "Kyselyn Vektorointi"
            },
            "vector_search": {
                "en": "Searching Candy Database",
                "fi": "Karkkitietokannan Haku"
            },
            "context_preparation": {
                "en": "Preparing Context",
                "fi": "Kontekstin Valmistelu"
            },
            "ai_generation": {
                "en": "Generating AI Response",
                "fi": "AI-vastauksen Generointi"
            }
        }

    async def initialize(self):
        """Initialize the RAG service with vector database and sample data"""
        try:
            # Initialize ChromaDB
            self.client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory="./chroma_db"
            ))
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Load candy data
            await self._load_candy_data()
            
            # Create or get collection
            self.collection = self.client.get_or_create_collection(
                name="candy_store",
                metadata={"description": "AI Candy Store knowledge base"}
            )
            
            # Populate vector database if empty
            if self.collection.count() == 0:
                await self._populate_vector_db()
            
            logger.info("RAG service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG service: {str(e)}")
            raise

    async def _load_candy_data(self):
        """Load sample candy data"""
        self.candies_data = [
            {
                "id": "1",
                "name": "Rainbow Gummy Bears",
                "name_fi": "Sateenkaaren Karhukarkit",
                "description": "Colorful, chewy gummy bears with fruity flavors. These delightful treats come in five different flavors: strawberry (red), orange (orange), lemon (yellow), apple (green), and grape (purple). Made with real fruit juice and natural colors.",
                "description_fi": "Värikkäitä, pureskeltavia karhunmuotoisia karkkeja hedelmäisillä mauilla. Nämä ihanat herkut tulevat viidessä eri mausa: mansikka (punainen), appelsiini (oranssi), sitruuna (keltainen), omena (vihreä) ja rypäle (violetti). Valmistettu aidosta hedelmämehusta ja luonnollisista väreistä.",
                "sweetness": 8,
                "category": "Gummy",
                "category_fi": "Kumimaiset",
                "price": 2.99,
                "ingredients": ["glucose syrup", "sugar", "gelatin", "fruit juice", "natural flavors", "natural colors"],
                "allergens": ["may contain traces of nuts"]
            },
            {
                "id": "2", 
                "name": "Chocolate Dreams",
                "name_fi": "Suklaa Unet",
                "description": "Rich, creamy milk chocolate bars with a smooth, velvety texture. Made from premium Belgian cocoa beans, these bars melt perfectly in your mouth. Each bar contains 70% cocoa for the perfect balance of sweetness and depth.",
                "description_fi": "Rikas, kermainen maitosuklaa joka sulaa suussa. Valmistettu premium belgialaisisita kaakaopavuista. Jokainen levy sisältää 70% kaakaota täydellisen makeus ja syvyys tasapainon saavuttamiseksi.",
                "sweetness": 7,
                "category": "Chocolate",
                "category_fi": "Suklaa", 
                "price": 4.99,
                "ingredients": ["cocoa beans", "milk powder", "sugar", "cocoa butter", "vanilla extract"],
                "allergens": ["contains milk", "may contain nuts"]
            },
            {
                "id": "3",
                "name": "Sour Space Crystals", 
                "name_fi": "Happamat Avaruuskiteet",
                "description": "Ultra-sour candy crystals that pack a punch! These crystalline treats start extremely sour and gradually become sweet. Perfect for sour candy lovers who want an intense flavor experience. Available in cosmic flavors like meteor berry and alien apple.",
                "description_fi": "Erittäin happamia karkkikiteitä jotka ovat voimakkaita! Nämä kiteisét herkut alkavat erittäin happamina ja muuttuvat vähitellen makeiksi. Täydellisiä happamuuskarkkien ystäville jotka haluavat intensiivisen makuelämyksen. Saatavilla kosmisissa mauissa kuten meteorimarja ja avaruusomena.",
                "sweetness": 3,
                "category": "Sour",
                "category_fi": "Happamat",
                "price": 3.49,
                "ingredients": ["citric acid", "sugar", "natural flavors", "artificial colors", "malic acid"],
                "allergens": ["none"]
            },
            {
                "id": "4",
                "name": "Fluffy Cloud Marshmallows",
                "name_fi": "Pörröiset Pilvivaahtokarkit", 
                "description": "Light, airy marshmallows that feel like eating sweet clouds. These premium marshmallows are perfectly roasted and have a golden exterior with a soft, gooey center. Great for camping, hot chocolate, or eating straight from the bag.",
                "description_fi": "Kevyitä, ilmavia vaahtokarkkeja jotka tuntuvat kuin söisi makeita pilviä. Nämä premium vaahtokarkit ovat täydellisesti paahdettuja ja niissä on kullanvärinen ulkokuori pehmeän, tahmaisen keskustan kanssa. Loistavia retkeilyyn, kuumaan suklaaseen tai syötäväksi suoraan pussista.",
                "sweetness": 9,
                "category": "Marshmallow", 
                "category_fi": "Vaahtokarkit",
                "price": 2.49,
                "ingredients": ["sugar", "corn syrup", "gelatin", "vanilla extract", "salt"],
                "allergens": ["may contain traces of eggs"]
            },
            {
                "id": "5",
                "name": "Tropical Fruit Explosion",
                "name_fi": "Trooppinen Hedelmäräjähdys",
                "description": "A vibrant mix of tropical fruit-flavored hard candies. Experience the taste of paradise with mango, pineapple, coconut, passion fruit, and guava flavors. Each piece is individually wrapped and bursts with authentic tropical taste.",
                "description_fi": "Elävä sekoitus trooppisia hedelmiä maistavia kovia karkkeja. Koe paratiisin maku mangon, ananaksen, kookoksen, passionhedelmän ja guaijan mauilla. Jokainen pala on erikseen kääritty ja pursuaa aitoa trooppista makua.",
                "sweetness": 6,
                "category": "Hard Candy",
                "category_fi": "Kovat Karkit", 
                "price": 3.99,
                "ingredients": ["sugar", "corn syrup", "natural fruit flavors", "citric acid", "artificial colors"],
                "allergens": ["none"]
            }
        ]

    async def _populate_vector_db(self):
        """Populate the vector database with candy data"""
        documents = []
        metadatas = []
        ids = []
        
        for candy in self.candies_data:
            # Create searchable text for both languages
            en_text = f"{candy['name']} - {candy['description']} Category: {candy['category']} Sweetness: {candy['sweetness']}/10"
            fi_text = f"{candy['name_fi']} - {candy['description_fi']} Kategoria: {candy['category_fi']} Makeus: {candy['sweetness']}/10"
            
            # Add English version
            documents.append(en_text)
            metadatas.append({**candy, "language": "en", "search_text": en_text})
            ids.append(f"{candy['id']}_en")
            
            # Add Finnish version  
            documents.append(fi_text)
            metadatas.append({**candy, "language": "fi", "search_text": fi_text})
            ids.append(f"{candy['id']}_fi")
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents)
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Added {len(documents)} documents to vector database")

    async def process_query_with_steps(self, query: str, language: str = "en") -> Dict[str, Any]:
        """Process query through RAG pipeline with step-by-step visualization"""
        steps = []
        start_time = time.time()
        
        # Step 1: Query Processing
        step_start = time.time()
        processed_query = await self._process_query(query, language)
        step_time = time.time() - step_start
        
        steps.append({
            "step": "query_processing",
            "title": self.translations["query_processing"],
            "description": {
                "en": f"Processing your question: '{query}' and preparing it for the AI system.",
                "fi": f"Käsitellään kysymyksesi: '{query}' ja valmistellaan se AI-järjestelmälle."
            },
            "data": {
                "original_query": query,
                "processed_query": processed_query,
                "language": language
            },
            "processing_time": step_time
        })
        
        # Step 2: Query Embedding
        step_start = time.time()
        query_embedding = await self._create_embedding(processed_query)
        step_time = time.time() - step_start
        
        steps.append({
            "step": "query_embedding", 
            "title": self.translations["query_embedding"],
            "description": {
                "en": "Converting your question into a mathematical vector that the AI can understand and search with.",
                "fi": "Muunnetaan kysymyksesi matemaattiseksi vektoriksi jonka AI voi ymmärtää ja hakea."
            },
            "data": {
                "embedding_dimensions": len(query_embedding),
                "embedding_sample": query_embedding[:5].tolist()  # Show first 5 dimensions
            },
            "processing_time": step_time
        })
        
        # Step 3: Vector Search
        step_start = time.time()
        search_results = await self._vector_search(query_embedding, language)
        step_time = time.time() - step_start
        
        steps.append({
            "step": "vector_search",
            "title": self.translations["vector_search"], 
            "description": {
                "en": "Searching through our candy database to find the most relevant information for your question.",
                "fi": "Haetaan karkkitietokannastamme kysymykseesi liittyvintä tietoa."
            },
            "data": {
                "results_found": len(search_results),
                "top_matches": [
                    {
                        "candy_name": result["name"] if language == "en" else result["name_fi"],
                        "similarity_score": round(result["similarity"], 3),
                        "category": result["category"] if language == "en" else result["category_fi"]
                    }
                    for result in search_results[:3]
                ]
            },
            "processing_time": step_time
        })
        
        # Step 4: Context Preparation
        step_start = time.time() 
        context = await self._prepare_context(search_results, language)
        step_time = time.time() - step_start
        
        steps.append({
            "step": "context_preparation",
            "title": self.translations["context_preparation"],
            "description": {
                "en": "Organizing the relevant candy information to help the AI provide you with the best answer.",
                "fi": "Järjestellään relevanttia karkkitietoa auttamaan AI:ta antamaan sinulle parhaan vastauksen."
            },
            "data": {
                "context_length": len(context),
                "candies_included": len(search_results)
            },
            "processing_time": step_time
        })
        
        # Step 5: AI Generation
        step_start = time.time()
        final_answer = await self._generate_answer(query, context, language)
        step_time = time.time() - step_start
        
        steps.append({
            "step": "ai_generation",
            "title": self.translations["ai_generation"],
            "description": {
                "en": "Using AI to generate a helpful and accurate answer based on our candy knowledge.",
                "fi": "Käytetään AI:ta hyödyllisen ja tarkan vastauksen luomiseen karkkitietomme perusteella."
            },
            "data": {
                "answer_length": len(final_answer[language]),
                "sources_used": len(search_results)
            },
            "processing_time": step_time
        })
        
        return {
            "steps": steps,
            "final_answer": final_answer
        }

    async def _process_query(self, query: str, language: str) -> str:
        """Process and clean the user query"""
        # Simple processing - in a real app you might do more sophisticated NLP
        return query.strip().lower()

    async def _create_embedding(self, text: str) -> np.ndarray:
        """Create embedding for the query"""
        await asyncio.sleep(0.1)  # Simulate processing time
        return self.embedding_model.encode([text])[0]

    async def _vector_search(self, query_embedding: np.ndarray, language: str, top_k: int = 5) -> List[Dict]:
        """Search the vector database for relevant candies"""
        await asyncio.sleep(0.2)  # Simulate processing time
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where={"language": language}
        )
        
        search_results = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0], 
            results['metadatas'][0], 
            results['distances'][0]
        )):
            # Convert distance to similarity (higher is better)
            similarity = 1 / (1 + distance)
            
            search_results.append({
                **metadata,
                "similarity": similarity,
                "rank": i + 1
            })
        
        return search_results

    async def _prepare_context(self, search_results: List[Dict], language: str) -> str:
        """Prepare context from search results"""
        await asyncio.sleep(0.1)  # Simulate processing time
        
        context_parts = []
        for result in search_results:
            name = result["name"] if language == "en" else result["name_fi"]
            description = result["description"] if language == "en" else result["description_fi"] 
            category = result["category"] if language == "en" else result["category_fi"]
            
            context_parts.append(
                f"Candy: {name}\n"
                f"Category: {category}\n" 
                f"Description: {description}\n"
                f"Sweetness Level: {result['sweetness']}/10\n"
                f"Price: ${result['price']}\n"
                f"---"
            )
        
        return "\n".join(context_parts)

    async def _generate_answer(self, query: str, context: str, language: str) -> Dict[str, str]:
        """Generate AI answer using the context"""
        await asyncio.sleep(0.5)  # Simulate AI processing time
        
        # System prompts for different languages
        system_prompts = {
            "en": """You are a friendly AI assistant working at a magical candy store. 
            Use the provided candy information to answer questions about candies in a fun, enthusiastic way.
            Be helpful and informative while maintaining a playful tone.
            If you don't find relevant information in the context, say so politely.""",
            
            "fi": """Olet ystävällinen AI-avustaja joka työskentelee taikuriksi karkkikaupassa.
            Käytä annettuja karkkitietoja vastataksesi kysymyksiin karkeista hauskalla, innostuneella tavalla.  
            Ole avulias ja informatiivinen säilyttäen leikkisän sävyn.
            Jos et löydä relevanttia tietoa kontekstista, sano niin kohteliaasti."""
        }
        
        user_prompts = {
            "en": f"Question: {query}\n\nCandy Information:\n{context}\n\nPlease provide a helpful answer about candies based on the information above.",
            "fi": f"Kysymys: {query}\n\nKarkkitieto:\n{context}\n\nAnna hyödyllinen vastaus karkeista yllä olevan tiedon perusteella."
        }
        
        try:
            # Try OpenAI first
            if openai.api_key:
                response = await self._call_openai(system_prompts[language], user_prompts[language])
                return {language: response}
        except Exception as e:
            logger.warning(f"OpenAI call failed: {e}, using fallback")
        
        # Fallback response
        fallback_responses = {
            "en": f"Based on our candy collection, I found some great options for your question '{query}'. "
                  f"Let me tell you about our most relevant candies that might interest you! "
                  f"Our selection includes various sweet treats with different flavors and textures.",
            "fi": f"Karkkivalikoimimme perusteella löysin hyviä vaihtoehtoja kysymykseesi '{query}'. "
                  f"Kerron sinulle relevanteimmista karkeistamme jotka saattavat kiinnostaa sinua! "
                  f"Valikoimaamme kuuluu erilaisia makeisia eri mauilla ja tekstuureilla."
        }
        
        return {language: fallback_responses[language]}

    async def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    async def get_all_candies(self):
        """Get all candy data for display"""
        return self.candies_data

    async def reset(self):
        """Reset the demo state"""
        logger.info("Demo reset requested")
        # Could clear any temporary state here if needed
        return True 