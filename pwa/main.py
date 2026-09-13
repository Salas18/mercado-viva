from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client


SUPABASE_URL = "https://grgiokbgquwxvavwcynu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdyZ2lva2JncXV3eHZhdndjeW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzMjUyMjcsImV4cCI6MjEwNDkwMTIyN30.lBL4boniEtfN0ASyjVAmNFGrtxmXlliNPdKUrNQ0Srg" 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

class DevolucionRequest(BaseModel):
    order_id: str
    motivo: str
    monto_devolucion: float
    pin_supervisor: str = None

@app.get("/pedidos/{order_id}")
def buscar_pedido(order_id: str):
    response = supabase.table("pedidos").select("*").eq("id_pedido", order_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Pedido no encontrado en la nube.")
        
    pedido = response.data[0]
    if pedido["estado"] == "Devuelto":
        raise HTTPException(status_code=400, detail="Bloqueo antifraude: El pedido ya fue devuelto.")
        
    return pedido

@app.post("/devoluciones")
def procesar_devolucion(req: DevolucionRequest):
    pedido_res = supabase.table("pedidos").select("*").eq("id_pedido", req.order_id).execute()
    if not pedido_res.data:
        raise HTTPException(status_code=404, detail="Pedido no existe.")
        
    # Regla estricta: PIN para montos altos
    if req.monto_devolucion >= 500000 and req.pin_supervisor != "7777":
        raise HTTPException(status_code=403, detail="Monto alto. PIN de supervisor incorrecto.")

    supabase.table("pedidos").update({"estado": "Devuelto"}).eq("id_pedido", req.order_id).execute()
    
    return {"status": "success", "mensaje": "Transacción aprobada en base de datos central."}