from dotenv import load_dotenv
from openai import OpenAI
import json 

load_dotenv()

client = OpenAI()

# 1. Define a list of callable tools for the model
tools = [
    {
        "type": "function",
        "name": "get_horoscope",
        "description": "Get today's horoscope for an astrological sign.",
        "parameters": {
            "type": "object",
            "properties": {
                "sign": {
                    "type": "string",
                    "description": "An astrological sign like Taurus or Aquarius",
                },
            },
            "required": ["sign"],
        },
    },
    {
        "type": "function",
        "name": "get_file",
        "description": "Reads and prints a file's content to the STDOUT.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The path to the file to read like 'fname.txt'",
                },
            },
            "required": ["filename"],
        },
    },


]

def get_horoscope(sign):
    return f"{sign}: Next Tuesday you will befriend a baby otter."

def get_file(path_dict):
    with open(path_dict['filename'], 'r') as file:
        content = file.read()
    print(content)
    return content

# Create a running input list we will add to over time
input_list = [
    {"role": "user", "content": "What are the contents of the 'files/test.md' file? Print just the contents."}
]


# 2. Prompt the model with tools defined
response = client.responses.create(
    model="gpt-4",
    tools=tools,
    input=input_list,
)

# Save function call outputs for subsequent requests
input_list += response.output

for item in response.output:
    if item.type == "function_call":
        if item.name == "get_horoscope":
            # 3. Execute the function logic for get_horoscope
            horoscope = get_horoscope(json.loads(item.arguments))
            
            # 4. Provide function call results to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "horoscope": horoscope
                })
            })
        if item.name == "get_file":
            # 3. Execute the function logic for get_horoscope
            content = get_file(json.loads(item.arguments))
            
            # 4. Provide function call results to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "file": content
                })
            })



print("Final input:")
print(input_list)

response = client.responses.create(
    model="gpt-4",
    instructions="What are the contents of the test.md file?",
    tools=tools,
    input=input_list,
)

# 5. The model should be able to give a response!
print("Final output:")
print(response.model_dump_json(indent=2))
print("\n" + response.output_text)

#def main():
#    print("Hello from openai-tools!")


#if __name__ == "__main__":
#    main()
