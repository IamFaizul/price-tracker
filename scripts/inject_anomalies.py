import numpy as np
from src.db.connection import get_connection
from src.model.autoencoder import prepare_sequences
from src.model.inference import load_model, get_reconstruction_error

def inject_anomalies(prices: list, anomaly_rate: float = 0.1) -> tuple:
    """
    Inject synthetic anomalies into a price sequence.
    Returns modified prices and anomaly indices.
    """
    prices = prices.copy()
    anomaly_indices = []
    n = len(prices)
    num_anomalies = max(1, int(n * anomaly_rate))
    
    indices = np.random.choice(range(6, n), size=num_anomalies, replace=False)
    
    for idx in indices:
        change = np.random.choice([-1, 1]) * np.random.uniform(0.3, 0.5)
        prices[idx] = prices[idx] * (1 + change)
        anomaly_indices.append(idx)
    
    return prices, sorted(anomaly_indices)

def evaluate():
    model, min_val, max_val = load_model()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT product_id FROM price_history")
    product_ids = [row["product_id"] for row in cursor.fetchall()]
    
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    
    THRESHOLD = 0.213
    
    for pid in product_ids:
        cursor.execute(
            "SELECT price FROM price_history WHERE product_id = ? ORDER BY scraped_at ASC",
            (pid,)
        )
        prices = [row["price"] for row in cursor.fetchall()]
        if len(prices) < 7:
            continue
        
        injected_prices, anomaly_indices = inject_anomalies(prices)
        
        seqs_normal = prepare_sequences(prices, window_size=7)
        seqs_injected = prepare_sequences(injected_prices, window_size=7)
        
        for i, (seq_n, seq_a) in enumerate(zip(seqs_normal, seqs_injected)):
            is_anomaly_window = any(idx <= i + 6 and idx >= i for idx in anomaly_indices)
            
            error = get_reconstruction_error(model, seq_a.tolist(), min_val, max_val)
            predicted_anomaly = error > THRESHOLD
            
            if is_anomaly_window and predicted_anomaly:
                true_positives += 1
            elif is_anomaly_window and not predicted_anomaly:
                false_negatives += 1
            elif not is_anomaly_window and predicted_anomaly:
                false_positives += 1
            else:
                true_negatives += 1
    
    conn.close()
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    print(f"True Positives:  {true_positives}")
    print(f"False Positives: {false_positives}")
    print(f"True Negatives:  {true_negatives}")
    print(f"False Negatives: {false_negatives}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")

if __name__ == "__main__":
    evaluate()