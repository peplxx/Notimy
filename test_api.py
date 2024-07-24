from fastapi import FastAPI
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware
import uuid
app = FastAPI()
# Define the origins that should be allowed to make requests (replace * with specific origins if needed)
origins = ["http://localhost:3000"]

# Add middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Add more methods if needed
    allow_headers=["*"],
)

bazzar = 'BAZZAR'
ids = [uuid.uuid1().__str__() for _ in range(10)]


x = []
for i in range(10):
    x += [{
            'id': ids[i],
            'title': bazzar,
            'description': 'Бургер Дмитрий',
            'color': 'gradients.gradientPinkGreen'
        }]
    x += [{
        'id': ids[i],
        'title': 'not green',
        'description': 'Бургер Дмитрий',
        'color': 'gradients.gradientPinkGreen'
        }]
@app.get("/test_orders")
async def test():
    return x
        # {
        #     'id': uuid.uuid4().__str__(),
        #     'title':  bazzar,
        #     'description': 'Бургер Дмитрий BEBRA',
        #     'color': 'gradients.gradientPinkGreen'
        # },
        # {
        #     'id': uuid.uuid4().__str__(),
        #     'title': bazzar,
        #     'description': 'Бургер Дмитрий',
        #     'color': 'gradients.gradientPinkGreen'
        # },
        # {
        #     'id': uuid.uuid4().__str__(),
        #     'title':  bazzar,
        #     'description': 'Бургер Дмитрий BEBRA',
        #     'color': 'gradients.gradientPinkGreen'
        # },
        # {
        #     'id': uuid.uuid4().__str__(),
        #     'title':  bazzar,
        #     'description': 'Бургер Дмитрий BEBRA',
        #     'color': 'gradients.gradientPinkGreen'
        # },


run(app, host="0.0.0.0", port=5000)
