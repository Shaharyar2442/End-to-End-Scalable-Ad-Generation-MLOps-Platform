import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

class AdGenerator:
    def __init__(self):
        # We switch to FLAN-T5-small (Same size ~300MB, but smarter at instructions)
        self.model_name = "google/flan-t5-small"
        print(f"Loading {self.model_name}... (this may take a moment)")
        
        # Load tokenizer and model
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        
        self.device = torch.device("cpu")
        self.model.to(self.device)
        print("Model loaded successfully on CPU.")

    def generate_ad(self, product_name, description):
        # 1. Prompt Engineering:
        input_text = (
            f"Write a catchy, exciting social media ad for a product named '{product_name}'. "
            f"It features {description}. "
            "Use emojis and hashtags!"
        )
        
        # Tokenize
        input_ids = self.tokenizer.encode(
            input_text, 
            return_tensors="pt", 
            max_length=512, 
            truncation=True
        ).to(self.device)

        # 2. Creative Generation Parameters (The Secret Sauce)
        outputs = self.model.generate(
            input_ids, 
            max_length=150,             
            min_length=30,              # Force it to say more than one sentence
            do_sample=True,             # ENABLE CREATIVITY!
            temperature=0.9,            # 0.9 = Creative, 0.5 = Boring
            top_k=50,                   # Pick from top 50 likely words
            top_p=0.95,                 # Nucleus sampling (removes nonsense)
            repetition_penalty=1.2,     # Don't repeat the same word twice
            num_return_sequences=1
        )

        # Decode
        ad_copy = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return ad_copy

if __name__ == "__main__":
    # Quick Test
    generator = AdGenerator()
    print(generator.generate_ad("Future Sneakers", "Self lacing, neon lights"))