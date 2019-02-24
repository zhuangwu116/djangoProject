from raven import Client

client = Client('http://a7401ad0ce9944b7ba8dcac4c966c0f8:432c5b1750c2494a94a986bf4bbe7666@127.0.0.1:9000/2')

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()
