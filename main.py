


from typing import Union
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def transform_schedule(input_schedule):
    transformed_schedule = {}
    app_name = input_schedule["app_name"]
    
    for entry in input_schedule["schedule"]:
        start, end = entry["slot"].split("-")
        day = input_schedule["days"][0]  # Assuming only one day is provided
        
        for group in entry["groups"]:
            group_name = group["group_name"]
            sources = group["sources"]
            
            if app_name not in transformed_schedule:
                transformed_schedule[app_name] = {}
            if day not in transformed_schedule[app_name]:
                transformed_schedule[app_name][day] = {}
            
            transformed_group = {
                "sources": sources,
                "slots": [{"start": start, "end": end}]
            }
            transformed_schedule[app_name][day][group_name] = transformed_group
            
    return transformed_schedule

# Input schema from your example
input_schema = {
    "app_name": "person_tresspassing",
    "schedule": [
        {
            "slot": "10:00-11:30",
            "groups": [
                {
                    "group_name": "group_name_1",
                    "sources": [
                        {
                            "source_id": "687655678",
                            "source_name": "sensor2",
                            "source_type": "iot",
                            "source_subtype": "temperature"
                        },
                        {
                            "source_id": "08765432",
                            "source_name": "camera1",
                            "source_type": "camera",
                            "source_subtype": None
                        }
                    ]
                },
                {
                    "group_name": "group_name_2",
                    "sources": [
                        {
                            "source_id": "08765435",
                            "source_name": "camera2",
                            "source_type": "camera",
                            "source_subtype": None
                        }
                    ]
                }
            ]
        }
    ],
    "days": ["monday"]
}

# Transform the input schema
transformed_output = transform_schedule(input_schema)

# Print the transformed output
print(transformed_output)



