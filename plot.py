import numpy as np
import pandas as pd
import plotly.graph_objects as go


def plot3d(h, name):
    x = np.array_split(h, len(h) / 3)
    fig = go.Figure()
    for i in range(0, len(x)):
        for j in range(i + 1, len(x)):
            fig.add_trace(go.Scatter3d(x=[x[i][0], x[j][0]], y=[x[i][1], x[j][1]], z=[x[i][2], x[j][2]], mode='lines',
                                       line=dict(color='black', width=4)))
    fig.update_layout(showlegend=False)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)
    # fig.show()
    fig.write_html(f"photo/{name}.html")


def process_mistakes(what):
    with open(what) as fp:
        pso = fp.read()
    contents = pso.split(';')
    tmp = []
    for i in range(0, len(contents), 7):
        tmp.append(contents[i:i + 7])
    df = pd.DataFrame(columns=['size', 'strength', 'best_pred', 'mean_time', 'min_time', 'max_time', 'best_pos'],
                      data=tmp)
    df = df.astype({'size': 'int', 'strength': 'int', 'best_pred': 'float', 'mean_time': 'float', 'min_time': 'float',
                    'max_time': 'float', 'best_pos': 'object'})
    return df


with open("perfect_results.txt") as fp:
    x = fp.read()
contents = x.replace('\n', ' ').split(" ")
tmp = []
for i in range(0, len(contents), 3):
    tmp.append(contents[i:i + 3])
per_df = pd.DataFrame(columns=['size', 'strength', 'best_pred'], data=tmp)
per_df = per_df.astype({'size': 'int', 'strength': 'int', 'best_pred': 'float'})
pso_df = process_mistakes("pso_results.txt")
gen_df = process_mistakes("gen_results.txt")
best_pso = pso_df.nlargest(3, 'best_pred')
best_gen = gen_df.nlargest(3, 'best_pred')


def plot2(what, name):
    for i, r in what.iterrows():
        print(r['best_pos'])
        tmp = []
        for j in r['best_pos'].strip('][\n').split(' '):
            if len(j) > 0:
                tmp.append(float(j))
        plot3d(tmp, f"{name}_{r['size']}_{r['strength']}")


def plot(what):
    strengths = [3, 6, 10, 14]
    for j in strengths:
        ax = pso_df[pso_df['strength'] == j].plot(x='size', y=what, title=f"strenght {j}, {what}")
        gen_df[pso_df['strength'] == j].plot(ax=ax, x='size', y=what)
        if what != 'mean_time':
            per_df[pso_df['strength'] == j].plot(ax=ax, x='size', y=what)
        ax.legend(["PSO", "GEN", "PERF"])
        ax.figure.savefig(f"graphs/{what}/strenght{j}.png")


#
# plot('best_pred')
# plot('mean_time')
plot2(best_pso, "PSO")
plot2(best_gen, "GEN")
