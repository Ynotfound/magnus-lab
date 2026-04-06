import time


if __name__ == "__main__":
    print("Starting mock training job...")
    for epoch in range(1, 11):
        # Simulate decreasing loss values with some variation
        loss = 1.0 - 0.05 * epoch
        val_loss = loss + 0.03

        # Print in format that matches our regex pattern
        print(f"Epoch {epoch}/10 - loss: {loss:.2f} - val_loss: {val_loss:.2f}")

        # Wait between epochs
        time.sleep(2)

    print("Mock training completed successfully")