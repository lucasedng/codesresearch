import requests

response = requests.get(
    f'https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES'
)

site_return = response

print(site_return.text)