from dotenv import load_dotenv
from openai import OpenAI
import json
from utils.tool_schema import tool_schema
from utils.tool_functions import get_horoscope
from utils.tool_functions import get_file
from utils.aux import extract_code_blocks

load_dotenv()

client = OpenAI()

# 1. Load tool schema
tools = tool_schema("./schema/from_sql.csv")

# Create a running input list we will add to over time
user_file_prompt ="""
                  What are the contents of the 'files/test.md' file?
                  Print just the contents.
                  DO not make additional comments.
                  """

input_list = [
    {"role": "user", "content": user_file_prompt}
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
            # 3. Execute the function logic for get_file
            content = get_file(json.loads(item.arguments))
            
            # 4. Provide function call results to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "file": content
                })
            })



#print("Final input:")
#print(input_list)

response = client.responses.create(
    model="gpt-4",
    instructions="What are the contents of the test.md file?",
    tools=tools,
    input=input_list,
)

# 5. The model should be able to give a response!
#print("Final output:")
#print(response.model_dump_json(indent=2))
print(response.output_text)

with open("./files/response_output.txt", "w") as f:
    f.write(response.output_text)

f.close()


#def main():
#    print("Hello from openai-tools!")


#if __name__ == "__main__":
#    main()
