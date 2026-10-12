from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)

    return data


@app.get("/")
def hello():
    return{"message":"Patient Management System API"}



@app.get("/view")
def view():
    data=load_data()
    return data



@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(...,description="ID of the patient in the DB", example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient not found") 
    #return{"error":"Patient not found"}



@app.get("/sort")
def sort_patient(sort_on: str = Query(..., description="Sort on the basis of height, weight or Bmi"), order:str = Query("asc",description="sort in acs or dcsc order" )):

    vaild_feilds=["height","weight","bmi"]

    if sort_on not in vaild_feilds:
        raise HTTPException(status_code=400,detail=f"Invaild feild: Select from {vaild_feilds}")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail="Invaild Order: Select betn acs and desc")
    
    data=load_data()

    sort_order =  True if order == "desc" else False

    sorted_data=sorted(data.values(), key=lambda x:x.get(sort_on,0),reverse=sort_order)

    return sorted_data

