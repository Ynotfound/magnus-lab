import time

def main():
    for epoch in range(1, 11):
        loss = 1.0 - 0.05 * epoch
        val_loss = loss + 0.03
        print(f"Epoch {epoch}/10 - loss: {loss:.2f} - val_loss: {val_loss:.2f}")
        time.sleep(2)

if __name__ == "__main__":
    main()