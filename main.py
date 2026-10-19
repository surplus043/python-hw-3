import time, asyncio
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel): #вводные данные для запроса, требование Pydantic в условии
    numbers: list
    delays: list

class CalcRes(BaseModel):
    number: int
    square: int
    delay: float
    time: float

class CalcFinal(BaseModel):
    results: list
    total_time: float
    parallel_faster_than_sequential: bool

app = FastAPI()

async def execute_calculation(number: int, delay: float) -> CalcRes:
    #принимает число для возведения в квадрат и задержку
    t1 = time.perf_counter()
    
    #подсчет и ожидание
    result = number*number
    await asyncio.sleep(delay) #нельзя использовать time.sleep() т.к. иначе оно останавливает все исполнение 
    
    #считаем время окончания работы и возвращаем результат
    t2=time.perf_counter()
    return {
        "number":number,
        "square":result,
        "delay":delay,
        "time":round(t2-t1,2)
    }

    
#API
@app.post("/calculate")
async def create_item(item: Item) -> CalcFinal:
    #запустить подсчет общего исполнения
    t1 = time.perf_counter()
    
    #вызываем асинхронную функциюю для всех значений
    l=[]
    for i in range(item.delays):
        l.append(execute_calculation(item.numbers[i],item.delays[i]))
    
    #теперь ожидаем каждый результат
    res = await asyncio.gather(l)
    t2=time.perf_counter()
    #возврат результатов с доп. подсчетами результатов работы
    total_time=round(t2-t1,2)
    return CalcFinal(
        results=res,
        total_time=total_time,
        parallel_faster_than_sequential=sum(item.delays) > total_time
    )
    