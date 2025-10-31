import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar archivo
df = pd.read_csv('Data_recovery.csv', sep=';', header=None)

# Transponer y usar la primera fila como encabezado
df = df.T
df.columns = df.iloc[0]
df = df.drop(0).reset_index(drop=True)

# Convertir a formato largo (melt)
id_vars = ['IHC', 'TUBO', 'Mouse #', 'Age (P#)', 'Time', 'Row', 'Exp', 'Stereocilia']
value_vars = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']

df_melted = df.melt(id_vars=id_vars, value_vars=value_vars,
                    var_name='Distance (%)', value_name='Grey value')

# Convertir columnas numéricas
df_melted['Grey value'] = pd.to_numeric(df_melted['Grey value'], errors='coerce')
df_melted['Distance (%)'] = df_melted['Distance (%)'].astype(str).str.replace('%', '', regex=False)
df_melted['Distance (%)'] = pd.to_numeric(df_melted['Distance (%)'], errors='coerce')

cond_a = (
    (df_melted['Row'] == '1') &
    (df_melted['Exp'] == '12') &
    (df_melted['TUBO'] == 'No')
)
df_filtered = df_melted.loc[cond_a]

palette_grey = sns.color_palette("Greys", n_colors=5)
palette_grey = [palette_grey[-1]] + palette_grey[:-1]

sns.scatterplot(
    data=df_filtered,
    x='Distance (%)',
    y='Grey value',
    hue='Time',
    palette=palette_grey,
    alpha=0.7,
    s=60,
      # nombre de la leyenda
)

sns.lineplot(
    data=df_filtered,
    x='Distance (%)',
    y='Grey value',
    hue='Time',
    palette=palette_grey,
    estimator='mean',
    lw=2,
    legend=False,
    errorbar=None,
)


cond_b = (
    (df_melted['Row'] == '1') &
    (df_melted['Exp'] == '12') &
    (df_melted['TUBO'] == 'Yes')
)
df_filteredB = df_melted.loc[cond_b]

palette_green = sns.color_palette("Greens", n_colors=5)
palette_green = [palette_green[-1]] + palette_green[:-1]

sns.scatterplot(
    data=df_filteredB,
    x='Distance (%)',
    y='Grey value',
    hue='Time',
    palette=palette_green,
    alpha=0.7,
    s=60,

)

sns.lineplot(
    data=df_filteredB,
    x='Distance (%)',
    y='Grey value',
    hue='Time',
    palette=palette_green,
    estimator='mean',
    lw=2,
    legend=False,
    errorbar=None,

)

sns.despine(top=True, right=True)

plt.ylim(0, 1.4)
plt.title("Perfil de intensidad a lo largo de la distancia \n "
          "para diferentes tiempos de tratamiento", fontsize=14)
plt.xlabel("Distancia [%]")
plt.ylabel("Intensidad de Fluorecencia")
plt.legend(
    title="Tiempo",
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    borderaxespad=0.5
)
ax = plt.gca()

# Texto fuera del eje (coordenadas en fracción del eje: (0..1))
ax.text(1.05, 0.2, 'Control',
        transform=ax.transAxes,
        fontsize=12,
        color='black')
ax.text(1.05, 0.15, 'Tubocurarine',
        transform=ax.transAxes,
        fontsize=12,
        color='green')
# Ajuste del layout para que no se corte la leyenda
plt.tight_layout(rect=[0, 0, 0.85, 1])
plt.tight_layout()
plt.savefig("Raw-data.png",
            dpi=300,
            bbox_inches='tight',
            transparent=True)
plt.show()