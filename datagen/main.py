from openai import OpenAI
import gradio as gr

# Initialize the OpenAI client
client = OpenAI()

# Open social media data
social_file = client.files.create(
    file=open("social_media_data.csv", "rb"),
    purpose='assistants'
)

txn_file = client.files.create(
    file=open("token_transactions.csv", "rb"),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
    name="Data visualizer",
    instructions="You are a crypto advisor bot specializing in altcoins or memecoins. You are going to be given two CSV files. One has information scraped from twitter and other social media sites with the following schema: Token, Date, Chain, Price (USD), User, Message, Sentiment Score. The other has data regarding transactions involving the memecoin at hand, with the following schema: Token,Date,Chain,Price (USD),Amount,BUY/SELL. You should expect questions regarding market sentiment and legitimacy of memecoins. You are not giving investing advice. You are providing interesting insights based on the data. Do not reveal specific data included in the datasets, but rather extract conceptual insights from them.",
    model="gpt-4-turbo-preview",
    tools=[{"type": "code_interpreter"}],
    file_ids=[txn_file.id, social_file.id]
)

assistant_id = assistant.id

def query_crypto_bot(user_input):
    Create a thread
    thread = client.beta.threads.create()

    # Add the user's message to the thread
    client.beta.threads.messages.create(thread_id=thread.id,
                                        role="user",
                                        content=user_input)
    #print('Client made')

    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread.id,
                                          assistant_id=assistant_id)
    #print('Run created')

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


# Launch the interface with sharing enabled
demo = gr.Interface(
    fn=query_crypto_bot,
    inputs=gr.Textbox(label="Enter Your Query", placeholder="Type here to ask about memecoins...", lines=2),
    outputs="text",
    title="Crypto Compass",
    description="Ask any question about the market sentiment and legitimacy of memecoins. No investment advice provided.",
    theme="huggingface",
    css="""
    body, html { background-color: #243E66; }
    .gradio-container { background-color: #243E66; }
    .input_text { background-color: #243E66; }
    .example-container .example {
        color: #243E66; 
    }

    """,
    examples=[["What is the current sentiment on Dogecoin?"],["Is Crypto Hot Dog a scam?"]]
)

demo.launch(share=True)
