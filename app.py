from transformers import pipeline
import torch
import graphsignal

# The API key is provided via environment variable GRAPHSIGNAL_API_KEY
graphsignal.configure(deployment='banana-example-server')

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
    global model

    device = 0 if torch.cuda.is_available() else -1
    model = pipeline('fill-mask', model='bert-base-uncased', device=device)

# Inference is ran for every server call
# Reference your preloaded global model variable here.
@graphsignal.trace_function(options=graphsignal.TraceOptions(enable_profiling=True))
def inference(model_inputs:dict) -> dict:
    global model

    # Parse out your arguments
    prompt = model_inputs.get('prompt', None)
    if prompt == None:
        return {'message': "No prompt provided"}
    
    # Run the model
    result = model(prompt)

    # Return the results as a dictionary
    return result
