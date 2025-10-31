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
id_vars = ['IHC', 'TUBO', 'Mouse #', 'Age (P#)', 'Time', 'Row', 'Exp', 'Stereocilia']
value_vars = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']

df_melted = df.melt(id_vars=id_vars, value_vars=value_vars,
                    var_name='Distance (%)', value_name='Grey value')

# Asegurar que los valores sean numéricos
df_melted['Grey value'] = pd.to_numeric(df_melted['Grey value'], errors='coerce')
df_melted['Distance (%)'] = df_melted['Distance (%)'].str.replace('%', '').astype(float)

# sns.set_theme(style="darkgrid")
g=sns.displot(data=df_melted,
            x="Row",
            col="Age (P#)",
            row="Time",
            hue="TUBO",
            palette=["#AAAAAA", "#00FF00"],
            multiple="dodge",
            binwidth=2,
            height=3,
            facet_kws=dict(margin_titles=True),
            )

g.set_axis_labels("Fila", "Conteo", fontsize=16)  # Tamaño de etiquetas de ejes
g.set_titles(row_template="{row_name}", col_template="P{col_name}", size=14)  # Tamaño de títulos de facetas
g.tick_params(axis='both', labelsize=13)  # Tamaño de los números en los ejes
g._legend.set_title("TUBO")  # cambiar título si quieres
for text in g._legend.texts:
    text.set_fontsize(14)     # texto de los ítems
g._legend.get_title().set_fontsize(14)
plt.savefig("displot-data.png",
            dpi=300,
            bbox_inches='tight',
            transparent=True)
plt.show()
# Filtrar según condiciones
cond_a = (
        (df_melted['Row'] == '1') &
        (df_melted['Exp'] == '12')
)
df_filtered = df_melted.loc[cond_a]

ax = sns.boxplot(data=df_filtered,
                 x='Time',
                 y='Grey value',
                 hue='IHC',
                 palette=["#00FF00", "#80FF00", "#AAAAAA", "#808080", ],
                 )


sns.despine(top=True, right=True)
plt.title('Comparación de la intensidad de fluorescencia \n '
          'en muestras con y sin tubocuraine')
plt.xlabel('Tiempo')
plt.ylabel('Intensidad de Fluorecencia')
plt.savefig("data-exp-IHC.png",
            dpi=300,
            bbox_inches='tight',
            transparent=True)
plt.show()

cond_b = ((df_melted['Exp'] == '12'))
df_filteredB = df_melted.loc[cond_b]
g=sns.catplot(data=df_filteredB,
            x='Time',
            y='Grey value',
            hue='TUBO',
            col='Row',
            kind='bar',
            palette = ["#00FF00",  "#AAAAAA", ],
            legend=False,
)
# Título general
g.fig.suptitle('Intensidad de fluorescencia por fila', fontsize=16)
# Etiquetas de los ejes
g.set_axis_labels('Tiempo', 'Intensidad de Fluorescencia')
# Ajustar para que no se sobreponga el título
g.fig.subplots_adjust(top=0.85)
for ax in g.axes.flat:
    ax.text(0.85, 0.85, 'Control',
            color='#AAAAAA',
            transform=ax.transAxes,
            fontsize=12,
            ha='center',
            fontweight='bold')
    ax.text(0.85, 0.8, 'Tubocurarine',
            color='#00FF00',
            transform=ax.transAxes,
            fontsize=12,
            ha='center',
            fontweight='bold')

plt.savefig("graph__rows.png",
            dpi=300,
            bbox_inches='tight',
            transparent=True)
plt.show()


