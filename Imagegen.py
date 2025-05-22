import replicate
import os
from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from .env file


replicate_api_token = os.getenv("REPLICATE_API_KEY")

replicate_client = replicate.Client(api_token=replicate_api_token)


def generate_comic_images(
    script: str,
    topic: str,
    style: str = "comic book, vibrant colors, cartoon",
    panel_format: str = "6-panel strip",
    grade_level: str = "middle school"
) -> list[str]:
    panel_texts = extract_panel_descriptions(script)
    image_urls: list[str] = []

    for i, panel in enumerate(panel_texts):
        prompt = (f"""
            Comic strip panel {i+1} on '{topic}' for {grade_level} students. 
            Panel description: {panel} 
            Style: {style}, format: {panel_format}
                  """
        )

        output = replicate_client.run(
            "stability-ai/sdxl:610dddf033f10431b1b55f24510b6009fcba23017ee551a1b9afbc4eec79e29c",
            input={
                "width": 768,
                "height": 768,
                "prompt": prompt,
                "refine": "expert_ensemble_refiner",
                "scheduler": "KarrasDPM",
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "high_noise_frac": 0.7,
                "prompt_strength": 0.85,
                "num_inference_steps": 40
            }
        )


        

        print(output)

        # Unwrap the FileOutput into a string URL
        if isinstance(output, list) and output:
            result = output[0]
            # Most Replicate FileOutputs have a `.url` attribute
            if hasattr(result, "url"):
                image_urls.append(result.url)
            else:
                # Fallback to string conversion
                image_urls.append(str(result))
        else:
            image_urls.append("Error generating image")

    return image_urls

def extract_panel_descriptions(script: str) -> list:
    """
    Extract panel descriptions from the comic script.
    Assumes each panel is prefixed with 'Panel X:'.
    """
    import re
    panels = re.findall(r"Panel \d+:\s*(.*)", script)
    return panels











