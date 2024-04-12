from openai import OpenAI

client = OpenAI()

# Open social media data
file = client.files.create(
    file=open("social_media_data.csv", "rb"),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
    name="Data visualizer",
    instructions="You are a crypto advisor bot specialized for altcoins. You are going to be given a CSV file that has information scraped from twitter and other social media sites. Token, Date, Chain, Price (USD), User, Message, Sentiment Score. Given this data provide information given the users prompt. You are not going to be recommending investing solely providing interesting insights on the data. Usually, a sentiment score greater than 0.5 means that the coin is being talked about in a positive outlook",
    model="gpt-4-turbo-preview",
    tools=[{"type": "code_interpreter"}],
    file_ids=[file.id]
)

assistant_id = assistant.id
thread = client.beta.threads.create()

while True:
    # Prompt the user for input
    user_input = input('Please enter your query or type "exit" to quit: ')
    if user_input.lower() == 'exit':
        break

    # Add the user's message to the thread
    client.beta.threads.messages.create(thread_id=thread.id,
                                        role="user",
                                        content=user_input)
    print('Client made')

    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread.id,
                                          assistant_id=assistant_id)
    print('Run created')

    # Check if the Run requires action (function call)
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id,
                                                       run_id=run.id)
        if run_status.status == 'completed':
            break

    # Retrieve and return the latest message from the assistant
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value

    print(f"Assistant response: {response}")

print("Goodbye!")
