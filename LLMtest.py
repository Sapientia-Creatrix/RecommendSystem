import vertexai
from vertexai.preview.language_models import TextGenerationModel
import pandas as pd

vertexai.init(project="tsmccareerhack2024-bsid-grp2")

fields = ['Course Name']
data = pd.read_csv("Coursera.csv", skipinitialspace=True, usecols=fields).head(512).to_markdown(index=False)

review = "Please tell me how many kinds of skills in this table and list at least 10 {expect ...} of them'"

prompt = '''
input: This table contains information about courses. The first row includes the table headers, while each subsequent row displays the corresponding data separated by the "|" symbol. And each row contains the specific skills that seperate from space
{data}

input: {review}
'''

def predict_large_language_model(
    model_name: str,
    temperature: float,
    max_output_tokens: int,
    top_p: float,
    top_k: int,
    content: str,
    tuned_model_name: str = "",
    ) :
    
    model = TextGenerationModel.from_pretrained(model_name)
    if tuned_model_name:
      model = model.get_tuned_model(tuned_model_name)
    response = model.predict(
        content,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        top_k=top_k,
        top_p=top_p,)
    return response.text

content = prompt.format(review=review, data=data)

response_text = predict_large_language_model(
    "text-bison@001", 
    temperature=0.2, 
    max_output_tokens=1024, 
    top_p=0.8, 
    top_k=1, 
    content=content
    )

print(response_text)