import numpy as np
from scipy import optimize 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

#Génération de la matrice A
def remplirMatriceA(m,n):
    
    #initialisation de la matrice par des 0
    A = np.zeros((m+n,m*n),dtype='int8')
    
    #remplissage de A_ub
    for i in range(m):
        pivot = i*n
        for j in range(m*n):
            if(j>=pivot and j<pivot+n):
                A[i][j]=1
    
    #remplissage de A_eq
    for i in range(m,n+m):
        pivot = i-m
        for j in range(m):
            A[i][j+pivot]=1
            pivot+=n-1
    
    return A

#résolution du problème
def calculSimplex(m,n,c,b_ub,b_eq):
    A = remplirMatriceA(m,n)
    A_ub =  A[:m,:]
    A_eq =  A[m:(m+n),:]
    return optimize.linprog(c,A_ub,b_ub,A_eq,b_eq,method='simplex',options={'disp':True})
"""
#nb de Sources #dispo
m =2
#nb de Destinations #demandes
n= 3
#size (n+m,n*m)=(5,6)  

#Les contraintes de dispo
#(m,1)
b_ub = np.array([50,20])

#Les contraintes des demandes
#(n,1)
b_eq = np.array([15,20,35])

#Vecteur Cout
#(1,n*m)
C = np.array([12,10,8,7,11,9])


res = calculSimplex(m,n,C,b_ub,b_eq)
"""

class Item(BaseModel):
    n: int
    m: int
    b_ub: list
    b_eq:list
    C:list
    #tax: Union[float, None] = None

#uvicorn main:app --reload 
app = FastAPI()

origins = [
    #"http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
   allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/solve')
def get_root(matrice : Item):
    opt = calculSimplex(matrice.m,matrice.n,matrice.C,matrice.b_ub,matrice.b_eq)
    #print(dict(res.items()))
    res = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in opt.items()}
    return res

@app.get("/")
def root():
    return {"msg" : "Hello world"}
