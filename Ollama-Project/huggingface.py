# Import necessary libraries
import torch
from transformers import pipeline  # For text tasks (alternative: specific model classes)
from diffusers import StableDiffusionPipeline  # For image generation
from PIL import Image
import os
from diffusers import DiffusionPipeline
from datasets import load_dataset
import soundfile as sf
from IPython.display import Audio

# # Step 1: Configuration
# MODEL_TYPE = "image_generation"  # Options: "text_generation", "image_generation", etc.
# MODEL_ID = "runwayml/stable-diffusion-v1-5"  # Example for image generation
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # Auto-detect GPU or CPU
# OUTPUT_DIR = "outputs"  # Directory to save results

# # Step 2: Load the model
# def load_model(model_type: str, model_id: str, device: str):
#     """Load a Hugging Face model based on the task type."""
#     try:
#         print(f"Loading {model_type} model: {model_id} on {device}...")
        
#         if model_type == "text_generation":
#             model = pipeline("text-generation", model=model_id, device=0 if device == "cuda" else -1)
#         elif model_type == "image_generation":
#             model = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
#             model = model.to(device)
#         else:
#             raise ValueError(f"Unsupported model type: {model_type}")
        
#         print("Model loaded successfully!")
#         return model
#     except Exception as e:
#         print(f"Error loading model: {e}")
#         return None

# # Step 3: Process input and generate output
# def generate_output(model, model_type: str, input_data: str):
#     """Generate output based on model type and input."""
#     if model is None:
#         print("Model not loaded. Cannot generate output.")
#         return None
    
#     try:
#         if model_type == "text_generation":
#             output = model(input_data, max_length=100, num_return_sequences=1)[0]["generated_text"]
#             print(f"Generated text: {output}")
#             return output
#         elif model_type == "image_generation":
#             output = model(input_data, num_inference_steps=50, guidance_scale=7.5).images[0]
#             print("Image generated successfully!")
#             return output
#         else:
#             raise ValueError(f"Unsupported model type: {model_type}")
#     except Exception as e:
#         print(f"Error generating output: {e}")
#         return None

# # Step 4: Save or display the output
# def save_output(output, model_type: str, output_name: str, output_dir: str = OUTPUT_DIR):
#     """Save the generated output to a file."""
#     if output is None:
#         print("No output to save.")
#         return
    
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     output_path = os.path.join(output_dir, f"{output_name}.{ 'txt' if model_type == 'text_generation' else 'png' }")
    
#     try:
#         if model_type == "text_generation":
#             with open(output_path, "w", encoding="utf-8") as f:
#                 f.write(output)
#             print(f"Text saved to {output_path}")
#         elif model_type == "image_generation":
#             output.save(output_path)
#             print(f"Image saved to {output_path}")
#             output.show()  # Optional: Display the image
#     except Exception as e:
#         print(f"Error saving output: {e}")

# # Step 5: Main execution
# def main():
#     # Load the model
#     model = load_model(MODEL_TYPE, MODEL_ID, DEVICE)
    
#     if model:
#         # Example input
#         if MODEL_TYPE == "text_generation":
#             input_data = "Tell me a story about a dragon."
#             output_name = "dragon_story"
#         elif MODEL_TYPE == "image_generation":
#             input_data = "A vibrant pop-art style dragon flying over a city"
#             output_name = "dragon_image"
        
#         # Generate output
#         output = generate_output(model, MODEL_TYPE, input_data)
        
#         # Save the output
#         save_output(output, MODEL_TYPE, output_name)

# # Run main directly
# main()


def analyze_sentiment(text: str):
    """
    Analyze the sentiment of the given text using a pre-trained model.
    Args:
        text (str): The input text to analyze.
    Returns:
        dict: The sentiment analysis result with label and score.
    """
    classifier = pipeline("sentiment-analysis", device=0,trust_remote_code=False, verify=False)
    result = classifier(text)
    return result[0]
text = "I'm super excited to be on the way to LLM mastery!"
result = analyze_sentiment(text)
print(result)


def named_entity_Recognition(text:str):
    classifier = pipeline("ner", grouped_entities=True,trust_remote_code=False, verify=False)
    result = classifier(text)
    return result

text = "Conor is calling John"
print(named_entity_Recognition(text))


def answer_question(question: str, context: str) -> str:
    question_answerer = pipeline("question-answering",trust_remote_code=False, verify=False)
    result = question_answerer(question=question, context=context)
    return result['answer']

print(answer_question(
    "Who was the 44th president of the United States?",
    "Barack Obama was the 44th president of the United States."
))


def summarize_text(text: str, max_length: int = 50, min_length: int = 25) -> str:
    summarizer = pipeline("summarization",trust_remote_code=False, verify=False)
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

text = """
The Hugging Face transformers library is an incredibly versatile and powerful tool for natural language processing (NLP).
It allows users to perform a wide range of tasks such as text classification, named entity recognition, and question answering, among others.
It's an extremely popular library that's widely used by the open-source data science community.
It lowers the barrier to entry into the field by providing Data Scientists with a productive, convenient way to work with transformer models.
"""
print(summarize_text(text))


def translate_to_french(text: str) -> str:
    translator = pipeline("translation_en_to_fr",trust_remote_code=False, verify=False)
    result = translator(text)
    return result[0]['translation_text']

print(translate_to_french("The Data Scientists were amazed by the Hugging Face pipeline API."))



def translate_to_spanish(text: str) -> str:
    translator = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es",trust_remote_code=False, verify=False)
    result = translator(text)
    return result[0]['translation_text']
print(translate_to_spanish("The Data Scientists were amazed by the Hugging Face pipeline API."))


def classify_text(text: str, candidate_labels: list) -> dict:
    classifier = pipeline("zero-shot-classification",trust_remote_code=False, verify=False)
    result = classifier(text, candidate_labels=candidate_labels)
    return result

print(classify_text(
    "Hugging Face's Transformers library is amazing!",
        ["technology", "sports", "politics"]
    ))


def generate_text(prompt: str) -> str:
    generator = pipeline("text-generation",trust_remote_code=False, verify=False)
    result = generator(prompt)
    return result[0]['generated_text']
print(generate_text(
        "If there's one thing I want you to remember about using Hugging Face pipelines, it's"
    ))


def generate_image(prompt: str) -> None:
    image_gen = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2",
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16"
    ).to(device)
    
    image = image_gen(prompt=prompt).images[0]
    image.show()
generate_image(
        "A class of Data Scientists learning about AI, in the surreal style of Salvador Dali"
    )


def generate_audio(text: str, speaker_index: int = 7306) -> None:
    synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts",trust_remote_code=False, verify=False)
    
    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    speaker_embedding = torch.tensor(embeddings_dataset[speaker_index]["xvector"]).unsqueeze(0)
    
    speech = synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})
    
    sf.write("speech.wav", speech["audio"], samplerate=speech["sampling_rate"])
    display(Audio("speech.wav"))
    
generate_audio(
        "Hi to an artificial intelligence engineer, on the way to mastery!"
    )













