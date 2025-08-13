from fastapi import FastAPI
from pydantic import BaseModel
from module_1 import baseConverter
from module_2 import (
    binary_addition, binary_subtraction, binary_multiplication, binary_division,
    signed_binary_addition, signed_binary_subtraction, signed_binary_multiplication, signed_binary_division,
    ones_complement_addition, ones_complement_subtraction, ones_complement_multiplication, ones_complement_division,
    twos_complement_addition, twos_complement_subtraction, twos_complement_multiplication, twos_complement_division
)
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse  

app = FastAPI(
    title="DLD simulator",
    description="just a poor soul doing his assignments :(",
)

app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

#Schemas 

class NumberConversion(BaseModel):
    number: str
    from_base: int
    to_base: int

class BinaryOperation(BaseModel):
    binary1: str
    binary2: str
    num_bits: int
    operation: str  # "add", "subtract", "multiply", "divide"
    representation: str = "unsigned"  # "unsigned", "signed", "ones_complement", "twos_complement"

# Calling the api

@app.post("/convert")
async def convert_number(conversion: NumberConversion):
    try:
        return baseConverter(conversion)
    except ValueError as e:
        return {"error": str(e)}

@app.post("/binary/operation")
async def binary_operation(operation: BinaryOperation):
    try:
        op = operation.operation.lower()
        rep = operation.representation.lower()
        
        # Unsigned operations
        if rep == "unsigned":
            if op == "add":
                result = binary_addition(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "unsigned addition",
                    "result": result,
                    "representation": "unsigned"
                }
            elif op == "subtract":
                result = binary_subtraction(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "unsigned subtraction",
                    "result": result,
                    "representation": "unsigned"
                }
            elif op == "multiply":
                result = binary_multiplication(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "unsigned multiplication",
                    "result": result,
                    "result_bits": len(result),
                    "representation": "unsigned"
                }
            elif op == "divide":
                quotient, remainder = binary_division(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "unsigned division",
                    "quotient": quotient,
                    "remainder": remainder,
                    "representation": "unsigned"
                }
        
        # Signed (sign-magnitude) operations
        elif rep == "signed":
            if op == "add":
                result = signed_binary_addition(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "signed addition",
                    "result": result,
                    "representation": "sign-magnitude"
                }
            elif op == "subtract":
                result = signed_binary_subtraction(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "signed subtraction",
                    "result": result,
                    "representation": "sign-magnitude"
                }
            elif op == "multiply":
                result = signed_binary_multiplication(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "signed multiplication",
                    "result": result,
                    "result_bits": len(result),
                    "representation": "sign-magnitude"
                }
            elif op == "divide":
                quotient, remainder = signed_binary_division(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "signed division",
                    "quotient": quotient,
                    "remainder": remainder,
                    "representation": "sign-magnitude"
                }
        
        # 1's complement operations
        elif rep == "ones_complement":
            if op == "add":
                result = ones_complement_addition(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "1's complement addition",
                    "result": result,
                    "representation": "1's complement"
                }
            elif op == "subtract":
                result = ones_complement_subtraction(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "1's complement subtraction",
                    "result": result,
                    "representation": "1's complement"
                }
            elif op == "multiply":
                result = ones_complement_multiplication(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "1's complement multiplication",
                    "result": result,
                    "result_bits": len(result),
                    "representation": "1's complement"
                }
            elif op == "divide":
                quotient, remainder = ones_complement_division(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "1's complement division",
                    "quotient": quotient,
                    "remainder": remainder,
                    "representation": "1's complement"
                }
        
        # 2's complement operations
        elif rep == "twos_complement":
            if op == "add":
                result = twos_complement_addition(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "2's complement addition",
                    "result": result,
                    "representation": "2's complement"
                }
            elif op == "subtract":
                result = twos_complement_subtraction(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "2's complement subtraction",
                    "result": result,
                    "representation": "2's complement"
                }
            elif op == "multiply":
                result = twos_complement_multiplication(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "2's complement multiplication",
                    "result": result,
                    "result_bits": len(result),
                    "representation": "2's complement"
                }
            elif op == "divide":
                quotient, remainder = twos_complement_division(operation.binary1, operation.binary2, operation.num_bits)
                return {
                    "operation": "2's complement division",
                    "quotient": quotient,
                    "remainder": remainder,
                    "representation": "2's complement"
                }
        
        else:
            return {"error": "Invalid representation. Use 'unsigned', 'signed', 'ones_complement', or 'twos_complement'"}
        
        return {"error": "Invalid operation. Use 'add', 'subtract', 'multiply', or 'divide'"}
    except ValueError as e:
        return {"error": str(e)}

#Command to run the fastapi api "python main.py"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)