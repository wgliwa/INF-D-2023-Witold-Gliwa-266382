import dataframe_image as dfi
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly_gif import three_d_scatter_rotate, GIF


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
    gif = GIF(gif_name=f'gif/{name}')
    three_d_scatter_rotate(gif, fig)


pso_df = pd.read_csv("results/pso_results.csv", index_col=[0])
gen_df = pd.read_csv("results/gen_results.csv", index_col=[0])
per_df = pd.read_csv("resultsperfect_results.csv", index_col=[0])
psoL_df = pd.read_csv("results/xd.csv", index_col=[0])
gen2_df = pd.read_csv("results/gen2.csv", index_col=[0])
pso_df.name = "PSO_G"
gen_df.name = "GEN"
per_df.name = "SCIENTIST"
psoL_df.name = "PSO_L"
gen2_df.name = "GEN2"


def plot2(what, name):
    for i, r in what.iterrows():
        print(r['best_pos'])
        tmp = []
        for j in r['best_pos'].strip('][\n').split(' '):
            if len(j) > 0:
                tmp.append(float(j))
        plot3d(tmp, f"{name}_{r['size']}_{r['strength']}")


def plot(type, list):
    for j in strengths:
        ax = list[0][list[0]['strength'] == j].plot(x='size', y=type, title=f"strenght {j}, {type}", label=list[0].name)
        for i in list[1:]:
            if type in i.columns:
                i[i['strength'] == j].plot(ax=ax, x='size', y=type, label=i.name)
        ax.figure.savefig(f"graphs/{type}/strenght{j}.png")


def table(list1):
    list2 = []
    for i in list1:
        tmp = i.drop(columns=["best_pos", "min_time", "max_time", "mean_time"], errors='ignore') \
            .pivot(index='size', columns='strength')
        tmp.columns = tmp.columns.droplevel()
        tmp.name = i.name
        dfi.export(tmp, f"tables/{tmp.name}.png")
        list2.append(tmp)
    for i in list2[:-1]:
        dfi.export(list2[-1] - i, f"tables/{i.name} - SCIENTIST.png")


sizes = [*range(5, 12)]
strengths = [3, 6, 10, 14]
df_list = [pso_df, gen_df, psoL_df, gen2_df, per_df]
best_pso = pso_df.loc[pso_df['strength'] == 3]
best_gen = gen_df.loc[gen_df['strength'] == 3]
best_psoL = psoL_df.loc[gen_df['strength'] == 3]
bestg2 = gen2_df.loc[gen_df['strength'] == 3]
# plot('best_pred', df_list)
# plot('mean_time', df_list)
# plot2(best_pso, "PSO")
# plot2(best_gen, "GEN")
plot2(best_psoL, "PSO_L")
plot2(bestg2, "GEN2")
table(df_list)
