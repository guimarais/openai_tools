import pandas as pd
import json

def tool_schema(filename):
    # Read the CSV file
    df = pd.read_csv(filename)
    
    tools = []
    
    # Group by function name to handle multiple parameters per function
    for name, group in df.groupby('name'):
        tool = {
            "type": group.iloc[0]['type'],
            "name": name,
            "description": group.iloc[0]['description'],
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
        
        # Add all parameters for this function
        for _, row in group.iterrows():
            param_name = row['param_name']
            tool["parameters"]["properties"][param_name] = {
                "type": row['param_type'],
                "description": row['param_description']
            }
            
            if row['param_required']:
                tool["parameters"]["required"].append(param_name)
        
        tools.append(tool)
    
    return tools