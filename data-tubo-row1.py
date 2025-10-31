import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar archivo
df = pd.read_csv('Data_recovery.csv', sep=';', header=None)

# transponer
df = df.T

# usar la primera fila como encabezado
df.columns = df.iloc[0]
df = df.drop(0).reset_index(drop=True)

# convertir a formato largo ("melt")
# Esto deja tres columnas: variable (porcentaje), valor (grey value), y condiciones
id_vars = ['IHC', 'TUBO', 'Mouse #', 'Age (P#)', 'Time', 'Row', 'Exp']
value_vars = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']

df_melted = df.melt(id_vars=id_vars, value_vars=value_vars,
                    var_name='Distance (%)', value_name='Grey value')

# Asegurar que los valores sean numéricos
df_melted['Grey value'] = pd.to_numeric(df_melted['Grey value'], errors='coerce')
df_melted['Distance (%)'] = df_melted['Distance (%)'].str.replace('%', '').astype(float)

# Filtrar según condiciones
cond = (
    (df_melted['TUBO'] == 'Yes') &
    (df_melted['Mouse #'] == '1') &
    (df_melted['Row'] == '1') &
    (df_melted['Exp'] == '12')
)

df_filtered = df_melted.loc[cond]
df_filtered.to_csv('resultado_tubo_row1.tsv', sep='\t')

palette_base = sns.color_palette("Greens", n_colors=5)
palette = [palette_base[-1]] + palette_base[:-1]

sns.lineplot(
    data=df_filtered,
    x='Distance (%)',
    y='Grey value',
    hue='Time',
    marker='o',
    palette=palette,
)

#Eliminar leyenda
plt.legend().remove()

# Obtener el eje actual
ax = plt.gca()



# Etiquetar cada línea al final
for line, name in zip(ax.lines, df['Time'].unique()):
    x = line.get_xdata()[0]      # última coordenada x
    y = line.get_ydata()[0]      # última coordenada y
    ax.text(x - 3.7, y + 0.05, name,
            color=line.get_color(),
            va='center',
            fontsize=13,
            fontweight='bold',
            )

sns.despine(top=True, right=True)

plt.title('Análisis del gradiente de intensidad en función \n'
          'de la distancia normalizada')
plt.xlabel('Distancia [%]')
plt.ylabel('Intensidad de Fluorecencia')
plt.ylim(0, 1.2)
plt.annotate('Tubocurarine',
             xy=(50, 0.8),          # punto que quieres señalar (x, y)
             xytext=(60, 1.12),      # posición del texto
             color='green',fontsize=12
             )
plt.grid(False)
plt.savefig("graph_tubo_row1.png",
            dpi=300,
            bbox_inches='tight',
            transparent=True)
plt.show()