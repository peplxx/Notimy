from fastapi import FastAPI
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware

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
@app.get("/test_orders")
async def test():
    return [
        {
            'title': 'BAZZAR',
            'description': 'Бургер Дмитрий',
            'color': 'gradients.gradientPinkGreen'
        },
        {
            'title': 'BAZZAR-test-123-123',
            'description': 'Бургер Дмитрий BEBRA',
            'color': 'gradients.gradientPinkGreen'
        },

    ]

run(app, host="0.0.0.0", port=5000)
