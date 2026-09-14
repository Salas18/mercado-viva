from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware

SUPABASE_URL = "https://grgiokbgquwxvavwcynu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdyZ2lva2JncXV3eHZhdndjeW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzMjUyMjcsImV4cCI6MjEwNDkwMTIyN30.lBL4boniEtfN0ASyjVAmNFGrtxmXlliNPdKUrNQ0Srg" 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DevolucionRequest(BaseModel):
    order_id: str
    motivo: str
    monto_devolucion: float
    pin_supervisor: str = None

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    
    response = supabase.table("usuarios").select("*").eq("username", req.username).execute()
    
    if not response.data:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
    usuario = response.data[0]
    
    if usuario["password_hash"] != req.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
    token_jwt = f"jwt-token-valido-{usuario['id_usuario']}"
    
    return {
        "status": "success",
        "token": token_jwt,
        "rol": usuario["rol"]
    }
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
        raise HTTPException(status_code=404, detail="Factura digital no encontrada en el sistema.")
            
    
    if req.monto_devolucion >= 500000 and req.pin_supervisor != "7777":
        raise HTTPException(status_code=403, detail="Autorización denegada. El PIN del supervisor es incorrecto.")

    
    supabase.table("pedidos").update({"estado": "Devuelto"}).eq("id_pedido", req.order_id).execute()
        

    if req.motivo == "buen_estado":
        try:
            
            inv_res = supabase.table("inventario").select("cantidad_disponible").eq("sku", "SKU-001").execute()
            
            if inv_res.data:
                cantidad_actual = inv_res.data[0]["cantidad_disponible"]
                nueva_cantidad = cantidad_actual + 1
                
                
                supabase.table("inventario").update({"cantidad_disponible": nueva_cantidad}).eq("sku", "SKU-001").execute()
        except Exception as e:

             pass
            
    return {"status": "success", "mensaje": "Transacción completada en Mercado Viva."}

@app.get("/")
def read_root():
    return {
        "sistema": "Mercado VIVA API",
        "estado": "Activo y corriendo en tiempo real"
    }