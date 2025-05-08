import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io

def generate_pie_chart(file_counts):
    fig, ax = plt.subplots(figsize=(12, 10))

    # Prepare data
    labels = [k.replace('.xlsx', '').replace('.xls', '') for k in file_counts.keys()]
    sizes = list(file_counts.values())
    total = sum(sizes)
    colors = plt.cm.Set3.colors[:len(sizes)]
    explode = [0.05 for _ in sizes]

    # Plot pie chart
    wedges, _ = ax.pie(
        sizes,
        explode=explode,
        labels=None,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.3, edgecolor='white')
    )

    # Format legend labels
    legend_labels = [
        f"{label} → {count} ({(count/total)*100:.1f}%)"
        for label, count in zip(labels, sizes)
    ]

    # Add legend
    ax.legend(
        wedges,
        legend_labels,
        title="Conditions",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=14,
        title_fontsize=12
    )

    # Center label
    ax.text(0, 0, f"TOTAL\n{total}", ha='center', va='center',
            fontsize=14, fontweight='bold', color='#d50032')

    #ax.set_title("", fontsize=14, weight='bold')
    ax.axis('equal')  # Keep it circular

    # Save to buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf



def generate_spider_chart(file_counts):
    labels = [label.replace('.xlsx', '').replace('.xls', '') for label in file_counts.keys()]
    values = list(file_counts.values())
    total_vars = len(labels)

    # Radar chart requires values to be circular (first = last)
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, total_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))

    # Draw the outline
    ax.plot(angles, values, color='#d50032', linewidth=2, linestyle='solid')
    ax.fill(angles, values, color='#d50032', alpha=0.25)

    # Draw axes with labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)

    # Improve layout: radial labels and ticks
    ax.set_yticks([])
    ax.tick_params(pad=10)
    ax.grid(True, linestyle='--', linewidth=0.5, color='gray')

    # Title and center
    ax.set_title("File-wise Row Count Comparison", fontsize=14, weight='bold', pad=20)
    ax.set_rlabel_position(0)  # y-labels position

    # Fix layout cropping
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf
