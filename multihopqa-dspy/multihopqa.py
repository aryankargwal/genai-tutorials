import requests
from dsp import LM
from dspy.datasets import HotPotQA
import dspy
from dsp.utils import deduplicate

class CustomLMClient(LM):
    def __init__(self, model, api_key):
        self.model = model
        self.api_key = api_key
        self.base_url = "https://proxy.tune.app/chat/completions"
        self.history = []
        self.kwargs = {}  # Initialize kwargs here

    def basic_request(self, prompt: str, **kwargs):
        headers = {
            "Authorization": f"{self.api_key}",
            "Content-Type": "application/json"
        }

        # Store kwargs for later access (as expected by the ChainOfThought module)
        self.kwargs.update(kwargs)

        # Define the request payload, including necessary parameters
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are TuneStudio, answer the question based on the context given to you."},
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.9),
            "max_tokens": kwargs.get("max_tokens", 100),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.2),
            "stream": kwargs.get("stream", False)
        }

        # Make the POST request
        response = requests.post(self.base_url, headers=headers, json=data)
        response_data = response.json()

        # Save the prompt and response history
        self.history.append({"prompt": prompt, "response": response_data, "kwargs": kwargs})

        # Return the raw response data for further processing
        return response_data

    def __call__(self, prompt, **kwargs):
        response = self.basic_request(prompt, **kwargs)
        
        # Extract the generated text from the correct field in the response structure
        try:
            completions = [result["message"]["content"] for result in response["choices"]]
        except KeyError:
            raise ValueError(f"Unexpected response structure: {response}")
        
        return completions
    
custom_lm = CustomLMClient(model='qwen/qwen-2.5-72b', api_key='YOUR_API_KEY')
colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
dspy.settings.configure(lm=custom_lm, rm=colbertv2_wiki17_abstracts)

# Load the dataset.
dataset = HotPotQA(train_seed=1, train_size=20, eval_seed=2023, dev_size=50, test_size=0)

# Tell DSPy that the 'question' field is the input. Any other fields are labels and/or metadata.
trainset = [x.with_inputs('question') for x in dataset.train]
devset = [x.with_inputs('question') for x in dataset.dev]

len(trainset), len(devset)

# Defining Simplified Baleen
class SimplifiedBaleen(dspy.Module):
    def __init__(self, lm_client, passages_per_hop=3, max_hops=1):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.max_hops = max_hops
        self.lm_client = lm_client  # Store the LM client instance

    def generate_query(self, context: list[str], question, **kwargs) -> str:
        # Create a search query based on the question and context
        query = f"{question} Context: {' '.join(context)}"
        return query

    def generate_answer(self, context: list[str], question, **kwargs) -> str:
        # Create a prompt that combines context and question
        context_str = " ".join(context)
        prompt = f"Given the following information: {context_str} \n\nAnswer the question: {question}"
        
        # Now pass this prompt to the generative model
        response = self.lm_client(prompt, **kwargs)  # Use your CustomLMClient instance
        answer = response[0]  # Get the first response

        return answer

    def forward(self, question, **kwargs):
        context = []

        for _ in range(self.max_hops):
            query = self.generate_query(context=context, question=question, **kwargs)
            passages = self.retrieve(query).passages
            context = deduplicate(context + passages)

        answer = self.generate_answer(context=context, question=question, **kwargs)
        return dspy.Prediction(context=context, answer=answer)

# Initialize and pass kwargs correctly
temperature = 0.9  # or any other value
max_tokens = 100

# Ask any question you like to this simple RAG program.
my_question = "What position on the Billboard Top 100 did Alison Moyet's late summer hit achieve?"

# Get the prediction. This contains `pred.context` and `pred.answer`.
uncompiled_baleen = SimplifiedBaleen(lm_client=custom_lm)  # uncompiled (i.e., zero-shot) program

# Pass in temperature and other parameters
pred = uncompiled_baleen(my_question, temperature=temperature, max_tokens=max_tokens)

# Print the contexts and the answer.
print(f"Question: {my_question}")
print(f"Predicted Answer: {pred.answer}")
print(f"Retrieved Contexts (truncated): {[c[:200] + '...' for c in pred.context]}")
