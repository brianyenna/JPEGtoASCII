from yattag import Doc
import os
import webbrowser as wb

doc, tag, text = Doc().tagtext()

with tag('body', style='background-color:black'):
    for colour in ['red', 'white', 'green']:
        with tag('text', style='white-space:PRE'):
            with tag('span', style='color:{}'.format(colour)):
                text('          *')

with tag('text', style='white-space:PRE'):
    with tag('span', style='color:white'):
        text('HELLO')


# color = [(255, 255, 0), (255, 0, 255), (255, 123, 123)]
# for i in range(3):
#     colour = color[i]
#     print(colour)
#     with tag('text', style='white-space:PRE'):
#         with tag('span', style='color:rgb{}'.format(colour)):
#             text('          *')

# doc.stag('br')
# # doc._append('<br/>')

# for i in range(3):
#     colour = color[i]
#     print(colour)
#     with tag('text', style='white-space:PRE;line-height:5;font-size:3px'):
#         with tag('span', style='color:rgb{}'.format(colour)):
#             text('          *')

with open('./test.html', 'w') as f:
    f.write(doc.getvalue())

# wb.open('file://'+os.path.realpath('./test.html'))



# from sklearn.cluster import KMeans
# from skimage import io

# img = io.imread('./Images/apple.jpg')
# print('1', img.shape)
# X = img.reshape(-1, 3) 
# print('2', img.shape)
# print('X', X.shape)
# kmeans = KMeans(n_clusters=10).fit(X)
# cluster_centre = kmeans.cluster_centers_
# labels = kmeans.labels_
# test = cluster_centre[labels]