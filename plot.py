import numpy as np
import plotly.graph_objects as go

a = [-0.357943798843941, 0.484847030772083, 0.280845417857238,
     -0.416761002513456, -0.101238265689339, -0.508119506288902,
     -0.733814602759236, -0.437998360612335, 0.369992967993395,
     0.220737076878098, -0.256523434359690, 0.572254695699536,
     -0.011561328479343, -0.922634799117377, -0.125846274834508,
     0.625130842027771, 0.618854803444181, 0.305705663028004,
     0.553908900949884, -0.127011801311289, -0.345157077856109,
     0.120186265681394, 0.741851885697296, -0.550028826775126]


def xd(h, name):
    x = np.array_split(h, len(h) / 3)
    fig = go.Figure()
    for i in range(0, len(x)):
        for j in range(i + 1, len(x)):
            fig.add_trace(go.Scatter3d(x=[x[i][0], x[j][0]], y=[x[i][1], x[j][1]], z=[x[i][2], x[j][2]], mode='lines',
                                       line=dict(color='black', width=4)))
    fig.update_layout(showlegend=False)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)
    # fig.show()
    fig.write_html(name + ".html")

# xd(a)
