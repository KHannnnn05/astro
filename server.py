from fastapi import FastAPI

from db import add_main_data, get_rezult

app = FastAPI()

@app.post('/app/')
def post_index(full_name: str, date: str, address: str, time_zone: str = None):
    id = add_main_data(full_name, date, address, time_zone)
    return ({'id': id})

@app.get('/app/')
def get_index(id: int):
    rez = str(get_rezult(id))
    return(rez)