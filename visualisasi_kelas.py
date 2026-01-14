import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("ml_dataset.csv")
LABEL_COL = "is_fix_like"

counts = df[LABEL_COL].value_counts().sort_index()

plt.figure()
counts.plot(kind="bar")
plt.title("Distribusi Kelas Bug-Fix vs Non Bug-Fix")
plt.xlabel("Class (0 = Non Bug-Fix, 1 = Bug-Fix)")
plt.ylabel("Jumlah Data")
plt.tight_layout()
plt.savefig("distribusi_kelas_bar.png")
plt.show()

plt.figure()
counts.plot(kind="pie", autopct="%.1f%%")
plt.title("Proporsi Kelas Dataset")
plt.ylabel("")
plt.tight_layout()
plt.savefig("distribusi_kelas_pie.png")
plt.show()
