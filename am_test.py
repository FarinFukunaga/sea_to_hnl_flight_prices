from amadeus import Client, ResponseError

amadeus = Client(
    client_id='vKkcB1zLtQ6VBApIvamZa5cSscpWNm8q',
    client_secret='mzxBdlej0zheLwAU'
)

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='SEA',
        destinationLocationCode='HNL',
        departureDate='2021-06-01',
        adults=1)
    print(response.data)
except ResponseError as error:
    print(error)