import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette(debug=True)

@app.route('/search')
async def homepage(request):
    query = request.query_params.getlist('query')
    print(query)
    # g = group([
    # frobnicate.message(1, 2),
    # frobnicate.message(2, 3),
    # frobnicate.message(3, 4),
    # ]).run()
    return JSONResponse({'hello': query})
