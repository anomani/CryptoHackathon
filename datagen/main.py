from openai import OpenAI
import gradio as gr

# Initialize the OpenAI client
client = OpenAI()

# Upload the social media data
file = client.files.create(
    file=open("social_media_data.csv", "rb"),
    purpose='assistants'
)

# Create an assistant
assistant = client.beta.assistants.create(
    name="Data visualizer",
    instructions="You are a crypto advisor bot specialized for altcoins. You will analyze a CSV file with information scraped from Twitter and other social media sites. Provide insights based on the data.",
    model="gpt-4-turbo-preview",
    tools=[{"type": "code_interpreter"}],
    file_ids=[file.id]
)

assistant_id = assistant.id

def query_crypto_bot(user_input):
    # Create a thread
    thread = client.beta.threads.create()

    # Add the user's message to the thread
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_input)

    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)

    # Wait for the run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == 'completed':
            break

    # Retrieve and return the latest message from the assistant
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    # Ensure to parse the last response correctly
    response = messages.data[0].content[0].text.value
    return response

# Gradio interface setup
demo = gr.Interface(fn=query_crypto_bot, inputs="text", outputs="text", title="Crypto Advisor Bot")

# Launch the interface with sharing enabled
demo.launch(share=True)
