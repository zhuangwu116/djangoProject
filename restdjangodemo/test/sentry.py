from raven import Client

client = Client('http://27af5ea23a7e4a4c847fc741aa3d8e2a:cb57686f3fde42b19457816764c49039@zhuangwu116.club:9000/3')

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()
    client.captureMessage('Something went fundamentally wrong')
