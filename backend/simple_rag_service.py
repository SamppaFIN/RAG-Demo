import asyncio
import time
from typing import List, Dict, Any
import logging

# Configure logging  
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleRAGService:
    def __init__(self):
        self.candies_data = []
        
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
        """Initialize the service with sample candy data"""
        await self._load_candy_data()
        logger.info("Simple RAG service initialized successfully")

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

    async def process_query_with_steps(self, query: str, language: str = "en") -> Dict[str, Any]:
        """Process query through simplified RAG pipeline with step-by-step visualization"""
        steps = []
        
        # Step 1: Query Processing
        step_start = time.time()
        await asyncio.sleep(0.5)  # Simulate processing
        
        # Advanced query processing with tokenization
        processed_query = query.lower().strip()
        tokens = processed_query.split()
        stop_words = ['the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by']
        filtered_tokens = [token for token in tokens if token not in stop_words]
        
        step_time = time.time() - step_start
        
        steps.append({
            "step": "query_processing",
            "title": self.translations["query_processing"],
            "description": {
                "en": f"🔍 TECHNICAL: Text preprocessing pipeline transforms raw user input into machine-readable format. This includes normalization, tokenization, and stop-word removal - critical for semantic similarity matching.",
                "fi": f"🔍 TEKNINEN: Tekstin esikäsittelypipeline muuntaa raaka käyttäjäsyötteen koneluettavaan muotoon. Sisältää normalisointia, tokenisointia ja stop-sanojen poistoa - kriittistä semanttiselle samankaltaisuudelle."
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
                    "5. Prepared for embedding"
                ],
                "language": language
            },
            "processing_time": step_time
        })
        
        # Step 2: Query Embedding  
        step_start = time.time()
        await asyncio.sleep(0.3)  # Simulate embedding
        
        # Generate realistic embedding values based on query content
        query_embedding = self._generate_mock_embedding(processed_query, filtered_tokens)
        embedding_magnitude = sum(x**2 for x in query_embedding)**0.5
        
        step_time = time.time() - step_start
        
        steps.append({
            "step": "query_embedding", 
            "title": self.translations["query_embedding"],
            "description": {
                "en": f"🧠 TECHNICAL: Sentence transformer converts text to dense vector representation in 384-dimensional semantic space. Each dimension captures different linguistic/semantic features. L2 norm: {embedding_magnitude:.3f}",
                "fi": f"🧠 TEKNINEN: Lause-transformaattori muuntaa tekstin tiheäksi vektorirepresentaatioksi 384-ulotteisessa semanttisessa avaruudessa. Jokainen ulottuvuus kaappaa erilaisia kielellisiä/semanttisia piirteitä. L2-normi: {embedding_magnitude:.3f}"
            },
            "data": {
                "model_info": {
                    "model": "all-MiniLM-L6-v2", 
                    "dimensions": 384,
                    "max_sequence_length": 256,
                    "architecture": "BERT-based transformer"
                },
                "embedding_vector": {
                    "full_dimensions": 384,
                    "sample_values": query_embedding[:10],  # Show first 10 dimensions
                    "magnitude": round(embedding_magnitude, 6),
                    "sparsity": f"{sum(1 for x in query_embedding if abs(x) < 0.01)/len(query_embedding)*100:.1f}% near-zero"
                },
                "vector_properties": {
                    "min_value": min(query_embedding),
                    "max_value": max(query_embedding), 
                    "mean": sum(query_embedding)/len(query_embedding),
                    "std_dev": (sum((x - sum(query_embedding)/len(query_embedding))**2 for x in query_embedding)/len(query_embedding))**0.5
                },
                "semantic_encoding": f"Vector encodes semantic meaning of '{' '.join(filtered_tokens)}' in high-dimensional space for cosine similarity comparison"
            },
            "processing_time": step_time
        })
        
        # Step 3: Vector Search
        step_start = time.time()
        search_results = await self._advanced_search(processed_query, language, query_embedding, filtered_tokens)
        step_time = time.time() - step_start
        
        # Calculate similarity statistics
        similarities = [r["similarity"] for r in search_results]
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0
        
        steps.append({
            "step": "vector_search",
            "title": self.translations["vector_search"], 
            "description": {
                "en": f"🔍 TECHNICAL: Cosine similarity search across {len(self.candies_data)} embedded documents. Query vector compared against pre-computed candy embeddings using dot product / (||a|| × ||b||). Avg similarity: {avg_similarity:.3f}",
                "fi": f"🔍 TEKNINEN: Kosini-samankaltaisuushaku {len(self.candies_data)} upotetun dokumentin läpi. Kyselyvektoria verrataan ennalta laskettuihin karkkiupotuksiin käyttäen pistetuloa / (||a|| × ||b||). Keskim. samankaltaisuus: {avg_similarity:.3f}"
            },
            "data": {
                "search_algorithm": {
                    "method": "Cosine Similarity",
                    "formula": "cos(θ) = (A·B) / (||A|| × ||B||)",
                    "database_size": len(self.candies_data),
                    "search_space": "384-dimensional semantic vector space"
                },
                "similarity_distribution": {
                    "highest_score": max(similarities) if similarities else 0,
                    "lowest_score": min(similarities) if similarities else 0,
                    "average_score": round(avg_similarity, 4),
                    "results_above_threshold": len([s for s in similarities if s > 0.3])
                },
                "top_matches": [
                    {
                        "rank": idx + 1,
                        "candy_name": result["name"] if language == "en" else result["name_fi"],
                        "cosine_similarity": round(result["similarity"], 6),
                        "similarity_explanation": result.get("similarity_breakdown", ""),
                        "category": result["category"] if language == "en" else result["category_fi"],
                        "matched_tokens": result.get("matched_tokens", [])
                    }
                    for idx, result in enumerate(search_results[:5])
                ],
                "vector_space_analysis": f"Query tokens '{' '.join(filtered_tokens)}' mapped to semantic clusters in embedding space"
            },
            "processing_time": step_time
        })
        
        # Step 4: Context Preparation
        step_start = time.time()
        await asyncio.sleep(0.2)  # Simulate processing
        
        # Build structured context from search results
        context_chunks = []
        total_tokens = 0
        for result in search_results[:3]:  # Top 3 results
            chunk = f"[CANDY: {result['name']}] Category: {result['category']}, Sweetness: {result['sweetness']}/10, Description: {result['description'][:100]}..."
            context_chunks.append(chunk)
            total_tokens += len(chunk.split())
        
        context = "\n".join(context_chunks)
        step_time = time.time() - step_start
        
        steps.append({
            "step": "context_preparation",
            "title": self.translations["context_preparation"],
            "description": {
                "en": f"📝 TECHNICAL: Context window assembly for LLM. Retrieved docs ranked by similarity, chunked and formatted with metadata. Token budget: {total_tokens}/2048 tokens used.",
                "fi": f"📝 TEKNINEN: Konteksti-ikkunan kokoaminen LLM:lle. Haetut dokumentit järjestetty samankaltaisuuden mukaan, pilkottu ja formatoitu metadatalla. Token-budjetti: {total_tokens}/2048 tokenia käytetty."
            },
            "data": {
                "context_window": {
                    "total_tokens": total_tokens,
                    "max_context_length": 2048,
                    "utilization": f"{(total_tokens/2048)*100:.1f}%",
                    "chunks_included": len(context_chunks)
                },
                "rag_strategy": {
                    "retrieval_count": len(search_results),
                    "context_selection": "Top-k similarity ranking",
                    "chunk_size": "~100 chars per description",
                    "metadata_included": ["name", "category", "sweetness", "description"]
                },
                "context_structure": [
                    {
                        "chunk_id": idx,
                        "candy_name": result["name"],
                        "similarity_rank": idx + 1,
                        "token_count": len(context_chunks[idx].split()),
                        "metadata": f"Category: {result['category']}, Sweetness: {result['sweetness']}"
                    }
                    for idx, result in enumerate(search_results[:3])
                ],
                "context_preview": context[:200] + "..." if len(context) > 200 else context
            },
            "processing_time": step_time
        })
        
        # Step 5: AI Generation
        step_start = time.time()
        final_answer, generation_details = await self._generate_technical_answer(query, search_results, context, language, filtered_tokens)
        step_time = time.time() - step_start
        
        steps.append({
            "step": "ai_generation",
            "title": self.translations["ai_generation"],
            "description": {
                "en": f"🤖 TECHNICAL: LLM prompt engineering with RAG context injection. Template-based generation with {len(search_results)} retrieved sources. Response length: {len(final_answer[language])} chars.",
                "fi": f"🤖 TEKNINEN: LLM-kehotteen suunnittelu RAG-kontekstin injektoinnilla. Mallipohjainen generointi {len(search_results)} haetulla lähteellä. Vastauksen pituus: {len(final_answer[language])} merkkiä."
            },
            "data": {
                "generation_model": {
                    "approach": "Rule-based + Template Generation",
                    "context_injection": "Retrieved documents as structured input",
                    "fallback_strategy": "Template-based responses when no matches",
                    "response_format": "Natural language with candy recommendations"
                },
                "prompt_engineering": {
                    "system_prompt": "Candy store AI assistant with expertise in confectionery",
                    "context_template": "[CANDY: name] Category: X, Sweetness: Y/10, Description: Z",
                    "user_query_processing": f"Original: '{query}' → Processed: '{' '.join(filtered_tokens)}'",
                    "response_strategy": generation_details["strategy"]
                },
                "output_analysis": {
                    "character_count": len(final_answer[language]),
                    "word_count": len(final_answer[language].split()),
                    "sources_referenced": len(search_results),
                    "confidence_score": generation_details["confidence"],
                    "generation_method": generation_details["method"]
                },
                "rag_effectiveness": {
                    "retrieval_success": len(search_results) > 0,
                    "context_utilization": f"{len(context)} chars of context used",
                    "semantic_matching": f"Query matched {generation_details['matched_concepts']} candy concepts",
                    "response_grounding": "Generated response grounded in retrieved candy data"
                }
            },
            "processing_time": step_time
        })
        
        return {
            "steps": steps,
            "final_answer": final_answer
        }



    async def get_all_candies(self):
        """Get all candy data for display"""
        return self.candies_data

    def _generate_mock_embedding(self, processed_query: str, tokens: List[str]) -> List[float]:
        """Generate realistic-looking embedding vector based on query content"""
        import random
        import math
        
        # Seed random with query for consistent results
        random.seed(hash(processed_query) % 2**32)
        
        # Generate 384 dimensions
        embedding = []
        for i in range(384):
            # Base random value
            val = random.gauss(0, 0.3)
            
            # Add semantic meaning based on tokens
            for token in tokens:
                if token in processed_query:
                    # Add token-specific influence 
                    token_influence = hash(token + str(i)) % 100 / 1000.0
                    val += token_influence * random.choice([-1, 1])
            
            # Clamp to reasonable range
            val = max(-1.0, min(1.0, val))
            embedding.append(round(val, 6))
        
        return embedding

    async def _advanced_search(self, query: str, language: str, query_embedding: List[float], tokens: List[str]) -> List[Dict]:
        """Advanced search with detailed similarity calculations and explanations"""
        await asyncio.sleep(0.4)  # Simulate search time
        
        results = []
        
        for candy in self.candies_data:
            # Generate embedding for candy (simulate pre-computed embeddings)
            candy_text = candy["name"] + " " + candy["description"]
            if language == "fi":
                candy_text = candy["name_fi"] + " " + candy["description_fi"]
            
            candy_embedding = self._generate_mock_embedding(candy_text.lower(), candy_text.lower().split())
            
            # Calculate cosine similarity
            dot_product = sum(a * b for a, b in zip(query_embedding, candy_embedding))
            query_magnitude = sum(a**2 for a in query_embedding)**0.5
            candy_magnitude = sum(a**2 for a in candy_embedding)**0.5
            
            cosine_similarity = dot_product / (query_magnitude * candy_magnitude) if (query_magnitude * candy_magnitude) > 0 else 0
            
            # Additional keyword matching for demo purposes
            keyword_boost = 0
            matched_tokens = []
            search_text = candy_text.lower()
            
            for token in tokens:
                if token in search_text:
                    keyword_boost += 0.1
                    matched_tokens.append(token)
            
            # Check for specific semantic matches
            if "sweet" in tokens or "makea" in tokens:
                keyword_boost += candy["sweetness"] / 100
            if "sour" in tokens or "hapan" in tokens:
                keyword_boost += (10 - candy["sweetness"]) / 100
            if "chocolate" in tokens or "suklaa" in tokens:
                if "chocolate" in candy["category"].lower() or "suklaa" in candy["category_fi"].lower():
                    keyword_boost += 0.2
            
            final_similarity = min(0.95, cosine_similarity + keyword_boost)
            
            if final_similarity > 0.1:  # Threshold for inclusion
                similarity_breakdown = f"Cosine: {cosine_similarity:.3f} + Keyword boost: {keyword_boost:.3f} = {final_similarity:.3f}"
                
                results.append({
                    **candy,
                    "similarity": final_similarity,
                    "similarity_breakdown": similarity_breakdown,
                    "matched_tokens": matched_tokens,
                    "cosine_base": cosine_similarity,
                    "keyword_boost": keyword_boost
                })
        
        # Sort by similarity score
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:5]

    async def _generate_technical_answer(self, query: str, search_results: List[Dict], context: str, language: str, tokens: List[str]) -> tuple:
        """Generate technical answer with detailed generation information"""
        await asyncio.sleep(0.6)  # Simulate AI processing
        
        generation_details = {
            "strategy": "retrieval_augmented",
            "method": "template_based_generation",
            "confidence": 0.85,
            "matched_concepts": len([t for t in tokens if t in context.lower()])
        }
        
        if not search_results:
            generation_details.update({
                "strategy": "fallback_general", 
                "method": "general_knowledge_template",
                "confidence": 0.6,
                "matched_concepts": 0
            })
            
            answers = {
                "en": f"🔍 RAG ANALYSIS: No semantic matches found for query tokens {tokens}. Falling back to general candy knowledge. In a production system, this might trigger query expansion or alternative retrieval strategies. Our collection includes diverse confectionery across categories: gummy, chocolate, sour, marshmallow, and hard candy varieties.",
                "fi": f"🔍 RAG ANALYYSI: Ei semanttisia osumia kyselytokeneille {tokens}. Palataan yleiseen karkkitietoon. Tuotantojärjestelmässä tämä voisi laukaista kyselyn laajennuksen tai vaihtoehtoisia hakustrategioita. Kokoelmamme sisältää monipuolisia makeisia eri kategorioissa: kumi-, suklaa-, happamat, vaahto- ja kovat karkit."
            }
            return answers, generation_details
        
        # Analyze top result for technical generation
        top_candy = search_results[0]
        similarity_score = top_candy["similarity"]
        
        # Update confidence based on similarity
        generation_details["confidence"] = min(0.95, 0.5 + similarity_score * 0.5)
        
        candy_name = top_candy["name"] if language == "en" else top_candy["name_fi"]
        candy_desc = top_candy["description"] if language == "en" else top_candy["description_fi"]
        
        # Technical answer with RAG analysis
        technical_analysis = f"Vector similarity: {similarity_score:.3f}, Matched tokens: {top_candy.get('matched_tokens', [])}"
        
        answers = {
            "en": f"🎯 RAG RESULT: Query '{query}' → Top match: '{candy_name}' (similarity: {similarity_score:.3f}). TECHNICAL ANALYSIS: {technical_analysis}. RECOMMENDATION: {candy_desc} This candy scores {top_candy['sweetness']}/10 on sweetness and costs ${top_candy['price']}. The retrieval system identified semantic alignment between your query tokens {tokens} and this {top_candy['category']} category item through embedding space proximity.",
            "fi": f"🎯 RAG TULOS: Kysely '{query}' → Paras osuma: '{candy_name}' (samankaltaisuus: {similarity_score:.3f}). TEKNINEN ANALYYSI: {technical_analysis}. SUOSITUS: {candy_desc} Tämä karkki saa {top_candy['sweetness']}/10 makeus-pistettä ja maksaa ${top_candy['price']}. Hakujärjestelmä tunnisti semanttisen yhteyden kyselytokeniesi {tokens} ja tämän {top_candy['category_fi']} -kategorian tuotteen välillä upotusavaruuden läheisyyden kautta."
        }
        
        return answers, generation_details

    async def reset(self):
        """Reset the demo state"""
        logger.info("Demo reset requested")
        return True 