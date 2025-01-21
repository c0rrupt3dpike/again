from fastapi import FastAPI

app = FastAPI()



@app.get("/")
async def root():
    return{"message: sup fam"}

@app.get("/buses/{buses_id}")
async def bus(buses_id):
    buspath = {"1": "Goes to Kapchagai",
       "2": "Goes to Opera",
       "3": "Goes nahui(Chimkent)"
       }
    if buses_id not in buspath.keys():
        return{"message": "Совсем башкой тронулся"}
    return{f"Where goes {buses_id}": buspath[buses_id]}