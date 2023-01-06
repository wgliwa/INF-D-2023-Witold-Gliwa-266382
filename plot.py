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


def xd(h):
    x = np.array_split(h, len(h) / 3)
    fig = go.Figure()
    for i in range(0, len(x)):
        for j in range(i + 1, len(x)):
            fig.add_trace(go.Scatter3d(x=[x[i][0], x[j][0]], y=[x[i][1], x[j][1]], z=[x[i][2], x[j][2]], mode='lines'))
    # fig.show()
    fig.write_html("8Ap6.html")


# def xd2(h):
#     x = np.array_split(h, len(h) / 3)
#     plt.figure('SPLTV', figsize=(10, 5))
#     custom = plt.subplot(121, projection='3d')
#     for i in range(0, len(x)):
#         for j in range(i + 1, len(x)):
#             for k in range(j + 1, len(x)):
#                 x1 = x[i]
#                 y1 = x[j]
#                 z1 = x[k]
#                 custom.scatter(x1, y1, z1)
#
#                 # 1. create vertices from points
#                 verts = [list(zip(x1, y1, z1))]
#                 # 2. create 3d polygons and specify parameters
#                 srf = Poly3DCollection(verts, alpha=0, facecolor='#800000')
#                 # 3. add polygon to the figure (current axes)
#                 plt.gca().add_collection3d(srf)
#
#     plt.show()

xd(a)
# xd2(a)
