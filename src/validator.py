import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def generate_visual_report():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(base_dir, 'models', 'evaluation_report.pkl')
    output_dir = os.path.join(base_dir, 'relazione_grafici')

    if not os.path.exists(output_dir): os.makedirs(output_dir)
    report_data = joblib.load(report_path)

    # 1. Grafico Feature Importance (Il preferito di Polese per la XAI)
    # Prendiamo l'importanza media tra i 3 modelli
    all_imp = pd.DataFrame([data['importance'] for data in report_data.values()]).mean()
    plt.figure(figsize=(10, 7))
    all_imp.nlargest(15).sort_values().plot(kind='barh', color='#2C3E50', edgecolor='black')
    plt.title("Analisi delle Feature Determinanti (Global Importance)")
    plt.xlabel("Peso statistico nel processo decisionale")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'feature_importance.png'))

    # 2. Matrici di Confusione (Una per categoria)
    for cat, data in report_data.items():
        plt.figure(figsize=(8, 6))
        sns.heatmap(data['confusion_matrix'], annot=True, fmt='d', cmap='YlGnBu',
                    xticklabels=data['labels'], yticklabels=data['labels'])
        plt.title(f"Matrice di Confusione: {cat.upper()}")
        plt.ylabel("Classe Reale")
        plt.xlabel("Classe Predetta")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'cm_{cat}.png'))

    # 3. Tabella delle Metriche in LaTeX (Comoda da copiare e incollare!)
    with open(os.path.join(output_dir, 'metrics_table.tex'), 'w') as f:
        f.write("\\begin{tabular}{lcccc}\n\\toprule\n")
        f.write("Modello & Precision & Recall & F1-Score \\\\\n\\midrule\n")
        for cat, data in report_data.items():
            m = data['report']['weighted avg']
            f.write(f"{cat.capitalize()} & {m['precision']:.2f} & {m['recall']:.2f} & {m['f1-score']:.2f} \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}")

    print(f"✅ Grafici e tabelle LaTeX generati in: {output_dir}")


if __name__ == "__main__":
    generate_visual_report()