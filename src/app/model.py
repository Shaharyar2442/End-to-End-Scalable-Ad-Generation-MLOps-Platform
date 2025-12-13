import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

class AdGenerator:
    def __init__(self):
        print("Loading T5-small model... (this may take a moment)")
        self.model_name = "t5-small"
        
        # ing tokenizer and model
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        
        # Ensuring that we are using CPU
        self.device = torch.device("cpu")
        self.model.to(self.device)
        print("Model loaded successfully on CPU.")

    def generate_ad(self, product_name, description): #Function to generate ad copy
        
        # Prompt Engineering by framing the task for the model T5
       
        input_text = f"write an advertisement for: {product_name}. Key features: {description}"
        
        # Tokenizing input
        input_ids = self.tokenizer.encode(
            input_text, 
            return_tensors="pt", 
            max_length=512, 
            truncation=True
        ).to(self.device)

        # Generating output
        # max_length=100 
        # num_beams=2 adds a little creativity search without being too slow
        outputs = self.model.generate(
            input_ids, 
            max_length=100, 
            num_beams=2, 
            early_stopping=True,
            no_repeat_ngram_size=2
        )

        # Decoding output
        ad_copy = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return ad_copy

if __name__ == "__main__":
    # Quick test of the AdGenerator
    generator = AdGenerator()
    sample_prod = "Retro Mechanical Keyboard"
    sample_desc = "Clicky blue switches, RGB lighting, vintage typewriter style."
    print(f"\n--- Input: {sample_prod} ---")
    print(f"Generated Ad: {generator.generate_ad(sample_prod, sample_desc)}")