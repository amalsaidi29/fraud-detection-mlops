"""
API Professionnelle de Détection de Fraude
Modèle: RandomForest (F1=0.828, Précision=97%, ROC-AUC=0.979)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime

# ==================== CONFIGURATION ====================
app = FastAPI(
    title="Fraud Detection API",
    description="API professionnelle pour détecter les fraudes de cartes bancaires",
    version="1.0.0"
)

# Charger le modèle
print("🚀 Démarrage de l'API...")
print("📦 Chargement du modèle RandomForest...")
MODEL = joblib.load("models/best_model.pkl")
print("✅ Modèle chargé (F1=0.828, Précision=97%)")

# Stats de monitoring
STATS = {
    "total_predictions": 0,
    "fraud_detected": 0,
    "start_time": datetime.now()
}

# ==================== MODÈLES DE DONNÉES ====================
class Transaction(BaseModel):
    """Transaction bancaire à analyser"""
    Time: float = 0.0
    V1: float = 0.0
    V2: float = 0.0
    V3: float = 0.0
    V4: float = 0.0
    V5: float = 0.0
    V6: float = 0.0
    V7: float = 0.0
    V8: float = 0.0
    V9: float = 0.0
    V10: float = 0.0
    V11: float = 0.0
    V12: float = 0.0
    V13: float = 0.0
    V14: float = 0.0
    V15: float = 0.0
    V16: float = 0.0
    V17: float = 0.0
    V18: float = 0.0
    V19: float = 0.0
    V20: float = 0.0
    V21: float = 0.0
    V22: float = 0.0
    V23: float = 0.0
    V24: float = 0.0
    V25: float = 0.0
    V26: float = 0.0
    V27: float = 0.0
    V28: float = 0.0
    Amount: float = 0.0

class PredictionResponse(BaseModel):
    """Réponse de prédiction"""
    is_fraud: bool
    probability: float
    confidence_level: str
    risk_score: int
    timestamp: str
    model_info: dict

# ==================== ENDPOINTS ====================

@app.get("/")
def home():
    """Page d'accueil de l'API"""
    return {
        "service": "Fraud Detection API",
        "model": "RandomForest",
        "f1_score": 0.828,
        "precision": 0.970,
        "status": "operational"
    }

@app.get("/health")
def health_check():
    """Health check pour Docker et monitoring"""
    uptime = (datetime.now() - STATS["start_time"]).total_seconds()
    return {
        "status": "healthy",
        "model": "RandomForest v5",
        "uptime_seconds": int(uptime),
        "predictions_made": STATS["total_predictions"]
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_fraud(transaction: Transaction):
    """
    Prédire si une transaction est frauduleuse
    
    Returns:
        - is_fraud: True si fraude détectée
        - probability: Probabilité de fraude (0-1)
        - confidence_level: HIGH/MEDIUM/LOW
        - risk_score: Score de risque (0-100)
    """
    try:
        # Convertir en DataFrame
        data = pd.DataFrame([transaction.dict()])
        
        # Prédiction
        prediction = int(MODEL.predict(data)[0])
        probability = float(MODEL.predict_proba(data)[0][1])
        
        # Calculer le niveau de confiance
        if probability > 0.8:
            confidence = "HIGH"
        elif probability > 0.5:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        # Score de risque (0-100)
        risk_score = int(probability * 100)
        
        # Mettre à jour les stats
        STATS["total_predictions"] += 1
        if prediction == 1:
            STATS["fraud_detected"] += 1
        
        # Log
        status = "🚨 FRAUDE" if prediction == 1 else "✅ OK"
        print(f"{status} | Prob={probability:.3f} | Amount={transaction.Amount}")
        
        return PredictionResponse(
            is_fraud=bool(prediction),
            probability=probability,
            confidence_level=confidence,
            risk_score=risk_score,
            timestamp=datetime.now().isoformat(),
            model_info={
                "name": "RandomForest",
                "version": "5",
                "f1_score": 0.828,
                "precision": 0.970
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

@app.get("/stats")
def get_statistics():
    """Statistiques de l'API (monitoring)"""
    fraud_rate = 0
    if STATS["total_predictions"] > 0:
        fraud_rate = STATS["fraud_detected"] / STATS["total_predictions"]
    
    uptime = (datetime.now() - STATS["start_time"]).total_seconds()
    
    return {
        "model": "RandomForest v5",
        "model_metrics": {
            "f1_score": 0.828,
            "precision": 0.970,
            "recall": 0.722,
            "roc_auc": 0.979
        },
        "api_stats": {
            "total_predictions": STATS["total_predictions"],
            "fraud_detected": STATS["fraud_detected"],
            "fraud_rate": f"{fraud_rate:.2%}",
            "uptime_hours": f"{uptime / 3600:.2f}h"
        },
        "start_time": STATS["start_time"].isoformat()
    }

@app.post("/batch_predict")
def batch_predict(transactions: list[Transaction]):
    """Prédiction en batch pour plusieurs transactions"""
    results = []
    
    for trans in transactions:
        data = pd.DataFrame([trans.dict()])
        prediction = int(MODEL.predict(data)[0])
        probability = float(MODEL.predict_proba(data)[0][1])
        
        results.append({
            "is_fraud": bool(prediction),
            "probability": probability,
            "amount": trans.Amount
        })
        
        STATS["total_predictions"] += 1
        if prediction == 1:
            STATS["fraud_detected"] += 1
    
    fraud_count = sum(1 for r in results if r["is_fraud"])
    
    return {
        "total_analyzed": len(transactions),
        "fraud_detected": fraud_count,
        "fraud_rate": f"{fraud_count / len(transactions):.2%}",
        "results": results
    }

# ==================== LANCEMENT ====================
if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("🚀 Lancement de l'API Fraud Detection")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)