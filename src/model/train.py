import torch
import torch.nn as nn
import numpy as np
import os
from src.model.autoencoder import PriceAutoencoder, prepare_sequences, normalize
from src.db.connection import get_connection

def load_all_prices() -> list:
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT product_id FROM price_history")
    product_ids = [row["product_id"] for row in cursor.fetchall()]
    
    all_sequences = []
    for pid in product_ids:
        cursor.execute(
            "SELECT price FROM price_history WHERE product_id = ? ORDER BY scraped_at ASC",
            (pid,)
        )
        prices = [row["price"] for row in cursor.fetchall()]
        if len(prices) >= 7:
            seqs = prepare_sequences(prices, window_size=7)
            all_sequences.extend(seqs.tolist())
    
    conn.close()
    return all_sequences

def train():
    print("Loading data...")
    sequences = load_all_prices()
    
    if len(sequences) == 0:
        print("Not enough data. Need at least 7 price points per product.")
        return
    
    data = np.array(sequences)
    data, min_val, max_val = normalize(data)
    
    
    tensor_data = torch.FloatTensor(data)
    
    # Model, loss, optimizer
    model = PriceAutoencoder(input_size=7)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    print(f"Training on {len(sequences)} sequences...")
    
    # Training loop
    epochs = 200
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        output = model(tensor_data)
        loss = criterion(output, tensor_data)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}/{epochs} | Loss: {loss.item():.6f}")
    
    
    os.makedirs("data", exist_ok=True)
    torch.save({
        "model_state": model.state_dict(),
        "min_val": min_val,
        "max_val": max_val
    }, "data/autoencoder.pth")
    
    print("Model saved to data/autoencoder.pth")

if __name__ == "__main__":
    train()